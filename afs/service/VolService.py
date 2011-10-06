import afs.util.options

from afs.dao.VolumeDAO import VolumeDAO
from afs.util.AfsConfig import AfsConfig
from afs.model.Volume import Volume
from afs.exceptions.VolError import VolError
from afs.util import afsutil
from sqlalchemy import func, or_

class VolService (object):
    """
    Provides Service about a Volume management.
    The cellname is set in the methods so that we 
    can use this for more than one cell.
    """
    
    def __init__(self,conf=None):
        
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
            self.DbSession = sqlalchemy.orm.sessionmaker(bind=self._CFG.DB_ENGINE)

    ###############################################
    # Volume Section
    ###############################################    
    #FIXME list or object ... no DICT ! 
    """
    Retrieve Volume Group
    """
    def getVolGroup(self, id ):
    
        list = self._volDAO.getVolGroup(id,  self._CFG.CELL_NAME, self._CFG.Token);
      
        return list 
       
    """
    Retrieve Volume Information by Name or ID
    """
    def getVolume(self, name, serv, part):

        vdict = self._volDAO.getVolume(name, serv, part,  self._CFG.CELL_NAME, self._CFG.Token)
        
        vol = Volume()
        vol.setByDict(vdict)
        self._setIntoCache(vol)
       
        return  vol
    
    """
    Retrieve Volume extended information
    """
    def getVolExtended(self,id):
        pass
 
 
    ################################################
    #  Cache Query 
    ################################################
    def getVolCountByQuery(self,query):
         if not self._CFG.DB_CACHE:
            raise VolError('Error, no db Cache defined ',None)
        
         query._tbl= "Volume"
         session = self.DbSession()
         queryc = query.getQueryCount()
         count  = eval(queryc)
         
         session.close()
         
         return count
 
    def getVolByQuery(self,query):
         if not self._CFG.DB_CACHE:
            raise VolError('Error, no db Cache defined ',None)
        
         query._tbl= "Volume"
         session = self.DbSession()
         query  = query.getQuery()
         res    = eval(query)
         session.close()
         
         return res
 
    def refreshCache(self, serv, part):
        if not self._CFG.DB_CACHE:
            raise VolError('Error, no db Cache defined ',None)
       
        part = afsutil.canonicalizePartition(part)
        list = self._volDAO.getVolList( serv, part, self._CFG.CELL_NAME, self._CFG.Token)
        #Convert into dictionary
        idVolDict = {}
        cUpdate = len(list)
        for el in list:
            idVolDict[el['vid']] = el
            
        session = self.DbSession()
        
        res  = session.query(Volume).filter(or_(Volume.serv == serv,Volume.servername == serv )).filter(Volume.part == part)
        
        flush = 0
        for vol in res:
            flush +=1
            if idVolDict.has_key(vol.vid):
                vol.setByDict(idVolDict[vol.vid])
                del idVolDict[vol.vid]
            else:     
                session.delete(vol) 
            
            if flush > self._CFG.DB_FLUSH:    
                session.flush() 
        session.flush()
        
        # ADD section 
        flush = 0
        for key in idVolDict.keys():
            flush +=1
            vol = Volume()
            vol.setByDict(idVolDict[key])
            session.add(vol)    
            if flush > self._CFG.DB_FLUSH:    
                session.flush() 
        session.flush()
        session.commit()
        
        return cUpdate
    
    ################################################
    #  Internal Cache Management 
    ################################################


    def _getFromCache(self,id, serv, part):
        #STORE info into  CACHE
        if not self._CFG.DB_CACHE:
            return None
        
        part = afsutil.canonicalizePartition(part)
        session = self.DbSession()
        # Do update
        vol = session.query(Volume).filter(Volume.vid == id).filter(Volume.serv == serv).filter(Volume.part == part).first

        session.close()
        return vol
        
    def _setIntoCache(self,vol):
         #STORE info into  CACHE
        if not self._CFG.DB_CACHE:
            return vol
        
        session = self.DbSession()
        volCache = session.query(Volume).filter(Volume.vid == vol.vid).filter(or_(Volume.serv == vol.serv,Volume.servername == vol.servername )).filter(Volume.part == vol.part).first()
       
        
        if volCache:
            volCache.copyObj(vol)
            session.flush()
        else:
            session.add(vol)  
            volCache = vol
        
        session.commit()  
        session.close()
        return volCache
    
    def _delCache(self,vol):
         #STORE info into  CACHE
        if not self._CFG.DB_CACHE:
            return None
        session = self.DbSession()
        # Do update
        session.delete(vol)
            
        session.commit()
        session.close()
    
    #MERGE ?  
    
      
    