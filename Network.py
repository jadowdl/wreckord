#!/usr/bin/env python

## from graph_tool.all import *

class Network:
  def __init__(self):
    self._records = {}

  def _hasRecord(self, name):
    return name in self._records

  # I keep track of both just because I don't know the equivalent of hasOwnProperty for python...
  def _addRecord(self, record):
    assert record._name not in self._records
    setattr(self, record._name, record)
    self._records[record._name] = record

  def _save(self): pass

  def _show(self):
    ## g = Graph()
    ## for record in self._records:
    ##   v = g.add_vertex() 
    pass  

__NETWORK = Network()
