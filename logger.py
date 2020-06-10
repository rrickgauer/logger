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

   def getDayOfWeekNum(self):
      return self.start_time.strftime("%w")

   def getDayOfYearNum(self):
      return self.start_time.strftime("%j")

   def getWeekdayShort(self):
      return self.start_time.strftime("%a")


# print all items that fall within a specified date's week number
def printDaysOfWeekItems(weekdayLists):
   # create a full list of the weekly messages to print out
   fullList = []
   for l in weekdayLists:
      for x in l:
         fullList.append(x)

   # print items
   printItems(fullList)



# prints a table version of the items
def printItems(items):
   data = []
   # currentDayNumber = items[0].getDayOfYearNum()

   for item in items:

      # if item is in a different day than the previous print line break
      # if item.getDayOfYearNum() != currentDayNumber:
      #    currentDayNumber = item.getDayOfYearNum()
      #    data.append(['', '', '', '', ''])

      data.append([item.index, item.getWeekdayShort(), item.getDisplayDate(), item.getDisplayTime(), item.message])

   print(getTable(data, ['Index', 'Day', 'Date', 'Time', 'Message']))


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

# writes the list of item classes to the data file
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
      
   if day is None: day = datetime.datetime.now().strftime("%x")

   itemsInDay = []
   for item in items:
      if item.getDisplayDate() == day:
         itemsInDay.append(item)

   return itemsInDay

# remove an item at the specified index
# returns the new item list with ids reset
def removeItem(items, index):
   items.pop(int(index))
   return resetItemIds(items)

# combines sortItems() and resetItemIds()
def sortAndResetItems(items):
   items = sortItems(items) 
   items = resetItemIds(items)

   return items

# returns a sorted list of items
def sortItems(items):
   return sorted(items, key=lambda x: x.start_time, reverse=False)


# returns list of items with correct indexes
def resetItemIds(items):
   for count in range(len(items)):
      items[count].index = count

   return items

# update an item's message
def editItemMessage(items, index, message):
   items[int(index)].message = message
   return items

# returns a date's weeknumber (0-51)
# needs to be a datetime.datetime object
def getWeekNum(date):
   return date.strftime("%U")





############################ MAIN ########################################

# create command line arguments
parser = argparse.ArgumentParser(description="Your personal activity logger.")
parser.add_argument('-n', '--new', nargs=1, metavar=('Message'), help="Insert new item to your log")
parser.add_argument('-d', '--day', nargs=1, metavar=('Day'), help="View your log on specified day (dd/mm/yy) ")
parser.add_argument('-r', '--remove', nargs=1, metavar=('Index'), help="Remove item at the specified index")
parser.add_argument('-e', '--edit', nargs=2, metavar=('Index', 'Message'), help="Edit an item's message")
parser.add_argument('-w', '--week', nargs=1, metavar=('Date'), help="Display weekly log")
parser.add_argument('-t', '--time', nargs=1, metavar=('Index'), help="Update an item's start time")
parser.add_argument('-a', '--all', action="store_true", help="Update an item's start time")
args = parser.parse_args()

# create new data file if one does not exist
if not os.path.exists(DATA_FILE):
   createEmptyDataFile()

items = readDataFile()     # original data from file

# user requested to add a new item
if args.new != None:
   newItemMessage = args.new[0]
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

# remove an item
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
         weekdayLists[int(item.getDayOfWeekNum())].append(item)

   space()
   printDaysOfWeekItems(weekdayLists)


# user start time
elif args.time != None:
   # get item to be modified
   item = items[int(args.time[0])]
   print('\nItem to be updated:\n')
   printItems([item])
 
   # remove old item
   items = removeItem(items, item.index)

   # make new datetime object 
   newDate = input('\nEnter new date (mm/dd/yy): ')
   newTime = input('Enter new time (HH:MM AM/PM): ')
   newStartTime = datetime.datetime.strptime(newDate + ' ' + newTime, "%m/%d/%y %I:%M %p")
   newItem = Item(item.message, item.index, str(newStartTime))

   # add updated item to the list and data file
   items.append(newItem)
   writeItemsToDataFile(sortAndResetItems(items))
   print('\nItem updated')

# print out all items
elif args.all == True:
   printItems(items)
   space(1)



# print the items for today
else:
   itemsInDay = getItemsInDay(items)
   space(2)
   printItems(itemsInDay)
   space()

# update and save items
writeItemsToDataFile(sortAndResetItems(items))
