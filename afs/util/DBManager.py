import datetime
import json
import logging
import string
from types import ListType,DictType,StringType,IntType
from copy import deepcopy

from sqlalchemy import or_, func, desc
import sqlalchemy.orm.session
from sqlalchemy.orm import object_session 

from afs.orm.Historic import historic_tables
from afs.util.AFSError import AFSError
import afs
import afs.model

class DBManager :

    def __init__(self, conf=None) :

        # CONF INIT 
        if conf:
            self._CFG = conf
        else:
            self._CFG = afs.CONFIG

        if not self._CFG.DB_CACHE:
            raise AFSError("DB_CACHE not configured")

        # LOG INIT
        classLogLevel = getattr(self._CFG,"LogLevel_%s" % self.__class__.__name__, "").upper()
        numericLogLevel = getattr(logging,classLogLevel, 0)
        self.Logger=logging.getLogger("afs.util.%s" % self.__class__.__name__)
        self.Logger.setLevel(numericLogLevel)
        self.Logger.debug("initializing %s-Object with conf=%s" % (self.__class__.__name__, conf))
        self.DbSession=afs.DB_SESSION_FACTORY()
	return


    def executeRaw(self, rawsql) :
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
       
    def get_from_cache(self, Class, mustBeUnique=True, fresh_only=True, **where) :
        """
        get an object from the cache.
        returns None if object is not found in cache
        unique is used the same way as in setIntoCache
        """
        query = self.DbSession.query(Class).filter_by(**where)
        if fresh_only == True :
            query = query.filter( Class.db_update_date > ( datetime.datetime.now() -  datetime.timedelta(seconds=int(self._CFG.DB_TIME_TO_CACHE))) )
        cachedObjList = query.all()
        emptyObj = Class()
        for r in cachedObjList :
            r.update_app_repr()
            # the unmapped_attributes_list is not stored in DB, thus add it here explictly.
            r.unmapped_attributes_list=emptyObj.unmapped_attributes_list
            # expunge Obj from Session, we don't want to use it outside
            self.DbSession.expunge(r)
        self.Logger.debug("get_from_cache: got fromDB: %s" % (cachedObjList))
        if mustBeUnique :
            if len(cachedObjList) > 1 :
                raise AFSError("Constraints %s return no unique Object from DB" % where)
            elif len(cachedObjList) == 1 :
                res = cachedObjList[0]
            else :
                res = None
        else :
            if len(cachedObjList) > 0 :
                res = cachedObjList
            else :
                res =  None
        self.Logger.debug("get_from_cache: returning %s" % res)
        return res 

    def get_from_cache_by_list_element(self, Class, Attr, Elem, mustBeUnique=True) :
        """
        use hand-craftet query to search for a single element
        in a json-encoded list.
        """
      
        if type(Elem) == StringType :
            RegEx="\[.*\"{0}\".*\]".format(Elem)
        else :
            RegEx="\[({0}|.*, {0}|{0},.*|.*, {0},.*)\]".format(Elem)
        
        emptyObj=Class()
        self.Logger.debug("get_from_cache_by_list_element: using regexp=%s" % RegEx)
        cachedObjList=self.DbSession.query(Class).filter(Attr.op('regexp')(RegEx)).all()
        if len(cachedObjList) == 0 :
            self.Logger.debug("get_from_cache_by_list_element: returning None")
            return None
        for r in cachedObjList :
            r.update_app_repr()
            # the unmapped_attributes_list is not stored in DB, thus add it here explictly.
            r.unmapped_attributes_list=emptyObj.unmapped_attributes_list
            # expung Obj from Session, we don't want to use it outside
            self.DbSession.expunge(r)
        self.Logger.debug("get_from_cache_by_list_element: returning: %s" % (cachedObjList))
        if mustBeUnique :
            if len(cachedObjList) > 1 :
                raise AFSError("get_from_cache_by_list_element: constraint Elem=%s returns no unique Object from DB" % (Elem))
            elif len(cachedObjList) == 1 :
                return cachedObjList[0]
            else :
                return None
        else :
            return cachedObjList
        return cachedObjList

    def get_from_cache_by_dict_key(self, Class, Attr, Key, mustBeUnique=True) :
        """
        use hand-craftet query to search for a single key
        in a json-encoded dict.
        """
        RegEx='{{.*"{0}":.*}}'.format(Key)
        self.Logger.debug("get_from_cache_by_dict_key: regex=%s" % (RegEx))
        emptyObj=Class()
        cachedObjList=self.DbSession.query(Class).filter(Attr.op('regexp')(RegEx)).all()
        if len(cachedObjList) == 0 :
            self.Logger.debug("get_from_cache_by_dict_key: returning None")
            return None
        for r in cachedObjList :
            r.update_app_repr()
            # the unmapped_attributes_list is not stored in DB, thus add it here explictly.
            r.unmapped_attributes_list=emptyObj.unmapped_attributes_list
            # expung Obj from Session, we don't want to use it outside
            self.DbSession.expunge(r)
        self.Logger.debug("get_from_cache_by_dict_key: returning: %s" % (cachedObjList))
        if mustBeUnique :
            if len(cachedObjList) > 1 :
                raise AFSError("get_from_cache_by_dict_key: constraint Key=%s returns no unique Object from DB" % (Key))
            elif len(cachedObjList) == 1 :
                return cachedObjList[0]
            else :
                return None
        else :
            return cachedObjList
        return cachedObjList

    def get_from_cache_by_dict_value(self, Class, Attr, Value, mustBeUnique=True) :
        """
        use hand-craftet query to search for a single Value
        in a json-encoded dict.
        """
        RegEx='{{.*: "{0}".*}}'.format(Value)
        self.Logger.debug("get_from_cache_by_dict_value: regex=%s" % (RegEx))
        emptyObj=Class()
        cachedObjList=self.DbSession.query(Class).filter(Attr.op('regexp')(RegEx)).all()
        if len(cachedObjList) == 0 :
            self.Logger.debug("get_from_cache_by_dict_value : returning None")
            return None
        for r in cachedObjList :
            r.update_app_repr()
            # the unmapped_attributes_list is not stored in DB, thus add it here explictly.
            r.unmapped_attributes_list=emptyObj.unmapped_attributes_list
            # expung Obj from Session, we don't want to use it outside
            self.DbSession.expunge(r)
        self.Logger.debug("get_from_cache_by_dict_value : returning: %s" % (cachedObjList))
        if mustBeUnique :
            if len(cachedObjList) > 1 :
                raise AFSError("get_from_cache_by_dict_keyValue: constraint Value=%s returns no unique Object from DB" % (Value))
            elif len(cachedObjList) == 1 :
                return cachedObjList[0]
            else :
                return None
        else :
            return cachedObjList
        return cachedObjList

    def get_from_cache_by_dict_key_value_pair(self, Class, Attr, Key, Value, mustBeUnique=True) :
        """
        use hand-craftet query to search for a single Value
        in a json-encoded dict.
        """
        RegEx='{{.*"{0}": "{1}".*}}'.format(Key,Value)
        self.Logger.debug("get_from_cache_by_dict_key_value_pair: regex=%s" % (RegEx))
        emptyObj=Class()
        cachedObjList=self.DbSession.query(Class).filter(Attr.op('regexp')(RegEx)).all()
        if len(cachedObjList) == 0 :
            self.Logger.debug("get_from_cache_by_dict_key_value_pair: returning None")
            return None
        for r in cachedObjList :
            r.unmapped_attributes_list=emptyObj.unmapped_attributes_list
            r.update_app_repr()
            # the unmapped_attributes_list is not stored in DB, thus add it here explictly.
        self.Logger.debug("get_from_cache_by_dict_key_value_pair: returning: %s" % (cachedObjList))
        if mustBeUnique :
            if len(cachedObjList) > 1 :
                raise AFSError("get_from_cache_by_dict_key_value_pair: constraint Key=%s, Value=%s return no unique Object from DB" % (Key,Value))
            elif len(cachedObjList) == 1 :
                return cachedObjList[0]
            else :
                return None
        else :
            return cachedObjList

    def set_into_cache(self, Class, Obj, **unique) :
        """ 
        Store an object into the cache.
        unique is a list of (Attribute-Name = value)-pairs which identifies 
        the object within the DB using filter_by() if Attribute is directly mapped.
        A complex Attribute which is json encoded has to be dealt with differently.
        See setIntoCacheByDictKey,set_into_cache_by_dict_value and set_into_cache_by_list_element for this.
        """ 
        self.Logger.debug("setIntoCache: called with class=%s, Obj=%s, **unique=%s " % (Class, Obj, unique))
        # we have to detach the Obj from the sqlalchemy session, otherwise
        # we mix Obj and mapped_object
        if object_session(Obj) != None : 
            self.DbSession.expunge(Obj)
        self.Logger.debug("setIntoCache: Obj=%s" % Obj)
        # get a mapped object
        mapped_object = self.get_from_cache(Class, fresh_only=False, **unique)
        if mapped_object == None :
            mapped_object = Class()
        updated_obj = self.do_set_into_cache(Obj, mapped_object)
        return self.get_from_cache(Class, fresh_only=False, **unique)

    def set_into_cache_by_dict_value(self, Class, Obj, Attr, Elem) :
        if object_session(Obj) != None : 
            self.DbSession.expunge(Obj)
        # get a mapped object
        mapped_object = self.get_from_cache_by_dict_value(Class, Attr, Elem)
        if mapped_object == None :
            mapped_object = Class()
        updated_obj = self.do_set_into_cache(Obj, mapped_object)
        return self.get_from_cache_by_dict_value(Class, Attr, Elem)

    def set_into_cache_by_list_element(self, Class, Obj, Attr, Elem) :
        if object_session(Obj) != None : 
            self.DbSession.expunge(Obj)
        # get a mapped object
        mapped_object = self.get_from_cache_by_list_element(Class, Attr, Elem)
        if mapped_object == None :
            mapped_object=Class()
        updated_obj = self.do_set_into_cache(Obj, mapped_object)
        return self.get_from_cache_by_list_element(Class, Attr,Elem)


    def obj_has_changed(self, obj, latest_archived_obj) :
        """
        checks if obj is different from latest archived object
        """
        from afs.model.BaseModel import BaseModel
        base_model_attrs = dir(BaseModel())
        model_attributes = dir(obj)
        for attr in model_attributes :
            if attr[0] == "_" : continue
            if attr in base_model_attrs : continue
            if attr == obj : continue
            if not attr in obj.unmapped_attributes_list :
                if getattr(latest_archived_obj, attr) != getattr(obj, attr) :
                    self.Logger.debug("attr %s changed. was :%s is: %s" % (attr, getattr(latest_archived_obj, attr),getattr(obj, attr)) )
                    return True
        return False   
             

    def archive_into_cache(self, mapped_object) :
        """
        archive object into historic class if configuration allows
        """
        self.Logger.debug("Entering archive_into_cache")
        historic_class = afs.model.get_historic_class(mapped_object)
        now = datetime.datetime.now()
        latest_archived_obj= self.DbSession.query(historic_class).filter_by(real_db_id=mapped_object.db_id).order_by(desc(historic_class.db_creation_date)).first()
       

    
        self.Logger.debug("latest=%s\n" % latest_archived_obj)
        if latest_archived_obj == None :
            self.do_archive_obj(mapped_object, now)
            return

        already_archived_objs = self.DbSession.query(historic_class).filter_by(real_db_id=mapped_object.db_id).filter( historic_class.db_creation_date > ( now - datetime.timedelta(minutes=int(self._CFG.DB_HISTORY_MIN_INTERVAL_MINUTES))) ).all()
        if len(already_archived_objs) == 0 :
            if self.obj_has_changed(mapped_object, latest_archived_obj)  :
                self.do_archive_obj(mapped_object, now)
                return
        else :
            self.Logger.debug("Not archiving any object, since we got one already in the last %s minutes." % self._CFG.DB_HISTORY_MIN_INTERVAL_MINUTES)

    def do_archive_obj(self, mapped_object, now) :
            historic_obj = afs.model.get_historic_object(mapped_object)
            if historic_obj.real_db_id != None : # only create history if there was sth there first
                historic_obj.db_creation_date = now
                historic_obj.db_update_date = None
                historic_obj.update_db_repr()
                self.DbSession.merge(historic_obj) 
                self.Logger.debug("do_archive_obj: history to mapped-Obj=%s" % historic_obj)

    def do_set_into_cache(self, Obj, mapped_object) : 
        """
        method to actually push something into the DB_CACHE
        """
        # copy over used Attributes
        self.Logger.debug("do_set_into_cache: got obj=%s" % Obj)
        now = datetime.datetime.now()
        # save mapped-object as-is into historical table.
        # admin need to vacuum once in a while, no automatism here.
        if self._CFG.DB_HISTORY :
            self.archive_into_cache(mapped_object)

        # update mapped-object to store it back to DB
        db_id = mapped_object.db_id
        db_creation_date = mapped_object.db_creation_date
        if db_creation_date == None :
            db_creation_date = now
            db_update_date = None
        else :
            db_update_date = now
        mapped_object = deepcopy(Obj) 
        mapped_object.db_id = db_id
        mapped_object.db_creation_date = db_creation_date
        mapped_object.db_update_date = db_update_date
        self.Logger.debug("do_set_into_cache: copied to mapped-Obj=%s" % mapped_object)
        # update database (json) representations
        mapped_object.update_db_repr()
        self.Logger.debug("do_set_into_cache: got mappedobj=%s" % mapped_object)
        # push it to the DB.
        self.DbSession.merge(mapped_object)  
        self.DbSession.commit()  
        self.Logger.debug("got %s" % mapped_object)
        # remove DB-association of Object ???
        sqlalchemy.orm.session.make_transient(mapped_object)
        self.Logger.debug("do_set_into_cache: returning=%s" % mapped_object)
        return mapped_object
    
    def delete_from_cache(self, Class, **unique):
        """
        Delete Object from cache
        """
        cached_obj = self.get_from_cache(Class, fresh_only=False, **unique)

        if cached_obj :
            self.DbSession.delete(cached_obj)
            self.DbSession.commit()
            return True
        else :
            return False

    def vacuum_history(self, Class, keep_num_days=-1  ) :
        """
        Cleanup historic tables, remove everything older than DB_HISTORY_NUM_DAYS.
        """
        if keep_num_days == -1 :
            keep_num_days = self._CFG.DB_HISTORY_NUM_DAYS

        # delete objects with no db_update_date (should not happen anyway)
        to_be_deleted_objs = self.get_from_cache(Class, db_update_date=None, mustBeUnique=False, fresh_only=False) 
        if to_be_deleted_objs != None :
            for obj in to_be_deleted_objs :
                self.Logger.debug("deleting invalid obj: %s db_id %s" % (obj, obj.db_id) ) 
                self.DbSession.delete(obj)
        to_be_deleted_objs = self.DbSession.query(Class).filter((Class.db_creation_date - datetime.datetime.now()) > datetime.timedelta(days=keep_num_days)).all()
        for obj in to_be_deleted_objs :
                self.Logger.debug("deleting obj: %s db_id %s" % (obj, obj.db_id) )
                self.DbSession.delete(obj)
        self.DbSession.commit()
        return 

    def count(self, Attr, **where) :
        self.Logger.debug("count: Entering with Attr=%s, where=%s" % (Attr, where))
        res = self.DbSession.query(func.count(Attr)).filter_by(**where).scalar()
        self.Logger.debug("count: returning %s" % res)
        return res

    def sum(self, Attr, **where) :
        res = self.DbSession.query(func.sum(Attr)).filter_by(**where).scalar()
        return res
