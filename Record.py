import json

# for __NETWORK.save()
from Network import __NETWORK
_N = __NETWORK # sidestep name manging in the class

# Would have prefered to do this as methods in Record,
# but lo-and-behold "@staticmethod def _unmarshal():" becomes hidden!
class RecordMarshal:
  @staticmethod
  def marshal(record):
    return json.dumps({"name": record._name})


  @staticmethod
  def unmarshal(str):
    parse = json.loads(str)
    return Record(parse['name'])


# TODO - POS, language
class Record:
  def __init__(self, name):
    self._name = name
    self._links = {}


  def _hasLink(self, record, linkType):
    lookup = None
    try:
      lookup = getattr(self, record._name)
    except: return False

    return isinstance(lookup, RecordLink) and lookup.linkType is linkType


  # This totally breaks "repr" format, because it can't be used to recreate the Record;
  # but since Greg will be using this from cmdline, I'm sacrificing correctness for
  # ease of use.  This way you can just enter the Record Name on the repl line and see
  # it.
  def _prettyRepr(self):
    rez  = "Record ["+self._name+"]: \n"
    if len(self._links) == 0:
      rez += "  (Empty, No Links Yet)\n"
    for link in self._links:
      lname = self._links[link]._linkType.aToBName
      if (self is self._links[link]._childRecord):
        lname = self._links[link]._linkType.bToAName
      rez += "  " +lname + " [" + link + "]\n"
    return rez


  def __repr__(self):
    # return "RecordMarshal.unmarshal(\"\"\"" +RecordMarshal.marshal(self)+"\"\"\")"
    return self._prettyRepr()


  def __str__(self):
    return RecordMarshal.marshal()


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
