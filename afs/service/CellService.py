import afs.util.options

from afs.dao.VolumeDAO import VolumeDAO
from afs.dao.VLDbDAO import VLDbDAO
from afs.util.AfsConfig import AfsConfig
from afs.exceptions.VLDbError import VLDbError
from afs.exceptions.VolError import VolError
from afs.model.Server import Server
from afs.model.Partition import Partition
from afs.util import afsutil


class CellService(object):
    """
    Provides Service about a Cell global information.
    The cellname is set in the methods so that we 
    can use this for more than one cell.
    """
    def __init__(self,conf=None):
        
        self._vlDAO  = VLDbDAO()
        self._volDAO = VolumeDAO()
               
        # LOAD Configuration from file if exist
        # FIXME Move in decorator
        if conf:
            self._CFG = conf
        else:
            self._CFG = afs.defaultConfig
        
        # DB INIT    
        if self._CFG.DB_CACHE :
            import sqlalchemy.orm
            from sqlalchemy import func, or_
            self.DbSession = sqlalchemy.orm.sessionmaker(bind=self._CFG.DB_ENGINE,expire_on_commit=False)

    
    
    ###############################################
    # Server Section
    ###############################################    
    """
    Retrieve Server List
    """
    def getFsList(self):

        nameList = self._vlDAO.getFsServList(self._CFG.CELL_NAME, self._CFG.Token);
        ipList   = self._vlDAO.getFsServList(self._CFG.CELL_NAME, self._CFG.Token, noresolve=True );
        
        nameDict = {}
        for el in nameList:
            nameDict[el['uuid']] = el['serv']
        
        fsList = []
        for el in ipList:
            el['servername'] = nameDict[el['uuid']]
            el['fileserver'] = 1
            serv = Server()
            serv.setByDict(el) 
            print "Before _______________________________"
            print serv
            
            # Cache Stuffz
            serv = self._setServIntoCache(serv)
            fsList.append(serv)
            
        return  fsList
          
    """
    Retrieve Server List
    """
    def getPartList(self, serv,):

        # FIXME look up server ip use only ip 
        list =self._volDAO.getPartList(serv, self._CFG.CELL_NAME, self._CFG.Token )
      
        partList = []
        for el in list:
            part = Partition()
            part.setByDict(el)
            # Cache Stuff
            part = self._setPartIntoCache(part)
            partList.append(part)
        return partList
    
    
    
    ################################################
    #  Internal Cache Management 
    ################################################


    def _getPartFromCache(self, serv, part):
        #STORE info into  CACHE
        if not self._CFG.DB_CACHE:
            return None
        
        part = afsutil.canonicalizePartition(part)
        session = self.DbSession()
        # Do update
        part = session.query(Partition).filter(Partition.part == part).filter(Partition.serv == serv).first

        session.close()
        return part
        
    def _setPartIntoCache(self,part):
         #STORE info into  CACHE
        if not self._CFG.DB_CACHE:
            return part
        
        session = self.DbSession()
        partCache = session.query(Partition).filter(Partition.part == part.part).filter(Partition.serv == part.serv).first()
       
        
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
        servCache = session.query(Server).filter(Server.serv == serv.serv).first()
        session.flush()
        
        if servCache:
            servCache.copyObj(serv)
        else:
            session.add(serv)
            servCache = serv
        
        session.commit()  
        session.close()

        return servCache
    
