import tweepy, os

USERNAME = os.getenv('TWITTER_USERNAME')

class StreamListener(tweepy.StreamListener):
  def __init__(self, bot, *args, **kwargs):
    self.bot = bot
    super(StreamListener, self).__init__(*args, **kwargs)

  def on_status(self, status):
    if status.user.screen_name != USERNAME and not status.retweeted:
      self.api.update_status(self.bot.generate_tweet(status.user.screen_name), status.id)
    else:
      self.bot.maybe_tweet()

  def keep_alive(self):
    self.bot.maybe_tweet()

class Stream(object):
  def __init__(self, bot):
    self.bot = bot
    self.api = bot.api.client
    self.listener = StreamListener(self.bot, self.api)

  def start(self):
    tweepy.Stream(auth=self.api.auth, listener=self.listener).userstream()
