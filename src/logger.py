import json
from os import path
import argparse
import datetime
from beautifultable import BeautifulTable

# constants
DATA_FILE = '.logger-data.json'





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


def space(numSpaces = 1):
   for x in range(numSpaces):
      print('')

def getTable(data, columns=[]):
   table = BeautifulTable(max_width=1000)
   table.set_style(BeautifulTable.STYLE_COMPACT)
   table.column_headers = columns

   for row in data:
      table.append_row(row)

   table.column_alignments = BeautifulTable.ALIGN_LEFT
   return table


# prints a table version of the items
def printItems(items):
   data = []

   for item in items:
      row = []
      row.append(item.getDisplayDate())
      row.append(item.getDisplayTime())
      row.append(item.message)
      data.append(row)

   print(getTable(data, ['Date', 'Time', 'Message']))

# creates an empty data file
def createEmptyDataFile():
   f = open(DATA_FILE, "w")
   f.write("[]")
   f.close()


# returns the data from the DATA_FILE
def readDataFile():
   with open(DATA_FILE) as dataFile:
      items = []
      data = json.loads(dataFile.read())

      for d in data:
         items.append(Item(d['message'], d['start_time']))

      return items

# returns a list of item classes from the data file
def writeItemsToDataFile(items):
   itemsDict = getItemsDictFromList(items)
   jsonString = json.dumps(itemsDict, indent=4, sort_keys=True, default=str)

   with open(DATA_FILE, "w") as dataFile:
      dataFile.write(jsonString)

# returns a list of item dicts
def getItemsDictFromList(itemsList):
   itemsDict = []

   for item in itemsList:
      itemDict = {
         "message": item.message,
         "start_time": item.start_time
      }

      itemsDict.append(itemDict)

   return itemsDict


def getItemsInDay(items, day = None):      
   if day is None:
      day = datetime.datetime.now().strftime("%x")

   itemsInDay = []
   for item in items:
      if item.getDisplayDate() == day:
         itemsInDay.append(item)

   return itemsInDay


########################## MAIN FUNCTION ########################################




# create command line arguments
parser = argparse.ArgumentParser(description="View your database table's fields and types")
parser.add_argument('-a', '--add', nargs=1, help="Add a new item to your log")
parser.add_argument('-d', '--day', nargs=1, help="(dd/mm/yy) View log on specified day")
args = parser.parse_args()

# create new config file if one does not exist in the local directory
if not path.exists(DATA_FILE):
   createEmptyDataFile()

# original data from file
items = readDataFile()


# user requested to add a new item
if args.add != None:
   newItemMessage = args.add[0]
   newItem = Item(newItemMessage) 
   items.append(newItem)
   writeItemsToDataFile(items)
   print('Item was added.')
   space(2)
   printItems([newItem])

# user requested to view items in a specified day
elif args.day != None:
   dayToSearch = args.day[0]
   itemsInDay = getItemsInDay(items, dayToSearch)
   printItems(itemsInDay)

# print the items for today
else:
   itemsInDay = getItemsInDay(items)
   printItems(itemsInDay)