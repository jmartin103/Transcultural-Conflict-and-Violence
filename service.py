from pymongo import MongoClient
from flask import Flask, jsonify
from flask_cors import CORS
from flask import Response
from flask import abort
from flask import make_response
from flask import request, render_template, send_from_directory
from datetime import datetime, timedelta

import json
import rdflib
import query

app = Flask(__name__, static_url_path='')

@app.route('/static/<path:path>')
def serveStaticFile(path):
   return send_from_directory('static', path)

@app.route('/provinces', methods=['GET'])
def get_provinces():
  client = MongoClient('mongodb://localhost:27017')
  db = client['image-db']
  col = db['imgdata']
  doc = col.find({}, {"_id": 0, "province": 1})
  provinces = []
  for x in doc:
    if x not in provinces:
      provinces.append(x)

  for i in range(len(provinces)):
    if provinces[i]['province'] == 'NA':
      del provinces[i]
      break

  return jsonify({'provinces': provinces})

@app.route('/', methods=['GET'])
def query():
  client = MongoClient('mongodb://localhost:27017')
  db = client['image-db']
  col = db['imgdata']
  doc = col.find({}, {"_id": 0})
  info = []
  for x in doc:
    if x not in info:
      info.append(x)

  return jsonify({'images': info})

@app.route('/queries', methods=['POST'])
def queryImages():
  datequery = request.json['datequery']
  province = request.json['province']
  date1 = int(request.json['date1'].replace("-", ""))
  violent = request.json['violent']

  client = MongoClient('mongodb://localhost:27017')
  db = client['image-db']
  col = db['imgdata']

  if datequery == 'on':
    if not violent:
      query = { "createdOn": date1, "province": province }
    else:
      query = { "createdOn": date1, "province": province, "tags": {"$ne": "Gore" } }
    doc = col.find(query, {"_id": 0})
  elif datequery == 'before':
    if not violent:
      query = { "createdOn": { "$lt": date1 }, "province": province }
    else:
      query = { "createdOn": { "$lt": date1 }, "province": province, "tags": {"$ne": "Gore" } }
    doc = col.find(query, {"_id": 0})
  elif datequery == 'after':
    if not violent:
      query = { "createdOn": { "$gt": date1 }, "province": province }
    else:
      query = { "createdOn": { "$gt": date1 }, "province": province, "tags": {"$ne": "Gore" } }
    doc = col.find(query, {"_id": 0})
  else:
    date2 = int(request.json['date2'].replace("-", ""))
    if not violent:
      query = { "createdOn": { "$gte": date1, "$lte": date2 }, "province": province }
    else:
      query = { "createdOn": { "$gte": date1, "$lte": date2 }, "province": province, "tags": {"$ne": "Gore" } }
    doc = col.find(query, {"_id": 0})
  return jsonify({'results': list(doc)})

if __name__ == '__main__':
  app.run(host='localhost', port=8000, debug=True)
