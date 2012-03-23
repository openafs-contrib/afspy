import socket

from afs.service.BaseService import BaseService
from afs.model.Server import Server




class FsService (BaseService):
    """
    Provides Service about a FileServer
    """
    
    _CFG    = None
    
    def __init__(self,conf=None):
        BaseService.__init__(self, conf, DAOList=["fs", "bnode", "vl"])
        

    ###############################################
    # BNode Section
    ##############################################

    def getRestartTimes(self,name, **kwargs):
            """
            return Dict about the restart times of the afs-server
            """
            TimesDict=self._bnodeDAO.getRestartTimes(name, self._CFG.CELL_NAME, self._CFG.Token)
            return TimesDict
            
    def setRestartTimes(self,name,time, restarttype,  **kwargs):
            """
            Ask Bosserver about the restart times of the fileserver
            """
            self._bnodeDAO.setRestartTimes(name,time, restarttype,  self._CFG.CELL_NAME, self._CFG.Token)
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
            vols = self._fsDAO.getVolIdList(partname, servername,self._CFG.CELL_NAME)
        else:
            parts = self._fsDAO.getPartList(servername,self._CFG.CELL_NAME)
            for part in parts:
                vols.extend(self._svrDAO.getVolIdList(part.name, servername,self._CFG.CELL_NAME))
    
        return vols
    
    
    
    
    
    ###############################################
    # File Server Section
    ###############################################
    
    
    def getFileServer(self,name_or_ip,cached=False):
        """
        Retrieve Server 
        """
        FileServer =Server()
        # get DNS-info about server
        DNSInfo=socket.gethostbyname_ex(name_or_ip)
        FileServer.servernames=[DNSInfo[0]]+DNSInfo[1]
        FileServer.ipaddrs=DNSInfo[2]
        # UUID
        FileServer.uuid=self.getUUID(name_or_ip, self._CFG.CELL_NAME, cached)
        parts = self._fsDAO.getPartList(FileServer.servernames[0], self._CFG.CELL_NAME, self._CFG.Token)
        #FIXME  Cache 
        FileServer.parts = parts
        return FileServer

    #
    # convenience functions  
    #

    def getUUID(self, name_or_ip="", cellname="", cached=False):
        """
        returns UUID of a fileserver, which is used as key for server-entries
        in other tables
        """
        uuid=""
        if cellname == "" :
            cellname = self._CFG.CELL_NAME
        if cached :
            cellCache=self._getFromCache(cellname)
            for serv in cellCache.FileServers :
                if name_or_ip in serv["ipaddrs"] or name_or_ip in serv["hostnames"]: 
                    uuid = serv["uuid"]
                    break
        else :
            self._vlDAO.getFsUUID(name_or_ip, cellname, self._CFG.Token)
        return uuid

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
