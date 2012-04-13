
from afs.service.BaseService import BaseService
from afs.model.Server import Server
from afs.exceptions.AfsError import AfsError
from afs.model.ExtendedVolumeAttributes import ExtVolAttr
from afs.model.Volume import Volume
from afs.model.Partition import Partition
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

    def getRestartTimes(self,name):
            """
            return Dict about the restart times of the afs-server
            """
            TimesDict=self._bnodeDAO.getRestartTimes(name, self._CFG.CELL_NAME, self._CFG.Token)
            return TimesDict
            
    def setRestartTimes(self,name,time, restarttype):
            """
            Ask Bosserver about the restart times of the fileserver
            """
            self._bnodeDAO.setRestartTimes(name,time, restarttype,  self._CFG.CELL_NAME, self._CFG.Token)
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
            parts = self.getPartitions(servername,self._CFG.CELL_NAME, cached=cached)
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

    #
    # convenience functions  
    #

    def getUUID(self, name_or_ip="",cached=False):
        """
        returns UUID of a fileserver, which is used as key for server-entries
        in other tables
        """
        servernames, ipaddrs=afsutil.getDNSInfo(name_or_ip)
        uuid=""
        if cached :
            return self._getUUIDFromCache(servernames)
        else :
            FileServer=Server()
            uuid=self._vlDAO.getFsUUID(name_or_ip, self._CFG.CELL_NAME, self._CFG.Token)
            FileServer.uuid=uuid
            FileServer.servernames=servernames
            FileServer.ipaddrs=ipaddrs
            if  self._CFG.DB_CACHE:
                self._setServerIntoCache(FileServer)
        return FileServer.uuid

    def getProjects(self, name_or_ip):
        """
        return a dict ["partition-name"]["projectname"]["VolumeType"]=numVolumes
        """
        if not self._CFG.DB_CACHE:
            raise AfsError("DB_CACHE not configured")
        serv_uuid=self.getUUID(name_or_ip)
        print  self.DbSession.query(Volume).join((ExtVolAttr, Volume.vid==ExtVolAttr.vid)).filter(Volume.serv_uuid==serv_uuid)
        projDict={}
        return projDict
        
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

        partList = self._fsDAO.getPartList(name_or_ip, self._CFG.CELL_NAME, self._CFG.Token)
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

    ################################################
    #  Internal Cache Management 
    ################################################

    def _getUUIDFromCache(self, name_or_ip):
        """
        get data from Cache
        """
        if not self._CFG.DB_CACHE:
            raise AfsError("DB_CACHE not configured")
        
        serv=self.DbSession.query(Server).filter(self.or_(Server.servernames.like(name_or_ip), Server.ipaddrs.like(name_or_ip) )).first()
        self.Logger.debug("%s gives %s" % (name_or_ip, serv))
        if serv :
            return serv.uuid
        else :
            return None

    def _getServerFromCache(self, uuid):
        """
        get data from Cache
        """
        if not self._CFG.DB_CACHE:
            raise AfsError("DB_CACHE not configured")
        serv= self.DbSession.query(Server).filter(Server.uuid == uuid).first()
        self.Logger.debug("%s gives %s" % (uuid, serv))
        return serv
        
    def _getPartsFromCache(self, serv_uuid):
        """
        get data from Cache
        """
        if not self._CFG.DB_CACHE:
            raise AfsError("DB_CACHE not configured")
        parts=self.DbSession.query(Partition).filter(Partition.serv_uuid == serv_uuid).all()
        self.Logger.debug("%s gives %s" % (serv_uuid, parts))
        return parts
        
    def _setServerIntoCache(self,serv):
        """
        update DB cache
        """
        if not self._CFG.DB_CACHE:
            raise AfsError("DB_CACHE not configured")
        servCache = self.DbSession.query(Server).filter(Server.uuid == serv.uuid).first()
        if servCache:
            servCache.copyObj(serv)
            self.DbSession.flush()
        else:
            servCache=self.DbSession.merge(serv)  
            self.DbSession.flush()
        return servCache    
        
    def _setPartIntoCache(self, part, serv_uuid):
        """
        update DB cache
        """
        if not self._CFG.DB_CACHE:
            raise AfsError("DB_CACHE not configured")
        part.serv_uuid=serv_uuid
        self.Logger.debug("setting into cache: %s" % part)
        partCache = self.DbSession.query(Partition).filter(Partition.serv_uuid == serv_uuid).filter(Partition.name == part.name).first()
        if partCache:
            partCache.copyObj(part)
            self.DbSession.flush()
        else:
            partCache=self.DbSession.merge(part)  
            self.DbSession.flush()
        self.DbSession.commit()  
        return partCache
    
    def _delServerFromCache(self,serv):
        """
        remove object from cache
        """
        if not self._CFG.DB_CACHE:
            raise AfsError("DB_CACHE not configured")
        # Do update
        self.DbSession.delete(serv)
        self.DbSession.commit()
        
    def _delPartsFromCache(self,parts):
        """
        remove object from cache
        """
        if not self._CFG.DB_CACHE:
            raise AfsError("DB_CACHE not configured")
        # Do update
        self.DbSession.delete(parts)
        self.DbSession.commit()
