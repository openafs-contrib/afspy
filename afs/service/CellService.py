import socket

from afs.exceptions.ORMError import  ORMError
from afs.model.Cell import Cell
from afs.service.BaseService import BaseService
from afs.util import afsutil


class CellService(BaseService):
    """
    Provides Service about a Cell global information.
    The cellname is set in the configuration passed to constructor.
    Thus one instance works only for cell.
    """
    def __init__(self, conf=None):
        BaseService.__init__(self, conf, DAOList=["fs",  "bnode","vl", "vol", "ubik", "dns"])


    def getCellInfo(self, cellname="", cached=False):
        """
        just return internal cell object
        """
        if cached :
            if cellname == "" : cellname = self._CFG.CELL_NAME
            return self.DBCService.getFromCache(Cell,Name = cellname)
        # refresh whole new CellObj
        cell=Cell()
        cell.Name=self._CFG.CELL_NAME
        cell.FileServers=self._getFileServers()
        cell.DBServers=self._getDBServers()
        cell.PTDBSyncSite, cell.PTDBVersion=self._getUbikDBInfo(7002)
        cell.VLDBSyncSite, cell.VLDBVersion=self._getUbikDBInfo(7003)
        if self._CFG.DB_CACHE :
            self.DBCService.setIntoCache(Cell,cell,Name=self._CFG.CELL_NAME)
        return cell
        
    
    ###############################################
    # Internal helper Section
    ###############################################    
   
    def _getFileServers(self):
        """
        Return FileServers as a list of uuid and hostname pair as dict for each fileserver
        """
        self.Logger.debug("refreshing FileServers from live system")
        FileServers =[]
        for na in self._vlDAO.getFsServList(self._CFG.CELL_NAME, self._CFG.Token,noresolve=True) :
            na['hostnames'],na['ipaddrs']=afsutil.getDNSInfo(na['name_or_ip'])
            na.pop('name_or_ip')
            for ip in na['ipaddrs'] :
                if ip in self._CFG.ignoreIPList :
                    self.Logger.debug("ignoring IP=%s" %ip)
                    continue
                else :
                    na['partitions']=self._fsDAO.getPartList(na['ipaddrs'][0], self._CFG.CELL_NAME, self._CFG.Token)
                    FileServers.append(na)
        self.Logger.debug("returning %s" % FileServers)
        return FileServers
    
    def _getDBServers(self):
        """
        return a light-weight DB-Server list
        """
        DBServList=[]

        # we need to bootstrap ourselves now from nothing but the Cellname
        # just list of simple dicts hostnames
        DBServers=[]

        # try DNS _SRV Records from afsdb
        try :
            DBServList=self._dns.getDBServList()
        except:
            pass
        if len(DBServList) == 0 :
            # get one fileserver and from that one the DBServList
            # we need to make sure to get the IP
            for f in self._vlDAO.getFsServList(self._CFG.CELL_NAME, self._CFG.Token, noresolve=True ) :
                if  f["name_or_ip"] in self._CFG.ignoreIPList : continue
            DBServList = self._bnodeDAO.getDBServList(f["name_or_ip"], self._CFG.CELL_NAME) 
        
        for na in DBServList :
            d={'dbserver' : 1, 'clonedbserver' : na['isClone'] }
            DNSInfo= socket.gethostbyname_ex(na['hostname'])
            d['ipaddrs'] =DNSInfo[2] 
            d['hostnames'] = [DNSInfo[0]]+DNSInfo[1]
            DBServers.append(d)
        return DBServers
    
    def _getUbikDBInfo(self, Port):
        """
        return (SyncSite,DBVersion) pair for DataBase accessible from Port
        """
        DBServIP=self._getDBServers()[0]["ipaddrs"][0]
        DBVersion=self._ubikDAO.getDBVersion(DBServIP, Port)
        DBSyncSite=self._ubikDAO.getSyncSite(DBServIP, Port)
        return (DBSyncSite, DBVersion)
    
    ################################################
    # Statistcis DB BASE
    ################################################
    
    #TODO Number of users 
    
    #getTotalVolume()
    
    #Number of Volumes
    
    #Number of partitions
    
    #Total Space
    
    #Number of Servers
    
    #Volume offline
    
    #Volume OK
