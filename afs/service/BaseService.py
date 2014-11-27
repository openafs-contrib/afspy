#import inspect
import logging
import random
import string
import threading

from afs.util.AFSError import AFSError

import afs
import sys

class BaseService(object):
    """
    Provides implementation for basic methods for all Service.
    """
    
    def __init__(self, conf=None, LLAList=[]):
        
        # CONF INIT
        if conf:
            self._CFG = conf
        else:
            self._CFG = afs.CONFIG
        
        # LOG INIT
        classLogLevel = getattr(self._CFG,"LogLevel_%s" % self.__class__.__name__, "").upper()
        numericLogLevel = getattr(logging,classLogLevel, 0)
        self.Logger=logging.getLogger("afs.service.%s" % self.__class__.__name__)
        self.Logger.setLevel(numericLogLevel)
        self.Logger.debug("initializing %s-Object with conf=%s" % (self.__class__.__name__, self._CFG))
        
        # DB INIT 
        if self._CFG.DB_CACHE :
            from afs.util.DBManager import DBManager
            self.DBManager=DBManager()
        else : # this is a simple object raising an error if called.
            from afs.util.NODBManager import NODBManager    
            self.DBManager=NODBManager()
        
        # LLA INIT 
        for lla in LLAList :
            if lla == "vl":
                from afs.lla.VLDBLLA import VLDBLLA
                self._vlLLA  = VLDBLLA()
            elif lla == "vol" :
                from afs.lla.VolServerLLA import VolServerLLA
                self._volLLA = VolServerLLA()
            elif lla == "BosServer" :
                from afs.lla.BosServerLLA import BosServerLLA
                self._bosserver_lla = BosServerLLA()
            elif lla == "fs" :
                from afs.lla.FileServerLLA import FileServerLLA
                self._fsLLA = FileServerLLA()
            elif lla == "rx" :
                from afs.lla import RXPeerLLA
                self._rxLLA=RXPeerLLA.RXPeerLLA()
            elif lla == "ubik" :
                from afs.lla import UbikPeerLLA
                self._ubikLLA=UbikPeerLLA.UbikPeerLLA()
            else :
                raise AFSError("internal Error. invalid LLA '%s' requested" % lla)


        # Async INIT
        # list of active threads in this service
        self.active_tasks={}
        self.task_results={}
  
    def wait_for_task(self, task_name)  :
        self.Logger.debug("task_results=%s" % self.task_results)
        self.active_tasks[task_name].join()
        return
 
    def get_task_result(self, task_name) :
        self.Logger.debug("task_results=%s" % self.task_results)
        return self.task_results.pop(task_name)

    def do_return(self, thread_name, result) :
        """
        Either just return the result or write it into self.task_results, 
        depending on if we are async or not.
        """
        if thread_name == "" :
            return result
        else :
            self.task_results[thread_name] = result
            return thread_name

    def get_thread_name(self) :
        """
        return a new unique thread-name
        """
        new_name = ""
        while new_name == "" or new_name in self.active_tasks :
            new_name = ""
            i = 0
            while ( i < 8 ) :
                new_name += random.choice(string.letters + string.digits)
                i += 1
        return new_name 

    def get_archived(self, historic_class, earliest=None, latest=None, limit=-1, **filter_dict) :
        """
        mapped_object has to be declared in the specific service itself.
        return list of mapped objects from the archive
        """
        query = self.DBManager.DbSession.query(historic_class).filter_by(**filter_dict)
        if earliest != None :
            query = query.filter( historic_class.db_creation_date > earliest) 
        if latest != None :
            query = query.filter( historic_class.db_creation_date < latest) 
        if limit == -1 :
            archived_objs = query.all()
        else :
            archived_objs = query.limit(limit)
        return archived_objs 

def task_wrapper(method) :
    """
    This decorator is meant for either calling a method directly 
    or execute it in a different thread.
    """

    def wrapped(self, *args, **kwargs): 
        """actual wrapper code""" 

        if not kwargs.has_key("async") :
            kwargs["async"] = False

        async = kwargs["async"]

        # get cmdlist and parsefunction from method
        # parse_fct is parsing the output of the executed function
        # ParseInfo are any info the parse_fct requires beside ret,
        # outout and outerr 
        #parse_parameterlist = {"args" : args, "kwargs" : kwargs } 
        #argspec = inspect.getargspec(method)
         
        #self.Logger.debug("argspec=%s" % (argspec,))

        #count = 0
        #if argspec[3] != None : 
        #    for key in argspec[0][-len(argspec[3]):] :
        #        self.Logger.debug("checking argspec key=%s" % key)
        #        value = argspec[3][count]
        #        self.Logger.debug("value=%s" % value)
        #        count += 1
        #        if not parse_parameterlist["kwargs"].has_key(key) :
        #            parse_parameterlist["kwargs"][key] = value

        self.Logger.debug("args=%s" % (args,))
        self.Logger.debug("kwargs=%s" % (kwargs,))
  
        if async :
            this_thread_name = self.get_thread_name()
            kwargs["_thread_name"] = this_thread_name
            this_thread = threading.Thread(name=this_thread_name, target=method, args=(self, ) + args, kwargs=kwargs)
            this_thread.start()
            self.active_tasks[this_thread_name]=this_thread
            return this_thread_name
        else :
            return method(self, *args, **kwargs)
    return wrapped
