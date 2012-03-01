import socket

from afs.exceptions.ORMError import  ORMError
from afs.model.Cell import Cell
from afs.service.BaseService import BaseService

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
            return self._getFromCache()
        # refresh whole new CellObj
        cell=Cell()
        cell.Name=self._CFG.CELL_NAME
        cell.FileServers=self._getFileServers()
        cell.DBServers=self._getDBServers()
        cell.PTDBSyncSite, cell.PTDBVersion=self._getUbikDBInfo(7002)
        cell.VLDBSyncSite, cell.VLDBVersion=self._getUbikDBInfo(7003)
        if self._CFG.DB_CACHE :
            self._setIntoCache(cell)
        return cell
        
#
# convenience functions 
#

    def getFsUUID(self, name_or_ip, cellname="", cached=False):
        """
        returns UUID of a fileserver, which is used as key for server-entries
        in other tables
        """
        uuid=""
        if cellname == "" :
            cellname = self._CFG.CELL_NAME
        if cached :
            cellCache=self._getFromCache(cellname)
            for serv in cellCache.FileServers :
                if name_or_ip in serv["ipaddrs"] or name_or_ip in serv["hostnames"]: 
                    uuid = serv["uuid"]
                    break
        else :
            uuid=self._vlDAO.getFsUUID(name_or_ip, cellname, self._CFG.Token)
        return uuid
    
    ###############################################
    # Internal helper Section
    ###############################################    
   
    def _getFileServers(self):
        """
        Return FileServers is a list of uuid and hostname pair as dict for each fileserver
        """
        self.Logger.debug("refreshing FileServers from live system")
        FileServers =[]
        for na in self._vlDAO.getFsServList(self._CFG.CELL_NAME, self._CFG.Token) :
            DNSInfo= socket.gethostbyname_ex(na['name_or_ip'])
            na['ipaddrs'] =DNSInfo[2] 
            na['hostnames'] = [DNSInfo[0]]+DNSInfo[1]
            na.pop('name_or_ip')
            na['partitions']=self._fsDAO.getPartList(na['ipaddrs'][0], self._CFG.CELL_NAME, self._CFG.Token)
            FileServers.append(na)
        return  FileServers
    
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
            FSServ = self._vlDAO.getFsServList(self._CFG.CELL_NAME, self._CFG.Token, noresolve=True )[0]["name_or_ip"]
            DBServList = self._bnodeDAO.getDBServList(FSServ, self._CFG.CELL_NAME) 
        
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
    
    
    ################################################
    #  Internal Cache Management 
    ################################################

    def _getFromCache(self, cellname=""):
        if not self._CFG.DB_CACHE:
            raise ORMError("DB_CACHE not configured")
        if cellname == "" :
            cellname = self._CFG.CELL_NAME
        self.Logger.debug("loading Cell '%s' from DB_CACHE"  % cellname)
        cell=self.DbSession.query(Cell).filter(Cell.name == cellname).first()
        return cell
        
    def _setIntoCache(self,cell):
         #STORE info into  CACHE
        if not self._CFG.DB_CACHE:
            raise ORMError("DB_CACHE not configured")
        
        cellCache=self.DbSession.query(Cell).filter(Cell.name == self._CFG.CELL_NAME).first()
        
        if cellCache:
            cellCache.copyObj(cell)
            self.DbSession.flush()
        else:
            cellCache=self.DbSession.merge(cell)  
            self.DbSession.flush()
        
        self.DbSession.commit()  
        return cellCache
