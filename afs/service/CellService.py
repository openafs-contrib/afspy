import socket,sys

from afs.service.CellServiceError import CellServiceError
from afs.model.Cell import Cell
from afs.model.FileServer import FileServer
from afs.model.DBServer import DBServer
from afs.service.BaseService import BaseService
from afs.service.FSsService import FSsService
from afs.service.BosService import BosService
from afs.service.ProjectService import ProjectService
import afs

class CellService(BaseService):
    """
    Provides Service about a Cell global information.
    The cellname is set in the configuration passed to constructor.
    Thus one instance works only for cell.
    """
    def __init__(self, conf=None):
        BaseService.__init__(self, conf, DAOList=["fs", "vl", "vol", "rx", "ubik"])
        self.FS=FSsService()
        self.PS=ProjectService()
        self.BosS=BosService()
        return


    def get_cell_info(self, cellname="", _user="", cached=False) :
        """
        return full Cellobject.
        """
        if cellname == "" : cellname = self._CFG.cell
        self.Logger.debug("Using cellname : %s " % cellname)
        if cached :
            cell=self.DBManager.get_from_cache(Cell, name = cellname)
            if cell != None :
                self.Logger.debug("getCellInfo: Cell.db_update_date=%s" % cell.db_update_date)
                # update Sums etc. from DB_CACHE
                cell.name=cellname
                self.Logger.debug("getCellInfo: Cell.FileServers=%s" % cell.file_servers)
                cell.numRW = cell.numRO = cell.numBK = cell.numOffline = 0
                numVolDict=self.bulk_getNumVolumes()
                removedServers=[]
                for f in cell.file_servers :
                    self.Logger.debug("getCellInfo: f=%s" % f)
                    try :
                        uuid = afs.LOOKUP_UTIL[self._CFG.cell].get_fsuuid(f)
                    except :
                        self.Logger.error("Cannot get uuid for %s. Ignore it here. Will be removed on next live-update" % f )
                    if numVolDict.has_key(uuid) :
                        cell.num_vol_rw += numVolDict[uuid].get("RW",0)
                        cell.num_vol_rw += numVolDict[uuid].get("RO",0)
                        cell.num_vol_bk += numVolDict[uuid].get("BK",0)
                cell.num_vol_offline = -1
                cell.num_users,cell.num_groups = self.getPTInfo(cached=True)
                cell.allocated_kb,cell.allocated_stale_kb = self.getAllocated()
                cell.size_kb,cell.used_kb,cell.free_kb=self.getUsage(cached=True)
                cell.projects=[] # Projects are in DB_CACHE only
                for p in self.PS.getProjectList() :
                    cell.Projects.append(p.name)
                self.Logger.debug("Cell=%s" % cell)
                return cell

        # refresh whole new CellObj
        cell = Cell()
        cell.name = cellname
        cell.file_servers=self.get_fileservers()
        cell.DBServers=self.get_dbservers()
        cell.PTDBSyncSite, cell.PTDBVersion,cell.PTDBState=self.get_ubik_db_info(cell.DBServers[0]["hostname"],7002)
        cell.VLDBSyncSite, cell.VLDBVersion,cell.VLDBState=self.get_ubik_db_info(cell.DBServers[0]["hostname"],7003)
        cell.numRW = cell.numRO = cell.numBK = cell.numOffline = 0
        for f in cell.file_servers :
            numRW,numRO,numBK,numOffline = self.FS.getNumVolumes(name_or_ip=f,cached=True)
            cell.numRW += numRW
            cell.numRO += numRO
            cell.numBK += numBK
            cell.numOffline += numOffline
        cell.numUsers,cell.numGroups = self.getPTInfo()
        cell.size,cell.used,cell.free=self.getUsage()
        # some information are only available if DB_CACHE is used.
        cell.allocated,cell.allocated_stale = -1,-1
        cell.Projects=[] # Projects are in DB_CACHE only

        if self._CFG.DB_CACHE :
            for p in self.PS.getProjectList() :
                cell.Projects.append(p.name)
            cell.allocated,cell.allocated_stale = self.getAllocated()
            self.Logger.debug("Cell=%s" % Cell)
            self.DBManager.set_into_cache(Cell,cell, name=self._CFG.cell)
        return cell

    def refreshLiveData(self, cellname="") : 
        """
        update livedata for the cell :
        partition free and used space, DBVersions, list of Servers
        """
        if cellname == "" : cellname = self._CFG.cell
        cell=Cell()
        cell.file_servers=self.getFileServers()
        cell.DBServers=self.getDBServers()
        cell.PTDBSyncSite, cell.PTDBVersion,cell.PTDBState=self.get_ubik_db_info(cell.DBServers[0]["hostname"],7002)
        cell.VLDBSyncSite, cell.VLDBVersion,cell.VLDBState=self.get_ubik_db_info(cell.DBServers[0]["hostname"],7003)
        cell.size,cell.used,cell.free=self.getUsage()
        return True 

  
    ###############################################
    # Internal helper Section
    ###############################################    
   
    def get_fileservers(self, _user="", cached=True):
        """
        Return FileServers as a list of hostnames for each fileserver
        """
        FileServers=[]
        if cached :
            _file_servers = self.DBManager.get_from_cache(FileServer, mustBeUnique=False)
            if _file_servers != None :
                for fs in _file_servers :
                    FileServers.append(fs.servernames[0])
                self.Logger.debug("get_fileservers: returning from cache %s" % FileServers)
                return FileServers
        self.Logger.debug("refreshing FileServers from live system")
        for na in self._vlDAO.getFsServList(_cfg=self._CFG, _user=_user,noresolve=True) :
            DNSInfo=afs.LOOKUP_UTIL[self._CFG.cell].get_dns_info(na['name_or_ip'])
            FileServers.append(DNSInfo['names'][0])
        self.Logger.debug("get_fileservers: returning %s" % FileServers)
        return FileServers
    
    def get_dbservers(self, _user="", cached=True):
        """
        return a DB-Server-hostname list
        """
        DBServers=[]
        if cached :
            _db_servers = self.DBManager.get_from_cache(DBServer,mustBeUnique=False)
            if _db_servers != None :
                for na in _db_servers :
                    DBServers.append(na.servernames[0])
                return DBServers
        # we need to bootstrap ourselves now from nothing but the Cellname
        # just list of simple dicts hostnames
        DBServList=[]

        # get one fileserver and from that one the DBServList
        # we need to make sure to get the IP
        for f in self._vlDAO.getFsServList(_cfg=self._CFG, _user=_user, noresolve=True ) :
            if  f["name_or_ip"] in self._CFG.ignoreIPList : continue
            break
        _bos_server = self.BosS.pull_bos_server(f["name_or_ip"])
       
        self.Logger.debug("returning %s" % _bos_server.db_servers)
        return _bos_server.db_servers

    def get_ubik_db_info(self, name_or_ip, Port, _user=""):
        """
        return (SyncSite,DBVersion,DBState) tuple for DataBase accessible from Port
        """
        shortInfo = self._ubikDAO.getShortInfo(name_or_ip, Port, _cfg=self._CFG, _user=_user)
        # we get DBState only from SyncSite  
        if not shortInfo["isSyncSite"] : 
             shortInfo = self._ubikDAO.getShortInfo(shortInfo["SyncSite"], Port, _cfg=self._CFG,_user=_user)
        return (shortInfo["SyncSite"],shortInfo["SyncSiteDBVersion"],shortInfo["DBState"])

    def getUsage(self,cached=False) :
        """
        Get Partition info of all Fileservers
        """
        size = used = free = 0 
        return size,used,free

    def getAllocated(self) :
        """
        Get sum of all given quotas of all Volumes
        DBCache only.
        """
        allocated = allocated_stale= 0 
        return allocated,allocated_stale

    def getPTInfo(self,cached=False) :
         """
         Get all sum of all users and groups defined in PTDB
         """
         numUsers = numGroups = 0
         return numUsers,numGroups

    def bulk_getNumVolumes(self) :
        """
        returns all volume count for all servers from DB
        """
        self.Logger.debug("bulk_getNumVolumes:") 
        resDict={}
        conn = self._CFG.DB_ENGINE.connect()
        transa = conn.begin()
        for t in ["RW","RO","BK"] :
            rawsql='SELECT TF.uuid, COUNT(TV.vid) FROM tbl_volume AS TV JOIN tbl_fileserver AS TF on TV.fileserver_uuid = TF.uuid WHERE TV.type="%s" GROUP BY TF.uuid;' % t
            for uuid,count in conn.execute(rawsql).fetchall() :
                if not resDict.has_key(uuid) : resDict[uuid]={"RW" : 0,"RO" : 0, "BK" : 0}
                resDict[uuid][t]=count
                
        transa.commit()
        conn.close()  
        self.Logger.debug("bulk_getNumVolumes: returning %s" % resDict) 
        return resDict
