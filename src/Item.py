import datetime

class Item:
   def  __init__(self, message, start_time = None):
      self.message = message

      # set start time
      if start_time is None:
         self.start_time = datetime.datetime.now()
      else:
         self.start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S.%f")


   def getDict(self):
      dictData = {
         "message": self.message,
         "start_time": self.start_time
      }

      return dictData

   def getDisplayDate(self):
      return self.start_time.strftime("%x")

   def getDisplayTime(self):
      return self.start_time.strftime("%I:%M %p")





