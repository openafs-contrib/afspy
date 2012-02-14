import logging, socket

from afs.dao.FileServerDAO import FileServerDAO
from afs.dao.ProcessDAO import ProcessDAO
from afs.exceptions.FSError import  FSError
from afs.model.Server import Server
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
        self.Logger=logging.getLogger("afs.%s" % self.__class__.__name__)
        self.Logger.debug("initializing %s-Object with conf=%s" % (self.__class__.__name__,conf))

        # DAO INIT
        self._svrDAO = FileServerDAO()
        self._procDAO = ProcessDAO()
        

    ###############################################
    # BNode Section
    ##############################################

    def getRestartTimes(self,name, **kwargs):
            """
            return Dict about the restart times of the afs-server
            """
            TimesDict=self._procDAO.getRestartTimes(name, self._CFG.CELL_NAME, self._CFG.Token)
            return TimesDict
            
    def setRestartTimes(self,name,time, restarttype,  **kwargs):
            """
            Ask Bosserver about the restart times of the fileserver
            """
            self._procDAO.setRestartTimes(name,time, restarttype,  self._CFG.CELL_NAME, self._CFG.Token)
            return
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
        FileServer =Server()
        # get DNS-info about server
        DNSInfo=socket.gethostbyname_ex(servername)
        FileServer.servernames=[DNSInfo[0]]+DNSInfo[1]
        FileServer.ipaddrs=DNSInfo[2]
        parts = self._svrDAO.getPartList(FileServer.servernames[0], self._CFG.CELL_NAME, self._CFG.Token)
        #FIXME  Cache 
        FileServer.parts = parts
        return FileServer


        ################################################
        # Statistcis DB BASE
        ################################################
    
        #TODO Number volumes
        
        #Number of partitions
        
        #Total Space/usage/free
        
        #Total Number of files
        
        #Access statistics
        
        #Volume offline
    
        #Volume KO
