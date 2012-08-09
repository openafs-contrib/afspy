
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
        Retrieve Volume List
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
        Retrieve Server 
        """
        self.Logger.debug("Entering getFileServer")
        if name_or_ip in self._CFG.ignoreIPList :
            return None
        
        if cached :
            uuid=self.getUUID(name_or_ip, cached)
            FileServer=self.DBCService.getFromCache(Server,uuid=uuid)
            FileServer.parts = {}
            for p in self.DBCService.getFromCache(Partition,mustBeunique=False,serv_uuid=uuid) :
                FileServer.parts[p.name] = p.getDict()
            return FileServer

        FileServer =Server()
        # get DNS-info about server
        FileServer.servernames, FileServer.ipaddrs=afsutil.getDNSInfo(name_or_ip)
        # UUID
        FileServer.uuid=self.getUUID(name_or_ip,  cached)
        # Partitions
        FileServer.parts = self.getPartitions(name_or_ip,cached)
        if self._CFG.DB_CACHE :
            self.DBCService.setIntoCache(Server,FileServer,uuid=FileServer.uuid)
            for p in FileServer.parts  :
                part=Partition()
                self.Logger.debug("Setting part to %s" % FileServer.parts[p])
                part.setByDict(FileServer.parts[p])
                self.DBCService.setIntoCache(Partition,part,serv_uuid=FileServer.uuid,name=p)
        # Projects
        # these we get directly from the DB_Cache
        
        FileServer.projects = []
        return FileServer

    #
    # convenience functions  
    #

    def getHostnameByUUID(self,uuid,cached=False) :
        """
        returns hostname of a fileserver by uuid
        """
        for fs in self._vlDAO.getFsServList(self._CFG.CELL_NAME, self._CFG.Token) :
            if fs['uuid'] == uuid :
               return fs['name_or_ip']
        return None
        
    def getUUID(self, name_or_ip,cached=False):
        """
        returns UUID of a fileserver, which is used as key for server-entries
        in other tables. This does not silently update the Cache
        """
        servernames, ipaddrs=afsutil.getDNSInfo(name_or_ip)
        uuid=""
        if cached :
            return self._getUUIDFromCache(name_or_ip)
        else :
            uuid=self._vlDAO.getFsUUID(name_or_ip, self._CFG.CELL_NAME, self._CFG.Token)
        return uuid

    def getProjectsonPartitions(self, name_or_ip):
        """
        return a dict ["partition-name"]["projectname"]["VolumeType"]=numVolumes
        """
        raise AfsError("Not implemented yet.")
        if not self._CFG.DB_CACHE:
            raise AfsError("DB_CACHE not configured")
        serv_uuid=self.getUUID(name_or_ip,cached=True)
        projDict={}
        for p in self.DBCService.getFromJoinwithFilter(Volume,ExtVolAttr, Volume.vid,ExtVolAttr.vid,serv_uuid = serv_uuid) :
           projDict["a"]=None
        return projDict
        
    def getPartitions(self, name_or_ip, cached=False):
        """
        return dict ["partname"]={"numROVolumes", "numRWVolumes","usage","free","total","serv_uuid" }
        """
        serv_uuid=self.getUUID(name_or_ip, cached)
        if cached :
            partDict={}
            for p in self.DBCService.getFromCache(Partition,mustBeunique=False,serv_uuid=serv_uuid) :
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

    def _getUUIDFromCache(self, name_or_ip):
        """
        get data from Cache
        """
        if not self._CFG.DB_CACHE:
            raise AfsError("DB_CACHE not configured")
        self.Logger.debug("%s isName: %s" % (name_or_ip,afsutil.isName(name_or_ip)))
        if afsutil.isName(name_or_ip) :
            list=self.DBCService.getFromCacheByListElement(Server,Server.servernames_js,name_or_ip)         
        else :
            list=self.DBCService.getFromCacheByListElement(Server,Server.ipaddrs_js,name_or_ip)         
        self.Logger.debug("%s gives %s" % (name_or_ip, list))
        uuidlist=[] 
        for l in list :
            uuidlist.append(l.uuid)
        if len(uuidlist) == 0:
            return None
        elif len(uuidlist) == 1 :
            return uuidlist[0]
        else :
            self.Logger.info("%s gives more than one uuid :%s" % (name_or_ip, uuidlist))
            return uuidlist

    
