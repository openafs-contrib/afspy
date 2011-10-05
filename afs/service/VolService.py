import afs.util.options

from afs.dao.VolumeDAO import VolumeDAO
from afs.dao.FileServerDAO import FileServerDAO
from afs.model.Volume import Volume
from afs.model.AfsConfig import AfsConfig
from afs.model.VolumeError import VolumeError
from sqlalchemy import func, or_
from afs.util import afsutil

class VolService (object):
    """
    Provides Service about a Volume management.
    The cellname is set in the methods so that we 
    can use this for more than one cell.
    """
    
    def __init__(self,token,conf=None):
        self._TOKEN  = token
        self._volDAO = VolumeDAO()
        self._srvDAO = FileServerDAO()
        
        # LOAD Configuration from file if exist
        # FIXME Move in decorator
        if conf:
            self._CFG = conf
        else:
            self._CFG = AfsConfig(True)
        
        # DB INIT    
        if self._CFG.DB_CACHE :
            import sqlalchemy.orm
            from sqlalchemy import func, or_
            self.DbSession = sqlalchemy.orm.sessionmaker(bind=self._CFG.DB_ENGINE)

    ###############################################
    # Volume Section
    ###############################################    
    """
    Retrieve Volume Group
    """
    def getVolGroup(self, id,  **kwargs):
        cellname = self._TOKEN._CELL_NAME
        
        if kwargs.get("cellname"):
            cellname = kwargs.get("cellname")

        list = self._volDAO.getVolGroup(id, cellname, self._TOKEN );
      
        return list 
       
    
    """
    Retrieve Volume Information by Name or ID
    """
    def getVolume(self, name, serv, part, **kwargs):
        cellname = self._TOKEN._CELL_NAME
        
        if kwargs.get("cellname"):
            cellname = kwargs.get("cellname")
    

        vdict = self._volDAO.getVolume(name, serv, part, cellname, self._TOKEN)
        
        vol = Volume(vdict)
       
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
         
 
    def refreshCache(self, serv, part,**kwargs):
        if not self._CFG.DB_CACHE:
            raise VolError('Error, no db Cache defined ',None)
       
        cellname = self._TOKEN._CELL_NAME
        if kwargs.get("cellname"):
            cellname = kwargs.get("cellname")
            
        part = afsutil.canonicalizePartition(part)
        list = self._volDAO.getVolList( serv, part, cellname, self._TOKEN)
        #Convert into dictionary
        idVolDict = {}
        for el in list:
            idVolDict[el['vid']] = Volume(el)
        session = self.DbSession()
        res  = session.query(Volume).filter(or_(Volume.serv == serv,Volume.servername == serv )).filter(Volume.part == part)
        
        flush = 0
        for el in res:
            print el
            flush +=1
            if idVolDict.has_key(el.vid):
                idVolDict[el.vid].id = el.id
                session.add(idVolDict[el.vid])
                del idVolDict[el.vid]
            else:     
                session.delete(idVolDict[el['vid']]) 
            
            if flush > 100:    
                session.flush() 
        session.flush()
        
        # ADD section 
        for el in idVolDict.keys():
            print el
            session.add(idVolDict[el])    
            if flush > 100:    
                session.flush() 
        session.flush()
        session.commit()
    
    ################################################
    #  Internal Cache Management 
    ################################################


    def _getFromCache(self,id, serv, part):
        #STORE info into  CACHE
        if not self._CFG.DB_CACHE:
            return None
        session = self.DbSession()
        # Do update
        vol = session.query(Volume).filter(Volume.vid == id).filter(Volume.serv == serv).filter(Volume.part == part).first
        
        session.commit()
        session.close()
        return 0,vol
        
    def _setIntoCache(self,vol):
         #STORE info into  CACHE
        if not self._CFG.DB_CACHE:
            return None
        
        session = self.DbSession()
        volCache = session.query(Volume).filter(Volume.vid == vol.vid).filter(or_(Volume.serv == vol.serv,Volume.servername == vol.servername )).filter(Volume.part == vol.part).first()
       
        
        if volCache:
            vol.id = volCache.id
            vol.cdate = volCache.cdate
            session.flush()
        else:
            session.add(vol)   
            
        session.commit()  
        session.close()
       
        
        return 
    
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
    
      
    def _updateCache(self,vol):
        if not self._CFG.DB_CACHE:
            return None
        
        session = self.DbSession()
        volCache = session.query(Volume).filter(Volume.vid == vol.vid).filter(or_(Volume.serv == vol.serv,Volume.servername == vol.servername )).filter(Volume.part == vol.part).first()
       
        
        if volCache:
            vol.id = volCache.id
            vol.cdate = volCache.cdate
            session.flush()
            
        session.commit()  
        session.close()
       
            
    

    
    
    
 
    
