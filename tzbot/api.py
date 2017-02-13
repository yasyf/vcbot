import tweepy, os

class API(object):
  def __init__(self):
    self.auth = tweepy.OAuthHandler(os.getenv('TWITTER_API_KEY'), os.getenv('TWITTER_API_SECRET'))
    self.auth.set_access_token(os.getenv('TWITTER_ACCESS_TOKEN'), os.getenv('TWITTER_ACCESS_SECRET'))

  @property
  def client(self):
    try:
      return self.__client
    except AttributeError:
      self.__client = tweepy.API(self.auth)
      return self.__client

  def tweet(self, text, parent_id=None):
    self.client.update_status(text, parent_id)
