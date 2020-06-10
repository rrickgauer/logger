import json
import os
import argparse
import datetime
from beautifultable import BeautifulTable
from sys import argv

# constants 
# SCRIPT_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))   # absolute path of the python script location
# DATA_FILE = SCRIPT_PATH + '\\.logger-data.json'                # abs path of data file

DATA_FILE = '.logger-data.json'


# print specified number of line breaks
def space(numSpaces = 1):
   for x in range(numSpaces):
      print('')

# returns a BeautifulTable object
def getTable(data, columns=[]):
   table = BeautifulTable(max_width=1000)
   table.set_style(BeautifulTable.STYLE_COMPACT)
   table.column_headers = columns

   for row in data:
      table.append_row(row)

   table.column_alignments = BeautifulTable.ALIGN_LEFT
   return table

class Item:
   def  __init__(self, message, index, start_time = None):
      self.message = message
      self.index = index

      # set start time
      if start_time is None:
         self.start_time = datetime.datetime.now()
      else:
         self.start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")

      # round up to nearest 15 minute interval
      discard = datetime.timedelta(minutes=self.start_time.minute % 15, seconds=self.start_time.second, microseconds=self.start_time.microsecond)
      self.start_time -= discard
      if discard >= datetime.timedelta(minutes=8):
          self.start_time += datetime.timedelta(minutes=15)


   # returns a dictionary of itself
   def getDict(self):
      return {
         "index": self.index,
         "message": self.message,
         "start_time": self.start_time
      }

   # returns the formatted version of the date start time
   def getDisplayDate(self):
      return self.start_time.strftime("%x")

   # returns the formatted version of the time start time
   def getDisplayTime(self):
      return self.start_time.strftime("%I:%M %p")

   def getWeekNum(self):
      # return self.start_timed.strftime("%U")
      return getWeekNum(self.start_time)

   def getDayNum(self):
      return self.start_time.strftime("%w")


# prints a table version of the items
def printItems(items):
   data = []
   for item in items:
      if item == '':
         data.append(['', '', '', ''])
      else:
         data.append([item.index, item.getDisplayDate(), item.getDisplayTime(), item.message])

   print(getTable(data, ['Index', 'Date', 'Time', 'Message']))


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
         item = Item(d['message'], d['index'], d['start_time'])
         # items.append(Item(d['index'], d['message'], d['start_time']))
         items.append(item)

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
      itemsDict.append({
         "index": item.index,
         "message": item.message,
         "start_time": item.start_time
      })

   return itemsDict

# returns a list of items that are in specified day
def getItemsInDay(items, day = None):      
   if day is None:
      day = datetime.datetime.now().strftime("%x")

   itemsInDay = []
   for item in items:
      if item.getDisplayDate() == day:
         itemsInDay.append(item)

   return itemsInDay

# remove an item at the specified index
def removeItem(items, index):
   items.pop(int(index))
   return resetItemIds(items)

# resets the items ids
def resetItemIds(items):
   for count in range(len(items)):
      items[count].index = count

   return items

# update an item's message
def editItemMessage(items, index, message):
   items[int(index)].message = message
   return items

# returns a date's weeknumber (0-51)
def getWeekNum(date):
   return date.strftime("%U")

# returns a sorted list of items
def sortItems(items):
   return sorted(items, key=lambda x: x.start_time, reverse=False)

def printDaysOfWeekItems(weekdayLists):
   # add a line break
   for l in weekdayLists:
      l.append('')

   # create a full list of the weekly messages to print out
   fullList = []
   for l in weekdayLists:
      for x in l:
         fullList.append(x)

   # print items
   printItems(fullList)


############################ MAIN ########################################

# create command line arguments
parser = argparse.ArgumentParser(description="Your personal activity logger.")
parser.add_argument('-a', '--add', nargs=1, metavar=('Message'), help="Add a new item to your log")
parser.add_argument('-d', '--day', nargs=1, metavar=('Day'), help="View your log on specified day (dd/mm/yy) ")
parser.add_argument('-r', '--remove', nargs=1, metavar=('Index'), help="Remove item at the specified index")
parser.add_argument('-e', '--edit', nargs=2, metavar=('Index', 'Message'), help="Edit an item's message")
parser.add_argument('-w', '--week', nargs=1, metavar=('Date'), help="Display weekly log")
args = parser.parse_args()

# create new data file if one does not exist
if not os.path.exists(DATA_FILE):
   createEmptyDataFile()

items = readDataFile()     # original data from file
items = sortItems(items)   # sort the items by date

# user requested to add a new item
if args.add != None:
   newItemMessage = args.add[0]
   index = len(items)
   newItem = Item(message=newItemMessage, index=index) 
   items.append(newItem)
   writeItemsToDataFile(items)
   print('Item was added.')

# user requested to view items in a specified day
elif args.day != None:
   dayToSearch = args.day[0]
   itemsInDay = getItemsInDay(items, dayToSearch)
   space(2)
   printItems(itemsInDay)

# remove am item
elif args.remove != None:
   items = removeItem(items, args.remove[0])
   print('Item was removed from log')
   writeItemsToDataFile(items)

# edit an item message
elif args.edit != None:
   index = args.edit[0]
   newMessage = args.edit[1]
   items = editItemMessage(items, index, newMessage)
   print('Item message updated')
   writeItemsToDataFile(items)

# print the log of the week that encapsulates the date given
elif args.week != None:
   # get the user input date 
   dayToSearch = datetime.datetime.strptime(args.week[0], "%x")
   weeknum = getWeekNum(dayToSearch)
   
   # create 7 empty lists to hold items for day of the week
   weekdayLists = [[], [], [], [], [], [], []]

   # place appropriate items that fall under the week number into their respective day lists
   for item in items:
      if item.getWeekNum() == weeknum:
         weekdayLists[int(item.getDayNum())].append(item)

   printDaysOfWeekItems(weekdayLists)

# print the items for today
else:
   itemsInDay = getItemsInDay(items)
   space()
   printItems(itemsInDay)

