import sys
import csv
import json
from pymongo import MongoClient

def getTags(fname):
  with open(fname, 'r') as f:
    tags = list(csv.reader(f))
    result = []
    for t in tags[1:]:
      ts = list(zip(t,tags[0]))
      for x in ts:
        if not x[0] == '':
          result.append(x) 
    return result

def produceTagDictionary(tags):
  result = {}
  for x in tags:
    if x[0] in result:
      result[x[0]].append(x[1])
    else:
      result[x[0]] = [x[1]]
  return result

def main():
  tags = getTags(sys.argv[1])
  tagdict = produceTagDictionary(tags)
  print(tags)
  print(tagdict)

  client = MongoClient("mongodb://localhost:27017")
  db = client['imgtagdb']
  tag_data = db['tagdata']

  d = {}
  json_data = []

  for key, value in tagdict.items():
    d['url'] = key
    d['tags'] = value
    json_data.append(d)

    json_data = json.dumps(json_data)
    json_data = json.loads(json_data)

  print(json_data)

  for entry in json_data:
    tag_data.insert_one(entry)
  
main()

#import pandas as pd
#
#def main():
#  df = pd.read_csv(sys.argv[1], delimiter=',')
#  # Or export it in many ways, e.g. a list of tuples
#  tuples = [tuple(x) for x in df.values]
#  print(tuples)
#  # or export it as a list of dicts
#  dicts = df.to_dict().values()
#  print(dicts)
#
#main()
