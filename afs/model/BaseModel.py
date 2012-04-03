import datetime
from types import *
from afs.exceptions.AfsError import AfsError

class BaseModel(object):
    """
    The mother of all models.
    """
    
    def setByDict(self,objByDict):      
        """
        fill in object by dict.
        It is an error to try to create new attributes.with this method
        """
        for key, value in objByDict.iteritems():
            if not hasattr(self,key) :
                raise AfsError("Cannot create new attribute '%s' to object '%s'" %(key, self.__class__.__name__))
            # do not alter DB internal id and creation date
            if key != "id" and key != "cdate":
                setattr(self,key,value)
          
    def copyObj(self, obj):
        self.setByDict(obj.getDict())
        return
    
    def getJson(self):
        """
        Get a dictionary representation of the model object
        """
        res = {}
        for attr, value in self.__dict__.iteritems():
             if isinstance(value, datetime.datetime):
                res[attr] = value.isoformat('-')
             elif isinstance(value, str) or isinstance(value, long) or isinstance(value,unicode) or isinstance(value, int):
                  res[attr] = value
        return res
    
    def getDict(self):
        """
        Get a dictionary representation of the model object
        """
        res = {}
        for attr, value in self.__dict__.iteritems():
            if isinstance(value, str) or isinstance(value, long) or isinstance(value,unicode) or isinstance(value, int) or isinstance(value, datetime.datetime):
                  res[attr] = value
        return res
    
    def __repr__(self):
        """
        Get a string representation of the model object.
        no python built-ins nor BaseModel stuff
        """
        BaseModelAttributes=dir(BaseModel())
        repr="<%s(" % self.__class__.__name__
        ModelAttributes=dir(self)
        for a in ModelAttributes :
            if a in BaseModelAttributes : continue
            repr += "%s=%s, " % (a, eval("self.%s" % a))
        repr += ")>"
        return repr
