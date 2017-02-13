from api import API
from stream import Stream
import markovify, constants

TWEET_SIZE = 140

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
    with open(constants.TWEETS_PATH) as f:
      text = f.read()

    twitter_model = markovify.NewlineText(text)
    # TODO: Medium model

    self.model = twitter_model

  def generate_tweet(self, username):
    tweet = self.model.make_short_sentence(TWEET_SIZE - len(username) - 1)
    return '@{username} {tweet}'.format(username=username, tweet=tweet)
