
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
                res += " %s=%s \n" %(attr, value)
        return res
    
    
    def setByDict(self,objByDict):      
        for key, value in objByDict.iteritems():
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
    
    
    def getDict(self):
        """
        Get a dictionary representation of the model object
        """
        res = {}
        for attr, value in self.__dict__.iteritems():
             if type(attr) is IntType or type(attr) is StringType or type(attr) is LongType or type(attr) is UnicodeType:
                res[attr] = value
             elif isinstance(attr, datetime.datetime):
                res[attr] = value.isoformat('-')
             
        return res
        
    