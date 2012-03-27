import datetime
from types import *
from afs.exceptions.AfsError import AfsError

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
            if type(value) is IntType or type(value) is StringType or type(value) is LongType or type(value) is UnicodeType:
                res += " %s=%s \n" % ( attr, value)
            elif type(value) is ListType :
                res += "%s= [\n" % attr
                for i in range(len(value)) :
                    res += "\t %s \n" %(value[i])
                res += "]\n"
        return res
    
    def setByDict(self,objByDict):      
        """
        fill in object by dict.
        It is an error to try to create new attributes.with this method
        """
        for key, value in objByDict.iteritems():
            if not hasattr(self,key) :
                raise AfsError("Cannot create new attribute '%s' to object '%s'" %(key, self.__class__.__name__))
            if key != "id" and key != "cdate":
                setattr(self,key,value)
          
    def copyObj(self, obj):
        self.setByDict(obj.getDict())        
    #FIXME
    #def update(self,obj):
    #    for attr, value in obj.__dict__.iteritems():
    #        
    #        if (type(attr) is IntType or type(attr) is StringType or type(attr) is LongType or type(attr) is UnicodeType\
    #            or isinstance(attr, datetime.datetime) ):
    #            print attr
    #            if attr != "id":
    #                setattr(self,attr,value)
    
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
        
    
