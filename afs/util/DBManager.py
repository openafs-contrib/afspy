from afs.util.AFSError import AFSError
import string,json,logging
from sqlalchemy import or_,func
import sqlalchemy.orm.session
from sqlalchemy.orm import object_session 
import afs
import afs.model
from types import ListType,DictType,StringType,IntType
from copy import deepcopy
from afs.orm.Historic import historic_tables
import time

class DBManager :

    def __init__(self,conf=None) :

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
        

    def get_from_cache(self, Class, mustBeUnique=True, **where) :
        """
        get an object from the cache.
        returns None if object is not found in cache
        unique is used the same way as in setIntoCache
        """
        query=self.DbSession.query(Class).filter_by(**where)
        cachedObjList = query.all()
        emptyObj = Class()
        for r in cachedObjList :
            r.update_app_repr()
            # the unmapped_attributes_list is not stored in DB, thus add it here explictly.
            r.unmapped_attributes_list=emptyObj.unmapped_attributes_list
            # expung Obj from Session, we don't want to use it outside
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
        mapped_object = self.get_from_cache(Class, **unique)
        if mapped_object == None :
            mapped_object = Class()
        updated_obj = self.do_set_into_cache(Obj, mapped_object)
        return self.get_from_cache(Class, **unique)

    def set_into_cache_by_dict_value(self, Class, Obj, Attr, Elem) :
        if object_session(Obj) != None : 
            self.DbSession.expunge(Obj)
        # get a mapped object
        mapped_object = self.get_from_cache_by_dict_value(Class, Attr, Elem)
        if mapped_object == None :
            mapped_object = Class()
        updated_obj = self.do_set_into_cache(Obj, mapped_object)
        return elf.get_from_cache_by_dict_value(Class, Attr, Elem)

    def set_into_cache_by_list_element(self, Class, Obj, Attr, Elem) :
        if object_session(Obj) != None : 
            self.DbSession.expunge(Obj)
        # get a mapped object
        mapped_object = self.get_from_cache_by_list_element(Class, Attr, Elem)
        if mapped_object == None :
            mapped_object=Class()
        updated_obj = self.do_set_into_cache(Obj, mapped_object)
        return self.get_from_cache_by_list_element(Class, Attr,Elem)

    def do_set_into_cache(self, Obj, mapped_object) : 
        # copy over used Attributes
        self.Logger.debug("do_set_into_cache: got obj=%s" % Obj)
        # save mapped-object as-is into historical table.
        # admin need to vacuum once in a while, no automatism here.
        historic_obj = afs.model.get_historic(mapped_object)
        historic_obj.update_db_repr()
        self.Logger.debug("do_set_into_cache: history to mapped-Obj=%s" % historic_obj)
        self.DbSession.merge(historic_obj) 
        # update mapped-object to store it back to DB
        db_id = mapped_object.db_id
        db_creation_date = mapped_object.db_creation_date
        mapped_object = deepcopy(Obj) 
        mapped_object.db_id = db_id
        mapped_object.db_creation_date = db_creation_date
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
        cached_obj = self.get_from_cache(Class, **unique)

        if cached_obj :
            self.DbSession.delete(cached_obj)
            self.DbSession.commit()
            return True
        else :
            return False

    def vaccuum_cache(self) :
        """
        Cleanup historic tables.
        keep the minimum number of objects DB_HISTORY_NUM_PER_DAY for each day
        young than DB_HISTORY_NUM_DAYS
        """
        now=time.mktime(time.localtime())
        for table in historic_tables :
            self.Logger.debug("vaccuuming table %s" % table)
            if table == "tbl_hist_extvolattr" :
                db_id_str = "vid"
            else :
                db_id_str = "db_id"
            res = self.executeRaw("SELECT %s, db_update_date FROM %s" % (db_id_str, table)).fetchall()
            to_be_deleted = []
            for db_id, db_update_date in res :
                timestamp=time.mktime(time.strptime("%s" % db_update_date, "%Y-%m-%d %H:%M:%S"))
                if timestamp < ( now - afs.CONFIG.DB_HISTORY_NUM_DAYS * 86440 ) :
                    self.Logger.debug("deleting %s" % (db_update_date) ) 
                    to_be_deleted.append(db_id)

            for db_id in to_be_deleted :
                res = self.executeRaw("DELETE FROM %s WHERE %s = %s" % (table, db_id_str, db_id))

            # get all remaining sorted by update_date
           
            res = self.executeRaw("SELECT %s, db_update_date FROM %s order by db_update_date ASC" % (db_id_str, table)).fetchall()

            if len(res) == 0 : continue
                
            db_id, db_update_date = res[0]
            day = ("%s" % db_update_date).split()[0]  
            to_be_deleted = []
            num_this_day = 0
            for db_id, db_update_date in res[1:] :
                if ("%s" % db_update_date).split()[0] == day :
                    num_this_day += 1
                    if num_this_day >= afs.CONFIG.DB_HISTORY_NUM_PER_DAY :
                        to_be_deleted.append(db_id)
                else :
                    day = ("%s" % db_update_date).split()[0] 
                    num_this_day = 0
             
            conn = self._CFG.DB_ENGINE.connect()
            t = conn.begin()
            for db_id in to_be_deleted :
                rawsql =  "DELETE FROM %s WHERE %s=%s" %  (table, db_id_str, db_id) 
                res = conn.execute(rawsql)
            t.commit()
            t.close()

        return 

    def count(self, Attr, **where) :
        self.Logger.debug("count: Entering with Attr=%s, where=%s" % (Attr, where))
        res = self.DbSession.query(func.count(Attr)).filter_by(**where).scalar()
        self.Logger.debug("count: returning %s" % res)
        return res

    def sum(self, Attr, **where) :
        res = self.DbSession.query(func.sum(Attr)).filter_by(**where).scalar()
        return res
