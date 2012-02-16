import afs.util.options
import socket, string

from afs.util.AfsConfig import AfsConfig
from afs.exceptions.VLDbError import VLDbError
from afs.exceptions.VolError import VolError
from afs.exceptions.ORMError import  ORMError
from afs.model.Server import Server
from afs.model.Partition import Partition
from afs.util import afsutil
from afs.service.BaseService import BaseService
import afs

class CellService(BaseService):
    """
    Provides Service about a Cell global information.
    The cellname is set in the configuration passed to constructor.
    Thus one instance works only for cell, or you
    need to change self._CFG
    """
    def __init__(self,conf=None):
        BaseService.__init__(self, conf, DAOList=["fs",  "bnode","vl", "vol"])

    ###############################################
    # Server Section
    ###############################################    
   
    def getFsList(self, includeParts=False, db_cache=True):
        """
        Retrieve light-weight Server List
        """
        if db_cache :
            fsList=self._getServListFromCache(includeParts=includeParts, dbserver=False )
            return fsList
            
        nameList = self._vlDAO.getFsServList(self._CFG.CELL_NAME, self._CFG.Token)
        ipList   = self._vlDAO.getFsServList(self._CFG.CELL_NAME, self._CFG.Token, noresolve=True )
        
        # create a dict of uuid -> dns_name mapping
        nameDict = {}
        for el in nameList:
            DNSInfo=socket.gethostbyname_ex(el['name_or_ip'])
            nameDict[el['uuid']] = [DNSInfo[0], ]+DNSInfo[1]
        
        fsList = []
        for el in ipList:
            el['servernames'] = nameDict[el['uuid']]
            el['fileserver'] = 1
            self.Logger.debug("querying %s" % (el['servernames'] [0]))
            # rename attr name_or_ip to proper
            el['ipaddrs'] = [el.pop('name_or_ip'), ]
            serv = Server()
            serv.setByDict(el) 
            # Cache Stuffz
            serv = self._setServIntoCache(serv)
            if includeParts :
                list =self._fsDAO.getPartList(el['ipaddrs'][0], self._CFG.CELL_NAME, self._CFG.Token)
                partList = []
                for elel in list:
                    part = Partition()
                    # inject serv_uuid, to be used as "ForeignKey"
                    elel["serv_uuid"]=el['uuid']
                    part.setByDict(elel)
                    # Cache Stuff
                    part = self._setPartIntoCache(part)
                    partList.append(part)
                serv.parts=partList
            fsList.append(serv)
        return  fsList

    def getDBList(self, serv, db_cache=False):
        """
        return a light-weight DB-Server list
        """
        dbList = []
        if db_cache :
            dbList=self._getServListFromCache(includeParts=False, dbserver=True)
            return dbList
        for na in self._bnodeDAO.getDBServList(serv, self._CFG.CELL_NAME) :
            d={'dbserver' : 1, 'clonedbserver' : na['isClone'] }
            DNSInfo= socket.gethostbyname_ex(na['hostname'])
            d['ipaddrs'] =DNSInfo[2] 
            d['servernames'] = [DNSInfo[0]]+DNSInfo[1]
            # create artitical UUID = "::IP::" (which (shouldbe) unique as well, since the ports are fixed, NAT not considered...)
            # FIXME!! this is not good. we should change our logic
            d['uuid']="::%s::" % (d['ipaddrs'][0], )
            serv = Server()
            serv.setByDict(d) 
            # Cache Stuffz
            serv = self._setServIntoCache(serv)
            dbList.append(serv)
        return dbList
    
    def getFsUUID(self, name_or_ip, db_cache=False):
        """
        returns UUID of a fileserver, which is used as key for server-entries
        in other tables
        """
        uuid=""
        if db_cache :
            uuid=self._getFsUUIDFromCache(name_or_ip)
        else :
            uuid=self._vlDAO.getFsUUID(name_or_ip, self._CFG.CELL_NAME, self._CFG.Token)
        return uuid

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


    def _getPartFromCache(self, serv_uuid, part):
        #RETRIEVE info from  CACHE
        if not self._CFG.DB_CACHE:
            raise ORMError("DB_CACHE not configured")
        
        part = afsutil.canonicalizePartition(part)
        # Do update
        part = self.DbSession.query(Partition).filter(Partition.name == part.name).filter(Partition.serv_uuid == serv_uuid).first()
        return part
        
    def _setPartIntoCache(self,part):
         #STORE info into  CACHE
        if not self._CFG.DB_CACHE:
            return part
        
        partCache = self.DbSession.query(Partition).filter(Partition.name == part.name).filter(Partition.serv_uuid == part.serv_uuid).first()
       
        if partCache:
            partCache.copyObj(part)         
        else:
            self.DbSession.add(part) 
            partCache = part 
        
        self.DbSession.flush() 
        self.DbSession.commit()  
        
        return  partCache
    
    def _delPartFromCache(self,part):
         #STORE info into  CACHE
        if not self._CFG.DB_CACHE:
            return None
        # Do update
        self.DbSession.delete(part)
        
        self.DbSession.commit()
        return 


    def _setServIntoCache(self,serv):
         #STORE info into  CACHE

        if not self._CFG.DB_CACHE:
            return serv
        
        servCache = self.DbSession.query(Server).filter(Server.uuid == serv.uuid).first()
        self.DbSession.flush()
        
        if servCache:
            servCache.copyObj(serv)
        else:
            self.DbSession.add(serv)
            servCache = serv

        self.DbSession.commit()  

        return servCache
    
    def _getServListFromCache(self, includeParts=False, dbserver=False):
        """
        return full Server List+partitions (if we query fileservers)
        """
        #RETRIEVE info from  CACHE
        if not self._CFG.DB_CACHE:
            raise ORMError("DB_CACHE not configured")
        
        # Do update
        servList = self.DbSession.query(Server).filter(Server.dbserver == dbserver).all()
        if not dbserver :
            if includeParts :
                for serv in servList :
                    serv.parts=self.DbSession.query(Partition).filter(Partition.serv_uuid==serv.uuid).all()
        return servList
        
    def _getFsUUIDFromCache(self, name_or_ip):
        """
        return uuid for a hostname or ipaddrs
        """
        #RETRIEVE info from  CACHE
        if not self._CFG.DB_CACHE:
            raise ORMError("DB_CACHE not configured")
        list=self.DbSession.query(Server.uuid, Server.ipaddrs, Server.servernames).all()
        for l in list :
            uuid, ipaddrs, hostnames=l
            if name_or_ip in ipaddrs or name_or_ip in hostnames : break
            
        return uuid
