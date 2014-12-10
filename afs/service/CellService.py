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
            fs = self.FS.get_fileserver(f, cached=cached)
            fs = self.FS.get_details(fs, cached=cached)
            for p in fs.parts  :
                cell.num_vol_rw += p.ExtAttr.num_vol_rw
                cell.num_vol_ro += p.ExtAttr.num_vol_ro
                cell.num_vol_bk += p.ExtAttr.num_vol_bk
                cell.num_vol_offline += p.ExtAttr.num_vol_offline
                cell.size_kb += p.size_kb
                cell.free_kb += p.free_kb
                cell.used_kb += p.used_kb
        cell.num_users, cell.num_groups = self.get_pt_info()
        # some information are only available if DB_CACHE is used.
        cell.allocated_kb, cell.allocated_stale_kb = self.get_allocated_space()
        cell.projects = [] # Projects are in DB_CACHE only

        if self._CFG.DB_CACHE :
            for p in self.PS.getProjectList() :
                cell.projects.append(p.name)
            # XXX stale stuff should be refactored out.
            cell.allocated_kb, cell.allocated_stale_kb = self.get_allocated_space()
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
        FileServers = []
        self.Logger.debug("refreshing FileServers from live system")
        for na in self._vlLLA.get_fileserver_list(_cfg=self._CFG, _user=_user, noresolve=True) :
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
        for f in self._vlLLA.get_fileserver_list(_cfg=self._CFG, _user=_user, noresolve=True ) :
            if f["name_or_ip"] in self._CFG.ignoreIPList : continue
            break

        _bos_server = self.BosS.get_bos_server(f["name_or_ip"], cached=False)
       
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
        return (shortInfo["SyncSite"], shortInfo["SyncSiteDBVersion"], shortInfo["DBState"])

    def get_pt_info(self) :
        """
        return (num_users, num_groups) of the cell
        """
        return (-1, -1)

    def get_allocated_space(self) :
        """
        return ()
        """
        return (-1, -1)
