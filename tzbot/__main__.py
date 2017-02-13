from tzbot import TZBot

def start():
  bot = TZBot()
  bot.come_alive()

def train():
  bot = TZBot()
  bot.train()

def test():
  bot = TZBot()
  print bot.generate_tweet('TZBot')

if __name__ == '__main__':
  start()
