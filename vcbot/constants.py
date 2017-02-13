import os

VCBOT_DIR = os.path.dirname(os.path.realpath(__file__))
TWEETS_DIR = os.path.join(VCBOT_DIR, os.pardir, 'data', 'tweets')
TWEET_PATH = lambda username: os.path.join(TWEETS_DIR, '{}.txt'.format(username))
MEDIUM_PATH = os.path.join(VCBOT_DIR, os.pardir, 'data', 'medium.txt')
TARGETS = os.getenv('TWITTER_TARGETS').split(',')
