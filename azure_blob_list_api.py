#! /usr/local/bin/python
# -*- coding: utf-8 -*-
from calendar import timegm
from datetime import datetime
import _strptime  # https://bugs.python.org/issue7980
from flask import Flask, request, jsonify
from azure.storage.blob import BlockBlobService
import os
app = Flask(__name__)

app.debug = True


def convert_to_time_ms(timestamp):
    return 1000 * timegm(datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ').timetuple())

def fetch_data_last_modified():
    block_blob_service = BlockBlobService(account_name='ACCNAME', sas_token='SASTOKEN')
    container_name = 'CONTAINERNAME'
    generator = block_blob_service.list_blobs(container_name, prefix=None,delimiter=None)
    print (generator)
    y = sorted(generator, key=lambda x: x.properties.last_modified, reverse=True)

    task = []
    for blob in y:
      blob_list = []
      blob_list.append(blob.name)
      blob_list.append(blob.properties.last_modified)        
      task.append(blob_list)
    return task

def fetch_data_size():
    block_blob_service = BlockBlobService(account_name='ACCNAME', sas_token='SASTOKEN')
    container_name = 'CONTAINERNAME'
    generator = block_blob_service.list_blobs(container_name, prefix=None,delimiter=None)
    print (generator)
    y = sorted(generator, key=lambda x: x.properties.last_modified, reverse=True)

    task = []
    for blob in y:
      blob_list = []        
      blob_list.append(blob.properties.content_length/1024)
      blob_list.append(blob.properties.last_modified)
      task.append(blob_list)
    return task

@app.route('/')
def health_check():
    return "Datasource is healthy"


@app.route('/search', methods=['POST'])
def search():
    return jsonify(['Blob Name'])


@app.route('/query', methods=['POST'])
def query():
    req = request.get_json()
    data = [
        {
            "target": req['targets'][0]['target'],
            "datapoints": fetch_data_last_modified()
        },
        {
            "target": "Size",
            "datapoints": fetch_data_size()
        }
    ]
    return jsonify(data)


@app.route('/annotations', methods=['POST'])
def annotations():
    req = request.get_json()
    data = [
        {
            "annotation": 'This is the annotation',
            "time": (convert_to_time_ms(req['range']['from']) +
                     convert_to_time_ms(req['range']['to'])) / 2,
            "title": 'Deployment notes',
            "tags": ['tag1', 'tag2',],
            "text": 'Hm, something went wrong...'
        }
    ]
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
