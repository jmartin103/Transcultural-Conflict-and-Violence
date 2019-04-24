import sys
import csv
import json
from pymongo import MongoClient

#fname = './50ImagesMain.csv'

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

def addToDB(fname, tagdict):
  client = MongoClient("mongodb://localhost:27017")
  db = client['image-db']
  img_data = db['imgdata']

  data_json = []
  with open(fname, 'r') as f:
    data = list(csv.reader(f))
  d = {}
  for row in data[1:]:
    d['url'] = row[0]
    d['size'] = row[1]
    d['province'] = row[2]
    d['tags'] = tagdict[row[0]]
    d['createdOn'] = row[0][0:8]   

    data_json.append(d)
    
  data_json = json.dumps(data_json)
  data_json = json.loads(data_json)

  print(data_json)

  for entry in data_json:
    img_data.insert_one(entry)

def getTagDictionary(fname):
  tags = getTags(fname)
  tagdict = produceTagDictionary(tags)
  #print(tags)
  #print(tagdict)
  return tagdict

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

def main():
  tagdict = getTagDictionary(sys.argv[1])
  addToDB(sys.argv[2],tagdict)
  
  
main()


    
