# for notes on data extraction, refer WorldRecords.ipynb

import gazpacho
import json
import os
from swimclub import DataFile

# Constants
URL = "https://en.wikipedia.org/wiki/List_of_world_records_in_swimming"
TABLES = (0, 1, 3, 4)
COURSES = ("LC Men", "LC Women", "SC Men", "SC Women")
JSONDATA = DataFile.JSONDATA.value
WHERE = "/home/hfpy/app/"

# prepare parsed HTML content for data extraction
soup = gazpacho.Soup.get(URL)
all_tables = soup.find(tag="table", mode="all")

# record required column data as dictionary-of-dictionaries in data
data = {}
for table, course in zip(TABLES, COURSES):
  rows = all_tables[table].find(tag="tr", mode="all")[1:] # escape header row
  data[course] = {}
  for row in rows:
    columns = row.find(tag="td", mode="all")
    event = columns[0].text
    time = columns[1].text
    if "relay" not in event: 
      data[course][event] = time

# write data to JSON file
current_dir = os.getcwd()
if "Z" in current_dir: # local project directory
  with open(JSONDATA, mode="w") as df:
    json.dump(obj=data, fp=df)
  print("Data saved in local project directory")
else:
  with open(WHERE + JSONDATA, mode="w") as df:
    json.dump(obj=data, fp=df)
  print("Data saved in production environment")
