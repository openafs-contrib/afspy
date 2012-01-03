import logging

from afs.dao.FileServerDAO import FileServerDAO
from afs.dao.ProcessDAO import ProcessDAO
from afs.exceptions.FSError import  FSError
import afs

class FsService (object):
    """
    Provides Service about a FileServer
    """
    
    _CFG    = None
    
    def __init__(self,conf=None):

        # CONF INIT 
        if conf:
            self._CFG = conf
        else:
            self._CFG = afs.defaultConfig
        
        # LOG INIT
        self.Logger=logging.getLogger("afs").getChild(self.__class__.__name__)
        self.Logger.debug("initializing %s-Object with conf=%s" % (self.__class__.__name__,conf))

        # DAO INIT
        self._svrDAO = FileServerDAO()
        self._procDAO = ProcessDAO()
        
        # DB INIT    
        if self._CFG.DB_CACHE:
            from afs.orm.DbMapper import DbMapper
            self.DbSession     = DbMapper(['Process'])

    ###############################################
    # BNode Section
    ##############################################

    def getRestartTimes(self,name, **kwargs):
            """
            Ask Bosserver about the restart times of the fileserver
            """
            rc, general, binary=self._procDAO.getRestartTimes(name, self._CFG.CELL_NAME, self._CFG.Token)
            if not rc :
                return general, binary
            
    def setRestartTimes(self,name,time, restarttype,  **kwargs):
            """
            Ask Bosserver about the restart times of the fileserver
            """
            rc, output, outerr=self._procDAO.setRestartTimes(name,time, restarttype,  self._CFG.CELL_NAME, self._CFG.Token)
            if not rc :
                return time
            else :
                return None
                
                
    ###############################################
    # Volume Section
    ###############################################    
    
    
    def getVolIdList(self,servername, partname=None,**kwargs):
        """
        Retrieve Volume ID List
        """
        vols = []
            
        if partname:    
            vols = self._svrDAO.getVolIdList(partname, servername,self._CFG.CELL_NAME)
        else:
            parts = self._svrDAO.getPartList(servername,self._CFG.CELL_NAME)
            for part in parts:
                vols.extend(self._svrDAO.getVolIdList(part.name, servername,self._CFG.CELL_NAME))
    
        return vols
    
    ###############################################
    # File Server Section
    ###############################################
    
    
    def getFileServer(self,servername,**kwargs):
        """
        Retrieve Server 
        """
            
        server = self._svrDAO.getServer(self,servername,self._CFG.CELL_NAME)
        parts = self._svrDAO.getPartList(server.name,self._CFG.CELL_NAME)
        server.parts = parts

        return server
