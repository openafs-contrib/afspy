from afs.service.BaseService import BaseService
from afs.model.FileServer import FileServer
from afs.exceptions.AfsError import AfsError
from afs.model.ExtendedVolumeAttributes import ExtVolAttr
from afs.model.ExtendedPartitionAttributes import ExtPartAttr
from afs.model.Volume import Volume
from afs.model.Partition import Partition
from afs.model.Project import Project
from afs.util  import afsutil


class FsService (BaseService):
    """
    Provides Service about a FileServer
    """
    
    def __init__(self,conf=None):
        BaseService.__init__(self, conf, DAOList=["fs", "bnode", "vl","rx","vol"])

    ###############################################
    # Volume Section
    ###############################################    
    
    def getVolList(self,servername, partname=None, _user="", cached=False):
        """
        Retrieve Volume List.
        """
        vols = []
            
        if partname:    
            vols = self._fsDAO.getVolList( servername,partname,self._CFG.CELL_NAME, _cfg=self._CFG, _user=_user)
        else:
            parts = self.getPartitions(servername,cached=cached)
            for part in parts:
                vols += self._fsDAO.getVolList(servername,parts[part]["name"], self._CFG.CELL_NAME, _cfg=self._CFG, _user=_user)
        return vols
    
    ###############################################
    # File Server Section
    ###############################################
    
    def getFileServer(self,name_or_ip,**kw):
        """
        Retrieve Fileserver Object by hostname or IP  or uuid and update DBCache, if enabled 
        """
        self.Logger.debug("Entering getFileServer with kw=%s" % kw)
        uuid=kw.get("uuid","")
        cached=kw.get("cached","")
        _user=kw.get("_user","")

        servernames, ipaddrs=afsutil.getDNSInfo(name_or_ip)
        if ipaddrs[0] in self._CFG.ignoreIPList :
            return None
        if uuid != "" :
            if uuid != afsutil.getFSUUIDByName_IP(name_or_ip,self._CFG, cached) :
                uuid=afsutil.getFSUUIDByName_IP(name_or_ip,self._CFG, cached)
        else :
            uuid=afsutil.getFSUUIDByName_IP(name_or_ip,self._CFG, cached)
         
        if cached :
            this_FileServer=self.DBManager.getFromCache(FileServer,uuid=uuid)
            if this_FileServer == None : # it's not in the cache. Log it and get it from live-system
                self.Logger.warn("getFileServer: FS with uuid=%s not in DB." % uuid)
            else :
                this_FileServer.parts = self.getPartitionsByUUID(uuid,name_or_ip=this_FileServer.servernames[0],cached=cached)
                return this_FileServer

        this_FileServer = FileServer()
        # get DNS-info about server
        this_FileServer.servernames, this_FileServer.ipaddrs=afsutil.getDNSInfo(name_or_ip)
        # UUID
        this_FileServer.uuid=uuid
        this_FileServer.version,this_FileServer.builddate=self._rxDAO.getVersionandBuildDate(this_FileServer.servernames[0], 7000, _cfg=self._CFG, _user=_user)
        # Partitions
        this_FileServer.parts = self.getPartitions(name_or_ip,cached=cached)
        if self._CFG.DB_CACHE :
            self.DBManager.setIntoCache(FileServer,this_FileServer,uuid=this_FileServer.uuid)
            for p in this_FileServer.parts  :
                part=Partition()
                self.Logger.debug("Setting part to %s" % this_FileServer.parts[p])
                part.setByDict(this_FileServer.parts[p])
                part.serv_uuid=this_FileServer.uuid
                self.DBManager.setIntoCache(Partition,part,serv_uuid=this_FileServer.uuid,name=p)

        # Projects
        # these we get directly from the DB_Cache
        
        this_FileServer.projects = []
        self.Logger.debug("getFileServerByUUID: returning: %s" % this_FileServer)
        return this_FileServer

    def getPartitions(self,name_or_ip,cached=False) : 
        servernames, ipaddrs=afsutil.getDNSInfo(name_or_ip)
        serv_uuid=afsutil.getFSUUIDByName_IP(servernames[0], self._CFG, cached)
        return self.getPartitionsByUUID(serv_uuid,name_or_ip=servernames[0],cached=cached)

    def getPartitionsByUUID(self,serv_uuid, **kw):
        """
        return dict ["partname"]={"numRW", "numRO","numBK","usage","free","total","serv_uuid"}
        if DB_CACHE is used, then also return "ExtAttr" ={}
        """
        cached=kw.get("cached",False)
        name_or_ip=kw.get("name_or_ip",False)
        _user=kw.get("_user","")
        if cached :
            partDict={}
            for p in self.DBManager.getFromCache(Partition,mustBeunique=False,serv_uuid=serv_uuid) :
                partDict[p.name] = p.getDict()
                extPartAttr=self.DBManager.getFromCache(ExtPartAttr,mustBeunique=True,serv_uuid=serv_uuid,name=p.name)
                if extPartAttr != None :
                    partDict[p.name]["ExtAttr"] = extPartAttr.getDict()
                else : # if there is no "ExtAttr", fake an emtpy one !? 
                    partDict[p.name]["ExtAttr"] =  None
                # XXX if there's no entry, fix default value of projectIDS
                if partDict[p.name]["ExtAttr"] == None :
                    partDict[p.name]["ExtAttr"] = { "projectIDs" : [] }
            return partDict
        if name_or_ip == "" :
            name_or_ip=afsutil.getHostnameByFSUUID(serv_uuid,self._CFG)
        partList = self._fsDAO.getPartList(name_or_ip, self._CFG.CELL_NAME, _cfg=self._CFG, _user=_user)
        partDict = {}
        for p in partList :
            p["serv_uuid"]=serv_uuid
            partDict[p["name"]] = p
        return partDict

    def getVolumeIDs(self,name_or_ip,part="",_user="",cached=False) :
        """
        return list of IDs present on given server partition
        """
        self.Logger.debug("getVolumeIds: Entering with name_or_ip=%s,part=%s,cached=%s" % (name_or_ip,part,cached) )
        servernames,ipaddrs = afsutil.getDNSInfo(name_or_ip)
        # UUID
        uuid=afsutil.getFSUUIDByName_IP(servernames[0],self._CFG)
        if cached :
            if part != "" :
               pass
            else :
               pass 
            return []
        return self._volDAO.getVolIDList(servernames[0],self._CFG.CELL_NAME,Partition=part, _cfg=self._CFG, _user=_user)

    def getNumVolumes(self,name_or_ip,part="",_user="",cached=False) :
        """
        Scan all or one server-partition and count volums
        """
        self.Logger.debug("getNumVolumes: Entering with name_or_ip=%s,part=%s,cached=%s" % (name_or_ip,part,cached) )
        # get DNS-info about server
        servernames, ipaddrs=afsutil.getDNSInfo(name_or_ip)
        # UUID
        uuid=afsutil.getFSUUIDByName_IP(servernames[0],self._CFG)
        if cached :
            if part != "" :
                numRW=self.DBManager.count(Volume.id,type="RW",serv_uuid=uuid,part=part)
                numRO=self.DBManager.count(Volume.id,type="RO",serv_uuid=uuid,part=part)
                numBK=self.DBManager.count(Volume.id,type="BK",serv_uuid=uuid,part=part)
                numOffline=self.DBManager.count(Volume.id,status="offline",serv_uuid=uuid,part=part)
            else :
                numRW=self.DBManager.count(Volume.id,type="RW",serv_uuid=uuid)
                numRO=self.DBManager.count(Volume.id,type="RO",serv_uuid=uuid)
                numBK=self.DBManager.count(Volume.id,type="BK",serv_uuid=uuid)
                numOffline=self.DBManager.count(Volume.id,status="offline")
        else :
            numRW = numRO = numBK = numOffline = 0
            for f in self._vlDAO.getFsServList(self._CFG.CELL_NAME, noresolve=True, _cfg=self._CFG, _user=_user) :
                self.Logger.debug("server=%s" %f)
                for v in self._vlDAO.getVolumeList(f["name_or_ip"],self._CFG.CELL_NAME, part,noresolve=True, _cfg=self._CFG, _user=_user) :
                    self.Logger.debug("Volume=%s" % v )
                    if v["RWSite"] == f["name_or_ip"] :
                         numRW += 1
                    if f["name_or_ip"] in v["ROSites"] :
                        numRO += 1
                self.Logger.debug("_getNumVolumes having: %s,%s,%s,%s" % (numRW,numRO,numBK,numOffline))
            # we don't get infos about existing Backups here !?
            # an existing BK-ID doesnot mean that there is one.
            numBK = -1
        self.Logger.debug("getNumVolumes returning: %s,%s,%s,%s" % (numRW,numRO,numBK,numOffline))
        return numRW,numRO,numBK,numOffline 
