from vcbot import VCBot

def start():
  bot = VCBot()
  bot.train()
  bot.come_alive()

def train():
  bot = VCBot()
  bot.train()

def test():
  bot = VCBot()
  print bot.generate_tweet('VCBot', 'yes no hello love Stanford')

if __name__ == '__main__':
  start()
