import afs.util.options

from afs.dao.VolumeDAO import VolumeDAO
from afs.dao.FileServerDAO import FileServerDAO
from afs.model.Volume import Volume
from afs.model.AfsConfig import AfsConfig
from afs.model.VolumeError import VolumeError

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
    #  Cache Management 
    ################################################

    def _getFromCache(self,id, serv, part):
        #STORE info into  CACHE
        if not self._CFG.DB_CACHE:
            return 1, None
        session = self.DbSession()
        # Do update
        vol = session.query(Volume).filter(Volume.vid == id).filter(Volume.serv == serv).filter(Volume.part == part).first
        
        session.commit()
        session.close()
        return 0,vol
        
    def _setIntoCache(self,vol):
         #STORE info into  CACHE
        if not self._CFG.DB_CACHE:
            return 1, None
        
        session = self.DbSession()
        try :
            session.add(vol) 
            session.commit()  
            session.close()
 
        except:
            session.rollback()
        
        print "add"
        
        return 
    
    def _delCache(self,vol):
         #STORE info into  CACHE
        if not self._CFG.DB_CACHE:
            return 1, None
        session = self.DbSession()
        # Do update
        session.delete(vol)
            
        session.commit()
        session.close()
    
    #MERGE ?    
    def _updateCache(self,vol):
         #STORE info into  CACHE
        if not self._CFG.DB_CACHE:
            return 1
        
        session = self.DbSession()
            
        session.commit()
        session.close()
            
    

    
    
    
 
    
