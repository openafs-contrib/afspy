import logging

from afs.exceptions.AfsError import AfsError

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
                    from afs.dao.VLDbDAO import VLDbDAO
                    self._vlDAO  = VLDbDAO()
                elif dao == "vol" :
                    from afs.dao.VolumeDAO import VolumeDAO 
                    self._volDAO = VolumeDAO()
                elif dao == "osdvol" :
                    from afs.dao.OSDVolumeDAO import OSDVolumeDAO 
                    self._osdvolDAO = OSDVolumeDAO()
                elif dao == "bnode" :
                    from afs.dao.BNodeDAO import BNodeDAO
                    self._bnodeDAO = BNodeDAO()
                elif dao == "fs" :
                    from afs.dao.FileServerDAO import FileServerDAO
                    self._fsDAO = FileServerDAO()
                elif dao == "osdfs" :
                    from afs.dao.OSDFileServerDAO import OSDFileServerDAO 
                    self._osdfsDAO = OSDFileServerDAO()
                elif dao == "rx" :
                    from afs.dao import RXPeerDAO
                    self._rxDAO=RXPeerDAO.RXPeerDAO()
                elif dao == "ubik" :
                    from afs.dao import UbikPeerDAO
                    self._ubikDAO=UbikPeerDAO.UbikPeerDAO()
                elif dao == "dns" :
                    from afs.dao import DNSconfDAO
                    self._dnsDAO=DNSconfDAO.DNSconfDAO()
                else :
                    raise AfsError("internal Error. invalid DAO '%s' requested" % dao)
        else :
            raise AfsError("internal Error. DAO-implementation '%s' not available" % self._CFG.DAOImplementation)
