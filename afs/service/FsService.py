from afs.service.BaseService import BaseService
from afs.model.Server import Server
from afs.exceptions.AfsError import AfsError
from afs.model.ExtendedVolumeAttributes import ExtVolAttr
from afs.model.Volume import Volume
from afs.model.Partition import Partition
from afs.model.Project import Project
from afs.util  import afsutil


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

    def getRestartTimes(self,name_or_ip):
            """
            return Dict about the restart times of the afs-server
            """
            TimesDict=self._bnodeDAO.getRestartTimes(name_or_ip, self._CFG.CELL_NAME, self._CFG.Token)
            return TimesDict
            
    def setRestartTimes(self,name_or_ip,time, restarttype):
            """
            Ask Bosserver about the restart times of the fileserver
            """
            self._bnodeDAO.setRestartTimes(name_or_ip,time, restarttype,  self._CFG.CELL_NAME, self._CFG.Token)
            return

    ###############################################
    # Volume Section
    ###############################################    
    
    def getVolList(self,servername, partname=None, cached=False):
        """
        Retrieve Volume List.
        Update attribute 'booked' in the DBCache 
        """
        vols = []
            
        if partname:    
            vols = self._fsDAO.getVolList( servername,partname,self._CFG.CELL_NAME, self._CFG.Token)
        else:
            parts = self.getPartitions(servername,cached=cached)
            for part in parts:
                vols += self._fsDAO.getVolList(servername,parts[part]["name"], self._CFG.CELL_NAME, self._CFG.Token)
        return vols
    
    ###############################################
    # File Server Section
    ###############################################
    
    def getFileServer(self,name_or_ip,cached=False):
        """
        Retrieve Fileserver Object by hostname or IP and update DBCache, if enabled 
        """
        self.Logger.debug("Entering getFileServer")

        if name_or_ip in self._CFG.ignoreIPList :
            return None
        
        uuid=afsutil.getFSUUIDByName_IP(name_or_ip,self._CFG, cached)
        return self.getFileServerByUUID(uuid,cached=False)

    def getFileServerByUUID(self,uuid,name_or_ip="",cached=False):
        """
        Retrieve Fileserver Object by UUID and update DBCache, if enabled.
        """
        self.Logger.debug("Entering getFileServerByUUID with uuid=%s" % uuid)

        if cached :
            FileServer=self.DBManager.getFromCache(Server,uuid=uuid)
            FileServer.parts = {}
            for p in self.DBManager.getFromCache(Partition,mustBeunique=False,serv_uuid=uuid) :
                FileServer.parts[p.name] = p.getDict()
            return FileServer

        # avoid uuid->hostname lookup if we already have that info
        if name_or_ip == "" :
            name_or_ip=afsutil.getHostnameByFSUUID(uuid,self._CFG,cached)

        FileServer = Server()
        # get DNS-info about server
        FileServer.servernames, FileServer.ipaddrs=afsutil.getDNSInfo(name_or_ip)
        # UUID
        FileServer.uuid=afsutil.getFSUUIDByName_IP(name_or_ip, self._CFG, cached)

        # Partitions
        FileServer.parts = self.getPartitions(name_or_ip,cached)
        if self._CFG.DB_CACHE :
            self.DBManager.setIntoCache(Server,FileServer,uuid=FileServer.uuid)
            for p in FileServer.parts  :
                part=Partition()
                self.Logger.debug("Setting part to %s" % FileServer.parts[p])
                part.setByDict(FileServer.parts[p])
                part.serv_uuid=FileServer.uuid
                self.DBManager.setIntoCache(Partition,part,serv_uuid=FileServer.uuid,name=p)

        # Projects
        # these we get directly from the DB_Cache
        
        FileServer.projects = []
        return FileServer

    def getProjectsonPartitions(self, name_or_ip):
        """
        return a dict ["partition-name"]["projectname"]["VolumeType"]=numVolumes
        """
        raise AfsError("Not implemented yet.")
        if not self._CFG.DB_CACHE:
            raise AfsError("DB_CACHE not configured")
        serv_uuid=afsutil.getFSUUIDByName_IP_FromCache(name_or_ip,self._CFG)
        projDict={}
        for p in self.DBManager.getFromJoinwithFilter(Volume,ExtVolAttr, Volume.vid,ExtVolAttr.vid,serv_uuid = serv_uuid) :
           projDict["a"]=None
        return projDict
        
    def getPartitions(self, name_or_ip, cached=False):
        """
        return dict ["partname"]={"numROVolumes", "numRWVolumes","usage","free","total","serv_uuid" }
        """
        serv_uuid=afsutil.getFSUUIDByName_IP(name_or_ip, self._CFG,cached)
        if cached :
            partDict={}
            for p in self.DBManager.getFromCache(Partition,mustBeunique=False,serv_uuid=serv_uuid) :
                partDict[p.name] = p.getDict()
            return partDict
        partList = self._fsDAO.getPartList(name_or_ip, self._CFG.CELL_NAME, self._CFG.Token)
        partDict={}
        for p in partList :
            p["serv_uuid"]=serv_uuid
            partDict[p["name"]]=p
        return partDict

    def getVolStati(self, name_or_ip):
        """
        get number of online and offline volumes
        """
        StatDict={"total": -1, "on-line" : -1, "off-line" : -1}
        return StatDict

    ################################################
    #  Internal Cache Management 
    ################################################

