import string,json,logging
from afs.exceptions.AfsError import AfsError
from sqlalchemy import or_
import sqlalchemy.orm.session
import afs
from types import ListType,DictType,StringType,IntType

class DBManager :

    def __init__(self,conf=None) :

        # CONF INIT 
        if conf:
            self._CFG = conf
        else:
            self._CFG = afs.defaultConfig

        if not self._CFG.DB_CACHE:
            raise AfsError("DB_CACHE not configured")

        # LOG INIT
        classLogLevel = getattr(afs.defaultConfig,"LogLevel_%s" % self.__class__.__name__, "").upper()
        numericLogLevel = getattr(logging,classLogLevel, 0)
        self.Logger=logging.getLogger("afs.service.%s" % self.__class__.__name__)
        self.Logger.setLevel(numericLogLevel)
        self.Logger.debug("initializing %s-Object with conf=%s" % (self.__class__.__name__, conf))
        self.DbSession=afs.DbSessionFactory()
	return

    def getFromCache(self, Class, mustBeunique=True,**where) :
        """
        get an object from the cache.
        unique is used the same way as in setIntoCache
        """
        query=self.DbSession.query(Class).filter_by(**where)
        self.Logger.debug("getFromCache, statement is : %s" % query.cte())
        cachedObjList = query.all()
        for c in cachedObjList :
            c.updateComplexAttrs()
        if mustBeunique :
            if len(cachedObjList) > 1 :
                raise AfsError("Constraints %s return no unique Object from DB" % unique)
            elif len(cachedObjList) == 1 :
                return cachedObjList[0]
            else :
                return Class()
        else :
            return cachedObjList

    def getFromCacheByListElement(self,Class,Attr,Elem) :
        """
        use hand-craftet query to search for a single element
        in a json-encoded list.
        """
        if type(Elem) == StringType :
            RegEx="\[.*\"{0}\".*\]".format(Elem)
        else :
            RegEx="\[({0}|.*,{0}|{0},.*|.*,{0},.*)\]".format(Elem)
        
        self.Logger.debug("getFromCacheByListElement, regex is : %s" % (RegEx))
        resObjs=self.DbSession.query(Class).filter(Attr.op('regexp')(RegEx)).all()
        for r in resObjs :
            r.updateComplexAttrs()
        return resObjs

    def getFromCacheByDictKey(self,Class,Attr,Elem) :
        """
        use hand-craftet query to search for a single key
        in a json-encoded dict.
        """
        RegEx="\{.*\"{0}\"\s+:.*\}".format(Elem)
        resObjs=self.DbSession.query(Class).filter(Attr.op('regexp')(RegEx)).all()
        for r in resObjs :
            r.updateComplexAttrs()
        return resObjs

    def getFromCacheByDictValue(self,Class,Attr,Elem) :
        """
        use hand-craftet query to search for a single Value
        in a json-encoded dict.
        """
        RegEx="\{.*:\s+\"{0}\".*\}".format(Elem)
        resObjs=self.DbSession.query(Class).filter(Attr.op('regexp')(RegEx)).all()
        for r in resObjs :
            r.updateComplexAttrs()
        return resObjs

    def getFromJoinwithFilter(self,ClassA,AttrA,ClassB,AttrB,**where) :
        query=self.DbSession.query(ClassA).join((ClassB, AttrA==AttrB)).filter_by(**where).all()
        return

    def setIntoCache(self,Class,Obj,**unique) :
        """ 
        Store an object into the cache.
        unique is a list of (Attribute-Name = value)-pairs which identifies 
        the object within the DB using filter_by() if Attribute is directly mapped.
        A complex Attribute which is json encoded has to be dealt with differently.
        See getFromCacheByDictKey,getFromCacheByDictValue and getFromCacheByListElement for this.
        up to now, we cannot store an object uniquified by an complex(json-encoded) attribute.
        """ 
        # get a mapped object
        cachedObj = self.getFromCache(Class,**unique)
        # copy over used Attributes
        cachedObj.copyObj(Obj) # copyObj is defined in BaseClass 
        # update json representations
        cachedObj.updateJSONReps()
        # push it to the DB.
        cachedObj=self.DbSession.merge(cachedObj)  
        self.DbSession.commit()  
        # remove DB-association of Object ???
        cachedObj=sqlalchemy.orm.session.make_transient(cachedObj)
        return cachedObj
    
    def deleteFromCache(self,Class,**unique):
        """
        Delete Object from cache
        """
        cachedObj = self.getFromCache(Class,**unique)

        if cachedObj :
            self.DbSession.delete(cachedObj)
            self.DbSession.commit()
            return True
        else :
            return False

