import string,json,logging
from afs.exceptions.AfsError import AfsError
from sqlalchemy import or_,func
import sqlalchemy.orm.session
from sqlalchemy.orm import object_session 
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


    def executeRaw(self,rawsql) :
        """
        execute directly a SQL-statement
        """
        self.Logger.debug("executeRaw: statement=%s" % (rawsql))
        conn = self._CFG.DB_ENGINE.connect()
        t = conn.begin()
        try:
            res = conn.execute(rawsql)
            t.commit()
            self.Logger.debug("executeRaw: returning %s rows." % (res.rowcount))
        except:
            self.Logger.warn("executeRaw: statement=%s failed." % (rawsql))
            t.rollback()
            res=None
        t.close()
        return res
        

    def getFromCache(self, Class, mustBeUnique=True, **where) :
        """
        get an object from the cache.
        unique is used the same way as in setIntoCache
        """
        query=self.DbSession.query(Class).filter_by(**where)
        cachedObjList = query.all()
        emptyObj=Class()
        self.Logger.debug("getFromCache: got fromDB: %s" % (cachedObjList))
        for r in cachedObjList :
            r.updateAppRepr()
            # the ignAttrList is not stored in DB, thus add it here explictly.
            r.ignAttrList=emptyObj.ignAttrList
            # expung Obj from Session, we don't want to use it outside
            self.DbSession.expunge(r)
        if mustBeUnique :
            if len(cachedObjList) > 1 :
                raise AfsError("Constraints %s return no unique Object from DB" % where)
            elif len(cachedObjList) == 1 :
                return cachedObjList[0]
            else :
                return None
        else :
            return cachedObjList

    def getFromCacheByListElement(self, Class, Attr, Elem, mustBeUnique=True) :
        """
        use hand-craftet query to search for a single element
        in a json-encoded list.
        """
      
        if type(Elem) == StringType :
            RegEx="\[.*\"{0}\".*\]".format(Elem)
        else :
            RegEx="\[({0}|.*, {0}|{0},.*|.*, {0},.*)\]".format(Elem)
        
        emptyObj=Class()
        self.Logger.debug("getFromCacheByListElement: using regexp=%s" % RegEx)
        cachedObjList=self.DbSession.query(Class).filter(Attr.op('regexp')(RegEx)).all()
        if len(cachedObjList) == 0 :
            self.Logger.debug("getFromCacheByListElement: returning None")
            return None
        for r in cachedObjList :
            r.updateAppRepr()
            # the ignAttrList is not stored in DB, thus add it here explictly.
            r.ignAttrList=emptyObj.ignAttrList
            # expung Obj from Session, we don't want to use it outside
            self.DbSession.expunge(r)
        self.Logger.debug("getFromCacheByListElement: returning: %s" % (cachedObjList))
        if mustBeUnique :
            if len(cachedObjList) > 1 :
                raise AfsError("getFromCacheByListElement: constraint Elem=%s returns no unique Object from DB" % (Elem))
            elif len(cachedObjList) == 1 :
                return cachedObjList[0]
            else :
                return None
        else :
            return cachedObjList
        return cachedObjList

    def getFromCacheByDictKey(self, Class, Attr, Key, mustBeUnique=True) :
        """
        use hand-craftet query to search for a single key
        in a json-encoded dict.
        """
        RegEx='{{.*"{0}":.*}}'.format(Key)
        self.Logger.debug("getFromCacheByDictKey: regex=%s" % (RegEx))
        emptyObj=Class()
        cachedObjList=self.DbSession.query(Class).filter(Attr.op('regexp')(RegEx)).all()
        if len(cachedObjList) == 0 :
            self.Logger.debug("getFromCacheByDictKey: returning None")
            return None
        for r in cachedObjList :
            r.updateAppRepr()
            # the ignAttrList is not stored in DB, thus add it here explictly.
            r.ignAttrList=emptyObj.ignAttrList
            # expung Obj from Session, we don't want to use it outside
            self.DbSession.expunge(r)
        self.Logger.debug("getFromCacheByDictKey: returning: %s" % (cachedObjList))
        if mustBeUnique :
            if len(cachedObjList) > 1 :
                raise AfsError("getFromCacheByDictKey: constraint Key=%s returns no unique Object from DB" % (Key))
            elif len(cachedObjList) == 1 :
                return cachedObjList[0]
            else :
                return None
        else :
            return cachedObjList
        return cachedObjList

    def getFromCacheByDictValue(self, Class, Attr, Value, mustBeUnique=True) :
        """
        use hand-craftet query to search for a single Value
        in a json-encoded dict.
        """
        RegEx='{{.*: "{0}".*}}'.format(Value)
        self.Logger.debug("getFromCacheByDictValue: regex=%s" % (RegEx))
        emptyObj=Class()
        cachedObjList=self.DbSession.query(Class).filter(Attr.op('regexp')(RegEx)).all()
        if len(cachedObjList) == 0 :
            self.Logger.debug("getFromCacheByDictValue : returning None")
            return None
        for r in cachedObjList :
            r.updateAppRepr()
            # the ignAttrList is not stored in DB, thus add it here explictly.
            r.ignAttrList=emptyObj.ignAttrList
            # expung Obj from Session, we don't want to use it outside
            self.DbSession.expunge(r)
        self.Logger.debug("getFromCacheByDictValue : returning: %s" % (cachedObjList))
        if mustBeUnique :
            if len(cachedObjList) > 1 :
                raise AfsError("getFromCacheByDictKeyValue: constraint Value=%s returns no unique Object from DB" % (Value))
            elif len(cachedObjList) == 1 :
                return cachedObjList[0]
            else :
                return None
        else :
            return cachedObjList
        return cachedObjList

    def getFromCacheByDictKeyValuePair(self, Class, Attr, Key, Value, mustBeUnique=True) :
        """
        use hand-craftet query to search for a single Value
        in a json-encoded dict.
        """
        RegEx='{{.*"{0}": "{1}".*}}'.format(Key,Value)
        self.Logger.debug("getFromCacheByDictKeyValuePair: regex=%s" % (RegEx))
        emptyObj=Class()
        cachedObjList=self.DbSession.query(Class).filter(Attr.op('regexp')(RegEx)).all()
        if len(cachedObjList) == 0 :
            self.Logger.debug("getFromCacheByDictKeyValuePair: returning None")
            return None
        for r in cachedObjList :
            r.updateAppRepr()
            # the ignAttrList is not stored in DB, thus add it here explictly.
            r.ignAttrList=emptyObj.ignAttrList
        self.Logger.debug("getFromCacheByDictKeyValuePair: returning: %s" % (cachedObjList))
        if mustBeUnique :
            if len(cachedObjList) > 1 :
                raise AfsError("getFromCacheByDictKeyValuePair: constraint Key=%s, Value=%s return no unique Object from DB" % (Key,Value))
            elif len(cachedObjList) == 1 :
                return cachedObjList[0]
            else :
                return None
        else :
            return cachedObjList

    def setIntoCache(self,Class,Obj,**unique) :
        """ 
        Store an object into the cache.
        unique is a list of (Attribute-Name = value)-pairs which identifies 
        the object within the DB using filter_by() if Attribute is directly mapped.
        A complex Attribute which is json encoded has to be dealt with differently.
        See setIntoCacheByDictKey,setIntoCacheByDictValue and setIntoCacheByListElement for this.
        """ 
        self.Logger.debug("setIntoCache: called with class=%s, Obj=%s, **unique=%s " % (Class, Obj, unique))
        # we have to detach the Obj from the sqlalchemy session, otherwise
        # we mix Obj and mappedObj
        if object_session(Obj) != None : 
            self.DbSession.expunge(Obj)
        self.Logger.debug("setIntoCache: Obj=%s" % Obj)
        # get a mapped object
        mappedObj = self.getFromCache(Class,**unique)
        if mappedObj == None :
            mappedObj=Class()
        return self.do_setIntoCache(Obj,mappedObj)

    def setIntoCacheByDictValue(self,Class,Obj,Attr,Elem) :
        if object_session(Obj) != None : 
            self.DbSession.expunge(Obj)
        # get a mapped object
        mappedObj = self.getFromCacheByDictValue(Class,Attr,Elem)
        if mappedObj == None :
            mappedObj=Class()
        return self.do_setIntoCache(Obj,mappedObj)

    def setIntoCacheByListElement(self,Class, Obj, Attr, Elem) :
        if object_session(Obj) != None : 
            self.DbSession.expunge(Obj)
        # get a mapped object
        mappedObj = self.getFromCacheByDictValue(Class,Attr,Elem)
        return self.do_setIntoCache(Obj,mappedObj)

    def do_setIntoCache(self,Obj,mappedObj) : 
        # copy over used Attributes
        self.Logger.debug("do_setIntoCache: got obj=%s" % Obj)
        mappedObj.copyObj(Obj) # copyObj is defined in BaseModel 
        self.Logger.debug("do_setIntoCache: copied to mapped-Obj=%s" % mappedObj)
        # update database (json) representations
        mappedObj.updateDBRepr()
        self.Logger.debug("do_setIntoCache: got mappedobj=%s" % mappedObj)
        # push it to the DB.
        self.DbSession.merge(mappedObj)  
        self.DbSession.commit()  
        self.Logger.debug("got %s" % mappedObj)
        # remove DB-association of Object ???
        sqlalchemy.orm.session.make_transient(mappedObj)
        self.Logger.debug("do_setIntoCache: returning=%s" % mappedObj)
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
