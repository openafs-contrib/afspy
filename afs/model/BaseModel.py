import datetime,json,logging,sys
from types import *
from afs.exceptions.AfsError import AfsError
import afs

# log-level is set in AfsConfig
Logger=logging.getLogger("afs.model")

class BaseModel(object):
    """
    The mother of all models.
    """

    def setByDict(self,objByDict):      
        """
        fill in object by dict.
        It is an error to try to create new attributes with this method
        It is also an error to pass json representations here.
        """
        Logger.debug("setByDict: got dict=%s" % objByDict)
        # inject ignAttrList is not present, happens in hand-craftet dicts..
        if not objByDict.has_key("ignAttrList") : objByDict["ignAttrList"]=[]
        for attr, value in objByDict.iteritems():
            if not hasattr(self,attr) and not attr in objByDict["ignAttrList"] + ["ignAttrList"]  :
                raise AfsError("Cannot create new attribute '%s' to object '%s'" %(attr, self.__class__.__name__))
            elif attr[-3:] == "_js" :
                raise AfsError("Cannot set json representational attributes here.")
            else :# do not alter DB internal id and creation date
                if attr != "id" and attr != "cdate":
                    setattr(self,attr,value)
        return True

    def updateAppRepr(self) :
        """
        update Complex attributes from their json encoded counterparts
        """
        cmplxAttrs={}
        for attr, value in self.__dict__.iteritems() :
            if attr[-3:]=="_js" :
                cmplxAttrs[attr[:-3]]=json.loads(value)
        for attr,value in cmplxAttrs.iteritems() :
            setattr(self,attr,value)
        return

    def updateDBRepr(self) :
        """
        update the all attributes holding json represenations of complex attributes
        """
        jsonReps={}
        Logger.debug("in updateDBRepr" )
        for attr, value in self.__dict__.iteritems() :
            if attr[0] == "_" : continue
            if not type(value) in [StringType,IntType,LongType,FloatType,BooleanType,datetime.datetime] :
                Logger.debug("attr=%s type(value)=%s" % (attr,type(value)))
                jsonReps["%s_js" % attr] = json.dumps(value)
        for attr,value in jsonReps.iteritems() :
            Logger.debug("setting json rep %s to '%s'" % (attr,value) )
            setattr(self,attr,value)
        return
 
    def copyObj(self, obj):
        """
        copies one object onto another.
        complex attributes are synced with their _js counterparts.
        """
        dict=obj.getDict()
        self.setByDict(dict)
        return
    
    def getJson(self):
        """
        Get a json representation of the model object
        """
        res={}
        for attr,value in self.getDict() :
            if isinstance(value, datetime.datetime):
                res[attr] = json.dumps(value.isoformat('-'))
            elif type(value) in [StringType,IntType,UnicodeType,ListType,DictType,NoneType] : 
                res[attr] = json.dumps(value)
        return res
    
    def getDict(self):
        """
        Get a dictionary representation of the model object.
        json encoded attributes ending in "_js" are not set.
        """
        res = {}
        for attr, value in self.__dict__.iteritems() :
            if attr[0] == "_" : continue
            if attr[-3:]=="_js" : continue
            if isinstance(value, datetime.datetime):
                res[attr] = value.isoformat('-')
            elif type(value) in [StringType,IntType,LongType,FloatType,BooleanType,UnicodeType,DictType,ListType,NoneType] :
                res[attr] = value
            else : # ignore anything else
                Logger.warn("getDict: ignoring attr %s with type(value)=%s" % (attr,type(value)) )
                pass
        Logger.debug("getDict: returning : %s" % res)
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
