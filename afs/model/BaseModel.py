
from types import *

class BaseModel(object):
    """
    The mother of all models.
    """
    def __str__(self):
        """
        Get a string representation of the model object
        """
        res = ""
        for attr, value in self.__dict__.iteritems():
            if type(attr) is IntType or type(attr) is StringType or type(attr) is LongType or type(attr) is UnicodeType:
                res += " %s=%s" %(attr, value)
        return res
    
    
    def setValues(self,list):      
        for key, value in list.iteritems():
            setattr(self,key,value)
    
    
    def getDict(self):
        """
        Get a dictionary representation of the model object
        """
        res = {}
        for attr, value in self.__dict__.iteritems():
             if type(attr) is IntType or type(attr) is StringType or type(attr) is LongType or type(attr) is UnicodeType:
                res.append(attr, value)
             elif isinstance(attr, datetime.datetime):
                 pass
             
        return res
        
    