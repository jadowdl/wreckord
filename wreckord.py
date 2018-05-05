#!/usr/bin/env python
#
# Main entry point for the library/project.

from Network import __NETWORK, DUMP_VERSION
from Record import Record, RecordMarshal
import re
from Links import __APPLY_LINKS
import POS
import json

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


# load from disk.
def __load(from_file='contextNet.json'):
  data = json.load(open(from_file, 'r'))
  # TODO - deal with version changes...
  assert data['DUMP_VERSION'] == DUMP_VERSION

  # 1 - get all the record names stubbed
  for r in data['records']:
    __new(r['name'])

  # 2 - unmarshal each individually.
  for r in data['records']:
    RecordMarshal.unmarshal(r)


__load()
