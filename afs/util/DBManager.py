import string,json,logging
from afs.exceptions.AfsError import AfsError
from sqlalchemy import or_,func
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
        self.Logger=logging.getLogger("afs.util.%s" % self.__class__.__name__)
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
        cachedObjList = query.all()
        emptyObj=Class()
        for c in cachedObjList :
            c.updateAppRepr()
            # the ignAttrList is not stored in DB, thus add it here explictly.
            c.ignAttrList=emptyObj.ignAttrList
        if mustBeunique :
            if len(cachedObjList) > 1 :
                raise AfsError("Constraints %s return no unique Object from DB" % unique)
            elif len(cachedObjList) == 1 :
                return cachedObjList[0]
            else :
                return None
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
        
        emptyObj=Class()
        self.Logger.debug("getFromCacheByListElement, regex is : %s" % (RegEx))
        resObjs=self.DbSession.query(Class).filter(Attr.op('regexp')(RegEx)).all()
        for r in resObjs :
            r.updateAppRepr()
            # the ignAttrList is not stored in DB, thus add it here explictly.
            r.ignAttrList=emptyObj.ignAttrList
        return resObjs

    def getFromCacheByDictKey(self,Class,Attr,Elem) :
        """
        use hand-craftet query to search for a single key
        in a json-encoded dict.
        """
        RegEx="\{.*\"{0}\"\s+:.*\}".format(Elem)
        emptyObj=Class()
        resObjs=self.DbSession.query(Class).filter(Attr.op('regexp')(RegEx)).all()
        for r in resObjs :
            r.updateAppRepr()
            # the ignAttrList is not stored in DB, thus add it here explictly.
            r.ignAttrList=emptyObj.ignAttrList
        return resObjs

    def getFromCacheByDictValue(self,Class,Attr,Elem) :
        """
        use hand-craftet query to search for a single Value
        in a json-encoded dict.
        """
        RegEx="\{.*:\s+\"{0}\".*\}".format(Elem)
        emptyObj=Class()
        resObjs=self.DbSession.query(Class).filter(Attr.op('regexp')(RegEx)).all()
        for r in resObjs :
            r.updateAppRepr()
            # the ignAttrList is not stored in DB, thus add it here explictly.
            r.ignAttrList=emptyObj.ignAttrList
        return resObjs

    def setIntoCache(self,Class,Obj,uniqType="",**unique) :
        """ 
        Store an object into the cache.
        unique is a list of (Attribute-Name = value)-pairs which identifies 
        the object within the DB using filter_by() if Attribute is directly mapped.
        A complex Attribute which is json encoded has to be dealt with differently.
        See setIntoCacheByDictKey,setIntoCacheByDictValue and setIntoCacheByListElement for this.
        """ 
        self.Logger.debug("setInto Cache: called with class=%s, Obj=%s, **unique=%s " % (Class,Obj,unique))
        # get a mapped object
        mappedObj = self.getFromCache(Class,**unique)
        if mappedObj == None :
            mappedObj=Class()
        self.Logger.debug("got %s" % mappedObj)
        return self.do_setIntoCache(Obj,mappedObj)

    def setFromCacheByDictValue(self,Class,Obj,Attr,Elem) :
        # get a mapped object
        mappedObj = getFromCacheByDictValue(Class,Attr,Elem)
        self.Logger.debug("got %s" % mappedObj)
        return self.do_setIntoCache(Obj,mappedObj)

    def setIntoCacheByListElement(self,Class, Obj, Attr, Elem) :
        # get a mapped object
        mappedObj = getFromCacheByDictValue(Class,Attr,Elem)
        self.Logger.debug("got %s" % mappedObj)
        return self.do_setIntoCache(Obj,mappedObj)

    def do_setIntoCache(self,Obj,mappedObj) : 
        # copy over used Attributes
        self.Logger.debug("got obj=%s" % Obj)
        mappedObj.copyObj(Obj) # copyObj is defined in BaseClass 
        self.Logger.debug("copied to mapped-Obj=%s" % mappedObj)
        # update database (json) representations
        mappedObj.updateDBRepr()
        self.Logger.debug("got %s" % mappedObj)
        # push it to the DB.
        self.DbSession.merge(mappedObj)  
        self.DbSession.commit()  
        self.Logger.debug("got %s" % mappedObj)
        # remove DB-association of Object ???
        sqlalchemy.orm.session.make_transient(mappedObj)
        self.Logger.debug("returning=%s" % mappedObj)
        return mappedObj
    
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

    def count(self,Attr,**where) :
        self.Logger.debug("count: Entering with Attr=%s, where=%s" % (Attr,where))
        res = self.DbSession.query(func.count(Attr)).filter_by(**where).scalar()
        self.Logger.debug("count: returning %s" % res)
        return res

    def sum(self,Attr,**where) :
        res = self.DbSession.query(func.sum(Attr)).filter_by(**where).scalar()
        return res
