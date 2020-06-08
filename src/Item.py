import datetime

class Item:
  def  __init__(self, message):
    self.message = message
    self.start_time = datetime.datetime.now()

