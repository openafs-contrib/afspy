
from types import *

class BaseModel(object):
    
    def __str__(self):
        res = ""
        for attr, value in self.__dict__.iteritems():
            if type(attr) is IntType or type(attr) is StringType or type(attr) is LongType or type(attr) is UnicodeType:
                res += " %s=%s" %(attr, value)
        return res
    
    
    def getDict(self):
        res = {}
        for attr, value in self.__dict__.iteritems():
             if type(attr) is IntType or type(attr) is StringType or type(attr) is LongType or type(attr) is UnicodeType:
                res.append(attr, value)
        return res
        