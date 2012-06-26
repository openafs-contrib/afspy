import logging

from afs.exceptions.AfsError import AfsError
from DBCacheService import DBCacheService

import afs

class BaseService(object):
    """
    Provides implementation for basic methods for all Service.
    """
    
    def __init__(self,conf=None, DAOList=[]):
        
        # CONF INIT
        if conf:
            self._CFG = conf
        else:
            self._CFG = afs.defaultConfig
        
        # LOG INIT
        classLogLevel = getattr(afs.defaultConfig,"LogLevel_%s" % self.__class__.__name__, "").upper()
        numericLogLevel = getattr(logging,classLogLevel, 0)
        self.Logger=logging.getLogger("afs.service.%s" % self.__class__.__name__)
        self.Logger.setLevel(numericLogLevel)
        self.Logger.debug("initializing %s-Object with conf=%s" % (self.__class__.__name__, conf))      
        
        # DB INIT 
        if self._CFG.DB_CACHE :
            self.DBCService=DBCacheService()
        else : # this is a simple object raising an error if called.
            class NODBCacheService :
                def __init__(self) :
                    raise AfsError("No DBcache defined.")
            self.DBCService=NODBCacheService()
        
        # DAO INIT 
        if self._CFG.DAOImplementation == "childprocs" :
            for dao in DAOList :
                if dao == "vl":
                    from afs.dao.VLDbDAO import VLDbDAO
                    self._vlDAO  = VLDbDAO()
                elif dao == "vol" :
                    from afs.dao.VolumeDAO import VolumeDAO 
                    self._volDAO = VolumeDAO()
                elif dao == "bnode" :
                    from afs.dao.BNodeDAO import BNodeDAO
                    self._bnodeDAO = BNodeDAO()
                elif dao == "fs" :
                    from afs.dao.FileServerDAO import FileServerDAO
                    self._fsDAO = FileServerDAO()
                elif dao == "pag" :
                    from afs.dao import PAGDAO
                    self._pagDAO=PAGDAO.PAGDAO()
                elif dao == "krb5" :
                    from afs.dao import krb5DAO
                    self._krb5DAO=krb5DAO.krb5DAO()
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
