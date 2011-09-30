import afs.util.options

from afs.dao.VolumeDAO import VolumeDAO
from afs.dao.FileServerDAO import FileServerDAO
from afs.model.Volume import Volume
from afs.model.AfsConfig import AfsConfig


class VolService (object):
    """
    Provides Service about a Volume management.
    The cellname is set in the methods so that we 
    can use this for more than one cell.
    """

    _CFG    = None
    
    def __init__(self,token,conf=None):
        self._TOKEN  = token
        self._volDAO = VolumeDAO()
        self._srvDAO = FileServerDAO()
        
        # LOAD Configuration from file if exist
        # FIXME Move in decorator
        if conf:
            self._CFG = conf
        else:
            self._CFG = AfsConfig("file")
        
        # DB INIT    
        if self._CFG.DB_CACHE:
            from afs.orm.DbMapper import DbMapper
            self.DbSession     = DbMapper(['Volume'])

    ###############################################
    # Volume Section
    ###############################################    
    """
    Retrieve Volume Information by ID
    """
    def getVolByID(self, id, **kwargs):
        cellname = self._TOKEN._CELL_NAME
        
        if kwargs.get("cellname"):
            cellname = kwargs.get("cellname")
    
        vol = Volume()
        #ALWAYS REAL DATA on single volume    
        self._volDAO.getVolume(id, vol, cellname, self._TOKEN)
        return vol
    
    """
    Retrieve Volume Information by Name
    """
    def getVolByName(self,name, **kwargs):
        cellname = self._TOKEN._CELL_NAME
        
        if kwargs.get("cellname"):
            cellname = kwargs.get("cellname")
    
        vol = Volume()
        #ALWAYS REAL DATA on single volume  
        self._volDAO.getVolume(name, vol, cellname, self._TOKEN)
        
        #STORE info into  CACHE
        if self._CFG.DB_CACHE:
            session = self.DbSession()
            # Do update
            
            session.close()
          
        return  vol
    
    """
    Retrieve Volume extended information
    """
    def getVolExtended(self,id):
        pass
    
    

    

    
    
    
 
    
