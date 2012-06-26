from afs.service.BaseService import BaseService
from afs.service.FsService import FsService
from afs.model.Server import Server
from afs.exceptions.AfsError import AfsError
from afs.model.ExtendedVolumeAttributes import ExtVolAttr
from afs.model.Volume import Volume
from afs.model.Partition import Partition
from afs.util  import afsutil


class OSDFsService (FsService):
    """
    Provides Service about a FileServer
    """
    
    _CFG    = None
    
    def __init__(self,conf=None):
        BaseService.__init__(self, conf, DAOList=["osdfs", "bnode", "vl"])

    ###############################################
    # Volume Section
    ###############################################    
    
    def getVolList(self,servername, partname=None, cached=False):
        """
        Retrieve Volume List
        """
        vols = []
            
        if partname:    
            vols = self._osdfsDAO.getVolList( servername,partname,self._CFG.CELL_NAME, self._CFG.Token)
        else:
            parts = self.getPartitions(servername,cached=cached)
            for part in parts:
                vols += self._osdfsDAO.getVolList(servername,parts[part]["name"], self._CFG.CELL_NAME, self._CFG.Token)
        return vols
    
    ###############################################
    # File Server Section
    ###############################################
    
    def getFileServer(self,name_or_ip,cached=False):
        """
        Retrieve Server 
        """
        self.Logger.debug("Entering getFileServer")
        if name_or_ip in self._CFG.ignoreIPList :
            return None
        
        if cached :
            uuid=self.getUUID(name_or_ip,   cached)
            FileServer=self._getServerFromCache(uuid)
            FileServer.parts = self.getPartitions(name_or_ip, cached)
            return FileServer

        FileServer =Server()
        # get DNS-info about server
        FileServer.servernames, FileServer.ipaddrs=afsutil.getDNSInfo(name_or_ip)
        # UUID
        FileServer.uuid=self.getUUID(name_or_ip,  cached)
        # Partitions
        FileServer.parts = self.getPartitions(name_or_ip,cached)
        if self._CFG.DB_CACHE :
            self._setServerIntoCache(FileServer)
            for p in FileServer.parts  :
                part=Partition()
                part.setByDict(FileServer.parts[p])
                self._setPartIntoCache(part, FileServer.uuid)
        # Projects
        # these we get directly from the DB_Cache
        if cached :
            FileServer.projects = self._getProjectsFromCache( FileServer.uuid)
        else :
            FileServer.projects = []
        return FileServer

    def getPartitions(self, name_or_ip, cached=False):
        """
        return dict ["partname"]={"numROVolumes", "numRWVolumes","usage","free","total" }
        """
        if cached :
            serv_uuid=self.getUUID(name_or_ip, cached)
            partDict={}
            for p in  self._getPartsFromCache(serv_uuid) :
                partDict[p.name] = p.getDict()
            return partDict

        partList = self._osdfsDAO.getPartList(name_or_ip, self._CFG.CELL_NAME, self._CFG.Token)
        partDict={}
        for p in partList :
            partDict[p["name"]]=p
        return partDict

    def getVolStati(self, name_or_ip):
        """
        get number of online and offline volumes
        """
        StatDict={"total": -1, "on-line" : -1, "off-line" : -1}
        return StatDict
