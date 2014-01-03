import logging

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
