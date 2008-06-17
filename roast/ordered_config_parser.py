from ConfigParser import RawConfigParser

from roast import odict

class OrderedRawConfigParser(RawConfigParser):
    def __init__(self, *a, **kw):
        RawConfigParser.__init__(self, *a, **kw)
        self._sections = odict.odict()
