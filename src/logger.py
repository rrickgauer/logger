from Utilities import Utilities as util
from Item import Item
import json
from os import path
import argparse

# constants
DATA_FILE = '.logger-data.json'


# prints a table version of the items
def printItems(items):
   data = []
   for item in items:
      data.append([item['message'], item['start_time']])

   print(util.getTable(data, ['Message', 'Start Time']))


# creates an empty data file
def createEmptyDataFile():
   f = open(DATA_FILE, "w")
   f.write("[]")
   f.close()


# returns the data from the DATA_FILE
def readDataFile():
   with open(DATA_FILE) as dataFile:
      data = json.loads(dataFile.read())
      return data


def writeItemsToDataFile(items):
   jsonString = json.dumps(items, indent=4, sort_keys=True, default=str)

   with open(DATA_FILE, "w") as dataFile:
      dataFile.write(jsonString)


########################## MAIN FUNCTION ########################################

# create command line arguments
parser = argparse.ArgumentParser(description="View your database table's fields and types")
parser.add_argument('-a', '--add', nargs=1, help="Add a new item to your log")
parser.add_argument('-d', '--day', nargs=1, help="() View log on specified day")
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
   items.append(newItem.getDict())
   writeItemsToDataFile(items)

util.space(2)
printItems(items)













