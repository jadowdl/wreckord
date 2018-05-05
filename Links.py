#!/usr/bin/env python

from Record import Record, RecordLink
from Network import __NETWORK


def _mkLink(link, recordA, recordB, weight):
  # add recordB to recordA as instance of type link.aToBName
  assert not recordA._hasLink(recordB, link.aToBName)
  assert not recordB._hasLink(recordB, link.bToAName)
  RecordLink(recordA, recordB, link, weight)
  __NETWORK._save()


# Represents the abstraction of all links of a type, like "sameAs".
# Every link has a forward type ("aToBName"), a sister backwards
# type ("bToAName"), and a weight.
class Link:
  def __init__(self, aToBName, bToAName):
    self.aToBName = aToBName;
    self.bToAName = bToAName;


  def opposite(self):
    return Link(self.bToAName, self.aToBName)


  def monkeyPatch(self):
    # record.{self.aToBName}(record2) {
    #   _mklink(self, record, record2)
    #   _mklink(self.opposite, record2, record)
    # }
    def aToB(record_self, record2, weight=1.0):
      _mkLink(self, record_self, record2, weight)
    def bToA(record_self, record2, weight=1.0):
      _mkLink(self.opposite(), record_self, record2, weight)

    setattr(Record, self.aToBName, aToB)
    if (self.aToBName is not self.bToAName):
      setattr(Record, self.bToAName, bToA)


__LINKS = [
  Link('sameAs', 'sameAs'),
  Link('kindOf', 'generalizationOf')
]



# ensure uniqueness of link names...
for i in range(0, len(__LINKS)):
  for j in range(i+1, len(__LINKS)):
    assert __LINKS[i].aToBName is not __LINKS[j].aToBName
    assert __LINKS[i].aToBName is not __LINKS[j].bToAName
    assert __LINKS[i].bToAName is not __LINKS[j].aToBName
    assert __LINKS[i].bToAName is not __LINKS[j].bToAName


def __APPLY_LINKS():
  Record.LINK_LOOKUP_MAP = {}
  for l in __LINKS:
    l.monkeyPatch()
    Record.LINK_LOOKUP_MAP[l.aToBName] = l
    Record.LINK_LOOKUP_MAP[l.bToAName] = l
