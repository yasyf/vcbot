import tweepy, os, constants

MAX_COUNT = 200

skip_mentions = lambda w: not w.startswith('@')
extract_text = lambda t: ' '.join(filter(skip_mentions, t.text.split(' '))).encode('utf-8')

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

  def download_all_target_tweets(self):
    for target in constants.TARGETS:
      with open(constants.TWEET_PATH(target), 'wb') as f:
        tweets = self.client.user_timeline(target, count=MAX_COUNT)
        while len(tweets):
          oldest = tweets[-1].id - 1
          text = '\n'.join(map(extract_text, tweets))
          f.write(text)
          tweets = self.client.user_timeline(target, count=MAX_COUNT, max_id=oldest)
