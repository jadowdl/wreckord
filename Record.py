#!/usr/bin/env python

# (for __NETWORK.save())
from Network import __NETWORK

import POS
import json

_N = __NETWORK # sidestep name manging in the class

# Would have prefered to do this as methods in Record,
# but lo-and-behold "@staticmethod def _unmarshal():" becomes hidden!
class RecordMarshal:
  @staticmethod
  def marshal(record, as_json=True):
    as_dict = {
      "name": record._name,
      "language": record._language,
      "pos": record._pos,
      "links": [{"name": lname, "other_record": link, "weight": weight, "dir": direction}
                for (lname, link, weight, direction) in record._genLinkData()]
    }

    if (as_json):
      return json.dumps(as_dict)
    else:
      return as_dict


  # this is a bit of a hack, because records are global variables.
  # assumes that the relevant records already exist in _N
  # merely mangles entries there, in place.
  @staticmethod
  def unmarshal(data, from_json=False):
    parse = data
    if (from_json):
      parse = json.loads(data)
    r = getattr(_N, parse['name'])
    r._language = parse['language']
    r._pos = parse['pos']
    for link in parse['links']:
      if (link['dir'] == 'bToA'): continue
      r2 = getattr(_N, link['other_record'])
      # LINK_LOOKUP_MAP Created by Links.py
      linkType = Record.LINK_LOOKUP_MAP[link['name']]
      RecordLink(r, r2, linkType, link['weight'])


# TODO - POS, language
class Record:
  def __init__(self, name, language='English', pos=POS.NOUN):
    self._name = name
    self._links = {}
    self._language = language
    self._pos = pos


  def _hasLink(self, record, linkType):
    lookup = None
    try:
      lookup = getattr(self, record._name)
    except: return False

    return isinstance(lookup, RecordLink) and lookup.linkType is linkType


  def _genLinkData(self):
    for link in self._links:
      direction = 'aToB'
      lname = self._links[link]._linkType.aToBName
      if (self is self._links[link]._childRecord):
        direction='bToA'
        lname = self._links[link]._linkType.bToAName
      yield (lname, link, self._links[link].weight, direction)


  def _marshal(self, as_json=True):
    return RecordMarshal.marshal(self, as_json)

  # This totally breaks "repr" format, because it can't be used to recreate the Record;
  # but since Greg will be using this from cmdline, I'm sacrificing correctness for
  # ease of use.  This way you can just enter the Record Name on the repl line and see
  # it.
  def _prettyRepr(self):
    rez  = "Record ["+self._name+"] (" + self._language+":"+self._pos+") \n"
    if len(self._links) == 0:
      rez += "  (Empty, No Links Yet)\n"
    for (lname, link, weight, _) in self._genLinkData():
      rez += "  " +lname + " [" + link + "] (weight=" + str(weight)+")\n"
    return rez


  def __repr__(self):
    # return "RecordMarshal.unmarshal(\"\"\"" +RecordMarshal.marshal(self)+"\"\"\")"
    return self._prettyRepr()


  def __str__(self):
    return RecordMarshal.marshal(self)


# Represents an individual link from record A to record B.
# Don't confuse with 'Link' class in Links.py
class RecordLink:
  def __init__(self, parentRecord, childRecord, linkType, weight):
    self._parentRecord = parentRecord
    self._childRecord = childRecord
    self._linkType = linkType
    self.weight = weight
    setattr(parentRecord, childRecord._name, self)
    parentRecord._links[childRecord._name] = self
    setattr(childRecord, parentRecord._name, self)
    childRecord._links[parentRecord._name] = self


  def deleteLink(self):
    delattr(self._parentRecord, self._childRecord._name)
    del self._parentRecord._links[self._childRecord._name]
    delattr(self._childRecord, self._parentRecord._name)
    del self._childRecord._links[self._parentRecord._name]
    _N._save()
