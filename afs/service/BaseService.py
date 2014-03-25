import inspect
import logging
import threading

from afs.util.AFSError import AFSError

import afs
import sys

class BaseService(object):
    """
    Provides implementation for basic methods for all Service.
    """
    
    def __init__(self,conf=None, DAOList=[]):
        
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
        self.Logger.debug("initializing %s-Object with conf=%s" % (self.__class__.__name__, conf))      
        
        # DB INIT 
        if self._CFG.DB_CACHE :
            from afs.util.DBManager import DBManager
            self.DBManager=DBManager()
        else : # this is a simple object raising an error if called.
            from afs.util.NODBManager import NODBManager    
            self.DBManager=NODBManager()
        
        # DAO INIT 
        if self._CFG.DAOImplementation == "childprocs" :
            for dao in DAOList :
                if dao == "vl":
                    from afs.dao.VLDBDAO import VLDBDAO
                    self._vlDAO  = VLDBDAO()
                elif dao == "vol" :
                    from afs.dao.VolumeDAO import VolumeDAO 
                    self._volDAO = VolumeDAO()
                elif dao == "BosServer" :
                    from afs.dao.BosServerDAO import BosServerDAO
                    self._bosserver_dao = BosServerDAO()
                elif dao == "fs" :
                    from afs.dao.FileServerDAO import FileServerDAO
                    self._fsDAO = FileServerDAO()
                elif dao == "rx" :
                    from afs.dao import RXPeerDAO
                    self._rxDAO=RXPeerDAO.RXPeerDAO()
                elif dao == "ubik" :
                    from afs.dao import UbikPeerDAO
                    self._ubikDAO=UbikPeerDAO.UbikPeerDAO()
                else :
                    raise AFSError("internal Error. invalid DAO '%s' requested" % dao)
        else :
            raise AFSError("internal Error. DAO-implementation '%s' not available" % self._CFG.DAOImplementation)


        # Async INIT
        # list of active threads in this service
        self.active_tasks={}
        self.task_results={}
  
    def wait_for_task(self, task_ident)  :
        self.active_tasks[task_ident].join()
        return
 
    def get_task_result(self, task_ident) :
        return self.task_results.pop(task_ident)


def task_wrapper(method) :
    """
    This decorator is meant for either calling a method directly 
    or execute it in a different thread.
    """

    def wrapped(self, *args, **kwargs): 
        """actual wrapper code""" 

        if not kwargs.has_key("async") :
            kwargs["async"] = True

        async = kwargs["async"]

        # get cmdlist and parsefunction from method
        # parse_fct is parsing the output of the executed function
        # ParseInfo are any info the parse_fct requires beside ret,
        # outout and outerr 
        parse_parameterlist = {"args" : args, "kwargs" : kwargs } 
        argspec = inspect.getargspec(method)
         
        self.Logger.debug("argspec=%s" % (argspec,))

        count = 0
        if argspec[3] != None : 
            for key in argspec[0][-len(argspec[3]):] :
                self.logger.debug("checking argspec key=%s" % key)
                value = argspec[3][count]
                self.Logger.debug("value=%s" % value)
                count += 1
                if not parse_parameterlist["kwargs"].has_key(key) :
                    parse_parameterlist["kwargs"][key] = value

        self.Logger.debug("args=%s" % (args,))
  
        if async :
            this_thread = threading.Thread(target=method, args=(self, ) + args, kwargs=kwargs)
            this_thread.start()
            self.active_tasks[this_thread.ident]=this_thread
            return this_thread.ident
        else :
            return method(self, *args, **kwargs)
    return wrapped
