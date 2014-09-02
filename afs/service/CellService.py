import socket,sys

from afs.service.CellServiceError import CellServiceError
from afs.model.Cell import Cell
from afs.model.FileServer import FileServer
from afs.model.DBServer import DBServer
from afs.service.BaseService import BaseService
from afs.service.FSService import FSService
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
        BaseService.__init__(self, conf, LLAList=["fs", "vl", "rx", "ubik"])
        self.FS=FSService()
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
            if cell == None :
                self.Logger.warn("get_cell_info: Cell named %s not in DB." % name)
            else :
                return cell

        # refresh whole new CellObj
        cell = Cell()
        cell.name = cellname
        cell.file_servers = self.get_fileservers()
        cell.db_servers = self.get_dbservers()
        cell.ptdb_sync_site, cell.ptdb_version, cell.ptdb_state = self.get_ubik_db_info(cell.db_servers[0]["hostname"],7002)
        cell.vldb_sync_site, cell.vldb_version, cell.vldb_state = self.get_ubik_db_info(cell.db_servers[0]["hostname"],7003)
        cell.num_vol_rw = 0
        cell.num_vol_ro = 0
        cell.num_vol_bk = 0
        cell.num_vol_offline = 0
        cell.size_kb = 0
        cell.used_kb = 0
        cell.free_kb = 0
        for f in cell.file_servers :
            num_vol_rw, num_vol_ro, num_vol_bk, num_vol_offline = self.FS.getNumVolumes(name_or_ip=f, cached=False)
            cell.num_vol_rw += num_vol_rw
            cell.num_vol_ro += num_vol_ro
            cell.num_vol_bk += num_vol_bk
            cell.num_vol_offline += num_vol_offline
            partitions = self.FS.getPartitions(f) 
            for p in partitions :
                cell.size_kb += partitions[p]["size"]
                cell.free_kb += partitions[p]["free"]
                cell.used_kb += partitions[p]["used"]
        cell.num_users, cell.num_groups = self.getPTInfo()
        # some information are only available if DB_CACHE is used.
        cell.allocated_kb, cell.allocated_stale_kb = -1, -1
        cell.projects = [] # Projects are in DB_CACHE only

        if self._CFG.DB_CACHE :
            for p in self.PS.getProjectList() :
                cell.projects.append(p.name)
            cell.allocated_kb, cell.allocated_stale_kb = self.getAllocated()
            self.Logger.debug("Cell=%s" % cell)
            self.DBManager.set_into_cache(Cell, cell, name=self._CFG.cell)
        return cell
  
    ###############################################
    # Internal helper Section
    ###############################################    
   
    def get_fileservers(self, _user=""):
        """
        Return FileServers as a list of hostnames for each fileserver
        """
        FileServers=[]
        self.Logger.debug("refreshing FileServers from live system")
        for na in self._vlLLA.getFsServList(_cfg=self._CFG, _user=_user, noresolve=True) :
            DNSInfo=afs.LOOKUP_UTIL[self._CFG.cell].get_dns_info(na['name_or_ip'])
            FileServers.append(DNSInfo['names'][0])
        self.Logger.debug("get_fileservers: returning %s" % FileServers)
        return FileServers
    
    def get_dbservers(self, _user=""):
        """
        return a DB-Server-hostname list
        """
        DBServers=[]
        # we need to bootstrap ourselves now from nothing but the Cellname
        # just list of simple dicts hostnames
        DBServList=[]

        # get one fileserver and from that one the DBServList
        # we need to make sure to get the IP
        for f in self._vlLLA.getFsServList(_cfg=self._CFG, _user=_user, noresolve=True ) :
            if  f["name_or_ip"] in self._CFG.ignoreIPList : continue
            break
        _bos_server = self.BosS.pull_bos_server(f["name_or_ip"], cached=False)
       
        self.Logger.debug("returning %s" % _bos_server.db_servers)
        return _bos_server.db_servers

    def get_ubik_db_info(self, name_or_ip, Port, _user=""):
        """
        return (SyncSite,DBVersion,DBState) tuple for DataBase accessible from Port
        """
        shortInfo = self._ubikLLA.get_short_info(name_or_ip, Port, _cfg=self._CFG, _user=_user)
        # we get DBState only from SyncSite  
        if not shortInfo["isSyncSite"] : 
             shortInfo = self._ubikLLA.get_short_info(shortInfo["SyncSite"], Port, _cfg=self._CFG,_user=_user)
        return (shortInfo["SyncSite"],shortInfo["SyncSiteDBVersion"],shortInfo["DBState"])
