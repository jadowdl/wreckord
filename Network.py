#!/usr/bin/env python

## from graph_tool.all import *

import json


DUMP_VERSION = 1

class Network:
  def __init__(self, filestore='contextNet.json'):
    self._records = {}
    self._filestore = filestore

  def _hasRecord(self, name):
    return name in self._records

  # I keep track of both just because I don't know the equivalent of hasOwnProperty for python...
  def _addRecord(self, record):
    assert record._name not in self._records
    setattr(self, record._name, record)
    self._records[record._name] = record

  # looking for _load(self)? it doesn't exist.  We've hit a design bottleneck; for
  # the global variables approach in __NETWORK to work, it only makes sense to
  # make __load() in wreckord.py
  def _save(self):
    records = [r._marshal(as_json=False) for r in self._records.values()]
    dump = {
      "DUMP_VERSION": DUMP_VERSION,
      "records": records
    }
    stream = open(self._filestore, 'w')
    stream.write(json.dumps(dump))
    stream.flush()
    stream.close()

  def _show(self):
    ## g = Graph()
    ## for record in self._records:
    ##   v = g.add_vertex() 
    pass  

__NETWORK = Network()
