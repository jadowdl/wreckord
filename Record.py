import json

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


  def _hasLink(self, record, linkType):
    lookup = None
    try:
      lookup = getattr(self, record._name)
    except: return False

    return isinstance(lookup, RecordLink) and lookup.linkType is linkType


  def __repr__(self):
    return "RecordMarshal.unmarshal(\"\"\"" +RecordMarshal.marshal(self)+"\"\"\")"


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
    setattr(childRecord, parentRecord._name, self)


  def deleteLink(self):
    delattr(self._parentRecord, self._childRecord._name)
    delattr(self._childRecord, self._parentRecord._name)
