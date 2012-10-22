import socket,sys

from afs.exceptions.AfsError import AfsError
from afs.model.Cell import Cell
from afs.model.Volume import Volume
from afs.service.BaseService import BaseService
from afs.service.FsService import FsService
from afs.service.ProjectService import ProjectService
from afs.util import afsutil


class CellService(BaseService):
    """
    Provides Service about a Cell global information.
    The cellname is set in the configuration passed to constructor.
    Thus one instance works only for cell.
    """
    def __init__(self, conf=None):
        BaseService.__init__(self, conf, DAOList=["fs", "bnode","vl", "vol", "rx", "ubik", "dns"])
        self.FS=FsService()
        self.PS=ProjectService()


    def getCellInfo(self, cellname="", _user="", cached=False) :
        """
        return full Cellobject.
        """
        if cellname == "" : cellname = self._CFG.CELL_NAME
        self.Logger.debug("Using cellname : %s " % cellname)
        if cached :
            cell=self.DBManager.getFromCache(Cell,Name = cellname)
            if cell == None :
               self.Logger.info("Cannot get cached Cell. Returning none.")
               return cell
            self.Logger.debug("Cell.udate=%s" % cell.udate)
            # update Sums etc. from DB_CACHE
            cell.Name=cellname
            cell.FileServers=self.getFileServers(cached=True)
            cell.DBServers=self.getDBServers(cached=True)
            cell.numRW = cell.numRO = cell.numBK = cell.numOffline = 0
            for f in cell.FileServers :
                numRW,numRO,numBK,numOffline = self.FS.getNumVolumes(name_or_ip=f,cached=True)
                cell.numRW += numRW
                cell.numRO += numRO
                cell.numBK += numBK
                cell.numOffline += numOffline
            cell.numUsers,cell.numGroups = self.getPTInfo(cached=True)
            cell.allocated,cell.allocated_stale = self.getAllocated()
            cell.size,cell.used,cell.free=self.getUsage(cached=True)
            cell.Projects=[] # Projects are in DB_CACHE only
            for p in self.PS.getProjectList() :
                cell.Projects.append(p.name)
            self.Logger.debug("Cell=%s" % cell)
            self.DBManager.setIntoCache(Cell,cell,Name=self._CFG.CELL_NAME)
            self.Logger.debug("Cell=%s" % cell)
            return cell

        # refresh whole new CellObj
        cell=Cell()
        cell.Name=cellname
        cell.FileServers=self.getFileServers()
        cell.DBServers=self.getDBServers()
        cell.PTDBSyncSite, cell.PTDBVersion,cell.PTDBState=self.getUbikDBInfo(cell.DBServers[0],7002)
        cell.VLDBSyncSite, cell.VLDBVersion,cell.VLDBState=self.getUbikDBInfo(cell.DBServers[0],7003)
        cell.numRW = cell.numRO = cell.numBK = cell.numOffline = 0
        for f in cell.FileServers :
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
            self.DBManager.setIntoCache(Cell,cell,Name=self._CFG.CELL_NAME)
        return cell

    def refreshLiveData(self, cellname="") : 
        """
        update livedata for the cell :
        partition free and used space, DBVersions, list of Servers
        """
        if cellname == "" : cellname = self._CFG.CELL_NAME
        cell=Cell()
        cell.FileServers=self.getFileServers()
        cell.DBServers=self.getDBServers()
        cell.PTDBSyncSite, cell.PTDBVersion,cell.PTDBState=self.getUbikDBInfo(cell.DBServers[0],7002)
        cell.VLDBSyncSite, cell.VLDBVersion,cell.VLDBState=self.getUbikDBInfo(cell.DBServers[0],7003)
        cell.size,cell.used,cell.free=self.getUsage()
        return True 

  
    ###############################################
    # Internal helper Section
    ###############################################    
   
    def getFileServers(self, _user="", cached=False):
        """
        Return FileServers as a list of hostnames for each fileserver
        """
        self.Logger.debug("refreshing FileServers from live system")
        FileServers = []
        cellname=self._CFG.CELL_NAME
        for na in self._vlDAO.getFsServList(cellname, _cfg=self._CFG, _user=_user,noresolve=True) :
            na['hostnames'],na['ipaddrs']=afsutil.getDNSInfo(na['name_or_ip'])
            FileServers.append(na['hostnames'][0])
        self.Logger.debug("returning %s" % FileServers)
        return FileServers
    
    def getDBServers(self, _user="", cached=False):
        """
        return a DB-Server-hostname list
        """
        # we need to bootstrap ourselves now from nothing but the Cellname
        # just list of simple dicts hostnames
        DBServList=[]

        # try DNS _SRV Records from afsdb
        try :
            DBServList=self._dns.getDBServList()
        except:
            pass
        if len(DBServList) == 0 :
            # get one fileserver and from that one the DBServList
            # we need to make sure to get the IP
            for f in self._vlDAO.getFsServList(self._CFG.CELL_NAME, _cfg=self._CFG, _user=_user, noresolve=True ) :
                if  f["name_or_ip"] in self._CFG.ignoreIPList : continue
            DBServList = self._bnodeDAO.getDBServList(f["name_or_ip"], self._CFG.CELL_NAME, _cfg=self._CFG, _user=_user) 
        
        # canonicalize DBServList 
        DBServers=[]
        for na in DBServList :
            na['hostnames'],na['ipaddrs']=afsutil.getDNSInfo(na['hostname'])
            DBServers.append(na['hostnames'][0])
        return DBServers

    def getUbikDBInfo(self, name_or_ip, Port, _user=""):
        """
        return (SyncSite,DBVersion,DBState) tuple for DataBase accessible from Port
        """
        shortInfo = self._ubikDAO.getShortInfo(name_or_ip, Port, self._CFG.CELL_NAME, _cfg=self._CFG, _user=_user)
        # we get DBState only from SyncSite  
        if not shortInfo["isSyncSite"] : 
             shortInfo = self._ubikDAO.getShortInfo(shortInfo["SyncSite"], Port,self._CFG.CELL_NAME, _cfg=self._CFG,_user=_user)
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
