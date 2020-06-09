import datetime

class Item:
   def  __init__(self, message):
      self.message = message
      self.start_time = datetime.datetime.now()


   def getDict(self):
      dictData = {
         "message": self.message,
         "start_time": self.start_time
      }

      return dictData

   def getDisplayDate(self):
      return self.start_time.strftime("%x")

   def getDisplayDate(self):
      return self.start_time.strftime("%I:%M %p")

      



