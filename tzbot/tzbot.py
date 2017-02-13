from stream import Stream

class TZBot(object):
  def __init__(self):
    self.stream = Stream()

  def come_alive(self):
    self.stream.start()
