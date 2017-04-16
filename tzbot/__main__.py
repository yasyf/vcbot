from tzbot import TZBot

def start():
  bot = TZBot()
  bot.train()
  bot.come_alive()

def train():
  bot = TZBot()
  bot.train()

def test():
  bot = TZBot()
  print bot.generate_reply('TZBot', 'yes no hello love Berkeley')

if __name__ == '__main__':
  start()
