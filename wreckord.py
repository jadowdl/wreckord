#!/usr/bin/env python
#
# Main entry point for the library/project.

from Network import __NETWORK
from Record import Record
import re
from Links import __APPLY_LINKS

_ = __NETWORK

def __new(recordName):
  recordName = recordName.upper()
  recordName = re.sub(r'\s', '_', recordName)
  r = Record(recordName)
  print("==== Created Record '" + recordName + "'")
  setattr(__NETWORK, recordName, r)
  globals()[recordName] = r

__APPLY_LINKS()
