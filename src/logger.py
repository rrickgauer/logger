from Utilities import Utilities as util
from Item import Item
import json
from os import path


# constants
DATA_FILE = '.logger-data.json'





def createEmptyDataFile():
  f = open(DATA_FILE, "w")



########################## MAIN FUNCTION ########################################


# create new config file if one does not exist in the local directory
if not path.exists(DATA_FILE):
  createEmptyDataFile()

print('hello')

