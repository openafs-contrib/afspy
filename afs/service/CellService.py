import afs.util.options
import logging, socket, string

from afs.dao.VolumeDAO import VolumeDAO
from afs.dao.VLDbDAO import VLDbDAO
from afs.dao.ProcessDAO import ProcessDAO
from afs.dao.FileServerDAO import FileServerDAO
from afs.util.AfsConfig import AfsConfig
from afs.exceptions.VLDbError import VLDbError
from afs.exceptions.VolError import VolError
from afs.exceptions.ORMError import  ORMError
from afs.model.Server import Server
from afs.model.Partition import Partition
from afs.util import afsutil
import afs

class CellService(object):
    """
    Provides Service about a Cell global information.
    The cellname is set in the configuration passed to constructor.
    Thus one instance works only for cell, or you
    need to change self._CFG
    """
    def __init__(self,conf=None):

        # CONF INIT 
        if conf:
            self._CFG = conf
        else:
            self._CFG = afs.defaultConfig

        # LOG INIT
        self.Logger=logging.getLogger("afs.%s" % self.__class__.__name__)
        self.Logger.debug("initializing %s-Object with conf=%s" % (self.__class__.__name__,conf))
        
        # DAO INIT
        self._vlDAO  = VLDbDAO()
        self._volDAO = VolumeDAO()
        self._bosDAO = ProcessDAO()
        self._fsDAO = FileServerDAO()
        # DB INIT    
        if self._CFG.DB_CACHE :
            import sqlalchemy.orm
            from sqlalchemy import func, or_
            self.DbSession = sqlalchemy.orm.sessionmaker(bind=self._CFG.DB_ENGINE,expire_on_commit=False)

    
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

    def getDBList(self, serv, db_cache=True):
        """
        return a light-weight DB-Server list
        """
        dbList = []
        if db_cache :
            dbList=self._getServListFromCache(includeParts=False, dbserver=True)
            return dbList
        for na in self._bosDAO.getDBServList(serv, self._CFG.CELL_NAME) :
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
    
    
    ################################################
    # Statistcis DB BASE
    ################################################
    
    #TODO Number of usrs 
    
    #getTotalVolume()
    
    #Number of Volumes
    
    #Number of partitions
    
    #Total Space
    
    #Number of Servers
    
    #Volume offline
    
    #Volume KO
    
    
    ################################################
    #  Internal Cache Management 
    ################################################


    def _getPartFromCache(self, serv_uuid, part):
        #RETRIEVE info from  CACHE
        if not self._CFG.DB_CACHE:
            raise ORMError("DB_CACHE not configured")
        
        part = afsutil.canonicalizePartition(part)
        session = self.DbSession()
        # Do update
        part = session.query(Partition).filter(Partition.name == part.name).filter(Partition.serv_uuid == serv_uuid).first()

        session.close()
        return part
        
    def _setPartIntoCache(self,part):
         #STORE info into  CACHE
        if not self._CFG.DB_CACHE:
            return part
        
        session = self.DbSession()
        partCache = session.query(Partition).filter(Partition.name == part.name).filter(Partition.serv_uuid == part.serv_uuid).first()
       
        if partCache:
            partCache.copyObj(part)         
        else:
            session.add(part) 
            partCache = part 
        
        session.flush() 
        session.commit()  
        session.close()
        
        return  partCache
    
    def _delPartFromCache(self,part):
         #STORE info into  CACHE
        if not self._CFG.DB_CACHE:
            return None
        session = self.DbSession()
        # Do update
        session.delete(part)
            
        session.commit()
        session.close()


    def _setServIntoCache(self,serv):
         #STORE info into  CACHE

        if not self._CFG.DB_CACHE:
            return serv
        
        session = self.DbSession()
        servCache = session.query(Server).filter(Server.uuid == serv.uuid).first()
        session.flush()
        
        if servCache:
            servCache.copyObj(serv)
        else:
            session.add(serv)
            servCache = serv

        session.commit()  
        session.close()

        return servCache
    
    def _getServListFromCache(self, includeParts=False, dbserver=False):
        """
        return full Server List+partitions (if we query fileservers)
        """
        #RETRIEVE info from  CACHE
        if not self._CFG.DB_CACHE:
            raise ORMError("DB_CACHE not configured")
        
        session = self.DbSession()
        # Do update
        servList = session.query(Server).filter(Server.dbserver == dbserver).all()
        if not dbserver :
            if includeParts :
                for serv in servList :
                    serv.parts=session.query(Partition).filter(Partition.serv_uuid==serv.uuid).all()
        session.close()
        return servList
