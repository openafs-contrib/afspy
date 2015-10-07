import socket
import sys
import time

from afs.service.CellServiceError import CellServiceError
from afs.model.Cell import Cell
from afs.model.FileServer import FileServer
from afs.model.DBServer import DBServer
from afs.service.BaseService import BaseService
from afs.service.FSService import FSService
from afs.service.DBsService import DBsService
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
        BaseService.__init__(self, conf, LLAList=["bos", "fs", "rx", "ubik", "vl"])
        self.FS=FSService()
        self.DBsS=DBsService()
        self.PS=ProjectService()
        self.BosS=BosService()
        return


    def get_cell_info(self, **kw) :
        """
        return full Cellobject.
        """
        cached = kw.get("cached", True)
        _user = kw.get("_user", "")
        cellname = kw.get("cellname", self._CFG.cell)
        async = kw.get("async", False)
        if cached :
            cell=self.DBManager.get_from_cache(Cell, name = cellname)
            if cell == None :
                self.Logger.warn("get_cell_info: Cellinfo for %s not in DB or outdated." % cellname)
            else :
                return cell

        # refresh whole new CellObj
        cell = Cell()
        cell.name = cellname
        cell.num_vol_rw = 0
        cell.num_vol_ro = 0
        cell.num_vol_bk = 0
        cell.num_vol_offline = 0
        cell.size_kb = 0
        cell.used_kb = 0
        cell.free_kb = 0
        cell.locations = []

        # sort list of file_servers names first by domain, then by hostname
        sorted_file_servers = sorted(self.get_fileservers(), key=lambda x: (".".join(x.split(".")[1:]),x.split(":")[0]))
        sorted_db_servers = sorted(self.get_dbservers(), key=lambda x: (".".join(x.split(".")[1:]),x.split(":")[0]))
        cell.file_servers=[]
        self.Logger.info("get_cell_info: getting details from %d servers." % len(sorted_file_servers))

        tasks = []
        fs_obj = []
        for serv_name in sorted_file_servers :
            self.Logger.debug("get_cell_info: getting details from %s" % serv_name)
            tasks.append(self.FS.get_fileserver(serv_name, cached=cached, async=async))

        if async :
            while 1 :
                for task in tasks :
                    self.FS.task_results[thread_name]     
                    sys.stderr.write("XXX results: %s : %s" % (thread_name, self.FS.task_results[thread_name]) )
                time.sleep(2)
        else :
            fs_objs = tasks
 
        tasks = []    

        for fs in fs_objs :
            if fs.version == -1 : 
                continue
            fs = self.FS.get_details(fs, cached=cached, async=async)

            for p in fs.parts  :
                cell.num_vol_rw += p.ExtAttr.num_vol_rw
                cell.num_vol_ro += p.ExtAttr.num_vol_ro
                cell.num_vol_bk += p.ExtAttr.num_vol_bk
                cell.num_vol_offline += p.ExtAttr.num_vol_offline
                cell.size_kb += p.size_kb
                cell.free_kb += p.free_kb
                cell.used_kb += p.used_kb
            cell.file_servers.append(fs)

        cell.db_servers=[]
        for serv_name in sorted_db_servers :
            self.Logger.debug("get_cell_info: getting details from db-server %s" % serv_name)
            db = self.DBsS.get_db_server(serv_name)
            cell.db_servers.append(db)

        cell.ptdb_sync_site, cell.ptdb_version, cell.ptdb_state = self.get_ubik_db_info(cell.db_servers[0], 7002)
        cell.vldb_sync_site, cell.vldb_version, cell.vldb_state = self.get_ubik_db_info(cell.db_servers[0], 7003)
            
        cell.num_users, cell.num_groups = self.get_pt_info()
        # some information are only available if DB_CACHE is used.
        cell.allocated_kb, cell.allocated_stale_kb = self.get_allocated_space()
        cell.projects = [] # Projects are in DB_CACHE only

        if self._CFG.DB_CACHE :
            for p in self.PS.get_project_list() :
                cell.projects.append(p.name)
            # XXX stale stuff should be refactored out.
            cell.allocated_kb, cell.allocated_stale_kb = self.get_allocated_space()
            self.Logger.debug("Cell=%s" % cell)
            self.DBManager.set_into_cache(Cell, cell, name=self._CFG.cell)
        
        cell.locations = [] # are nowhere stored
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
            dns_info = afs.LOOKUP_UTIL[self._CFG.cell].get_dns_info(na['name_or_ip'])
            FileServers.append(dns_info['names'][0])
        self.Logger.debug("get_fileservers: returning %s" % FileServers)
        return FileServers
    
    def get_dbservers(self, _user=""):
        """
        return a DB-Server-hostname list
        """
        self.Logger.debug("get_dbservers: entering")
        # get one fileserver and from that one the DBServList
        # we need to make sure to get the IP
        for fs_ip in self._vlLLA.get_fileserver_list(_cfg=self._CFG, _user=_user, noresolve=True ) :
            if fs_ip["name_or_ip"] in self._CFG.ignoreIPList : continue
            break
        
        DBServers = []
        for db_serv_info in self._bosLLA.get_db_servers(fs_ip["name_or_ip"]) :
            DBServers.append(db_serv_info["hostname"])

        self.Logger.debug("get_dbservers: returning %s" % DBServers)
        return DBServers

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

