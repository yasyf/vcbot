from api import API
from stream import Stream
import markovify, constants, os

TWEET_SIZE = 140
MEDIUM_WEIGHT = 0.05

def markovify_file(path):
  if not os.path.exists(path):
    return markovify.NewlineText("")

  with open(path) as f:
    return markovify.NewlineText(f.read())

class TZBot(object):
  def __init__(self):
    self.api = API()
    self.stream = Stream(self)
    self._set_model()

  def come_alive(self):
    self.stream.start()

  def train(self):
    self.api.download_all_target_tweets()

  def _set_model(self):
    tweet_models = map(lambda target: markovify_file(constants.TWEET_PATH(target)), constants.TARGETS)
    medium_model = markovify_file(constants.MEDIUM_PATH)
    self.model = markovify.combine(tweet_models + [medium_model], [1] * len(tweet_models) + [MEDIUM_WEIGHT])

  def generate_tweet(self, username):
    tweet = self.model.make_short_sentence(TWEET_SIZE - len(username) - 1)
    return '@{username} {tweet}'.format(username=username, tweet=tweet)
