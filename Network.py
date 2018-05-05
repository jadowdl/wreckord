#!/usr/bin/env python

import igraph
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
    g = igraph.Graph(directed=True)

    # enumerate vertex numbers
    recordNames = [r for r in self._records.keys()]
    vertNumbers = {}
    for i in range(0, len(recordNames)):
      vertNumbers[recordNames[i]] = i

    # Add vertices, one per record
    g.add_vertices(len(recordNames))
    g.vs['label'] = recordNames

    # Add aToB edges
    edges = []
    labels = []
    for r in self._records.values():
      for (lname, link, weight, dr) in r._genLinkData():
        if (dr == 'bToA'): continue
        src = vertNumbers[r._name]
        dst = vertNumbers[link]
        edges.append((src, dst))
        labels.append(lname + ":" + str(weight))
    g.add_edges(edges)
    g.es['label'] = labels

    # visualize it
    layout = g.layout('kk')
    igraph.plot(g, layout=layout, margin=100, vertex_size=50, vertex_label_size=14)

__NETWORK = Network()
