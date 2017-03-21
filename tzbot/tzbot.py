from api import API
from stream import Stream
import markovify, constants, os, time, random

TWEET_SIZE = 140
MEDIUM_WEIGHT = 0.05
TWEET_DELAY = 60 * 60 * 12
SEED_TRIES = 3
SEED_PROB = 0.7

def markovify_file(path):
  if not os.path.exists(path):
    return markovify.NewlineText("")

  with open(path) as f:
    return markovify.NewlineText(f.read())

def filter_out(tweet, f):
  not_f = lambda w: not f(w)
  return ' '.join(filter(not_f, tweet.split(' ')))

class TZBot(object):
  def __init__(self):
    self.api = API()
    self.stream = Stream(self)
    self.last_tweet = 0

    self._set_model()

  def maybe_tweet(self):
    if (time.time() - self.last_tweet) > TWEET_DELAY:
      self.last_tweet = time.time()
      self.api.tweet(self.model.make_short_sentence(TWEET_SIZE))

  def come_alive(self):
    self.maybe_tweet()
    self.stream.start()

  def train(self):
    self.api.download_all_target_tweets()

  def _set_model(self):
    tweet_models = map(lambda target: markovify_file(constants.TWEET_PATH(target)), constants.TARGETS)
    medium_model = markovify_file(constants.MEDIUM_PATH)
    self.model = markovify.combine(tweet_models + [medium_model], [1] * len(tweet_models) + [MEDIUM_WEIGHT])

  def generate_tweet(self, username, seed):
    words = seed.split(' ')
    length = TWEET_SIZE - len(username) - 1
    tweet = None

    try:
      if random.random() <= SEED_PROB:
        try:
          first_seed = filter(lambda w: w.istitle(), words)[0]
        except IndexError:
          first_seed = random.choice(words)
        possible_seeds = [first_seed] + random.sample(words, SEED_TRIES - 1)

        for seed in possible_seeds:
          state = (markovify.chain.BEGIN, seed)
          try:
            tweet = self.model.make_short_sentence(length, init_state=state)
          except (KeyError, UnicodeDecodeError):
            continue
          if tweet:
            break
    except:
      # something bad happened
      pass

    if not tweet:
      tweet = self.model.make_short_sentence(length)

    tweet = filter_out(tweet, lambda w: w.startswith('@') or w.startswith('http'))

    return '@{username} {tweet}'.format(username=username, tweet=tweet)
