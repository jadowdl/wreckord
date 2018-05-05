#!/usr/bin/env python
#
# Main entry point for the library/project.

from Network import __NETWORK
from Record import Record
import re
from Links import __APPLY_LINKS
import POS

_ = __NETWORK

def __new(recordName, language='English', pos=POS.NOUN):
  recordName = recordName.upper()
  recordName = re.sub(r'\s', '_', recordName)
  if __NETWORK._hasRecord(recordName):
    print ("Could Not Create Record \"" + recordName + "\": already exists")
    return
  r = Record(recordName, language=language, pos=pos)
  print("==== Created Record '" + recordName + "'")
  __NETWORK._addRecord(r)
  globals()[recordName] = r

__APPLY_LINKS()


def __save():
  __NETWORK._save()


# TODO - load from disk.
# 1 - get all the record names stubbed
# 2 - unmarshal each individually.
# 3 - deal with version changes...
def __load():
  pass


__load()
