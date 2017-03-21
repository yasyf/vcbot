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
      fname = constants.TWEET_PATH(target)
      if not os.path.exists(fname):
        open(fname, 'a').close()
      with open(fname, 'rb') as f:
        lines = set(f.readlines())
      with open(fname, 'ab') as f:
        tweets = self.client.user_timeline(target, count=MAX_COUNT, include_rts=False)
        while len(tweets):
          oldest = tweets[-1].id - 1
          new_lines = filter(lambda t: t not in lines, map(extract_text, tweets))
          lines |= set(new_lines)
          text = '\n'.join(new_lines)
          f.write(text)
          tweets = self.client.user_timeline(target, count=MAX_COUNT, include_rts=False, max_id=oldest)
