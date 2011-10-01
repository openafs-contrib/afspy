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
    
    def __init__(self,token,conf):
        self._TOKEN  = token
        self._volDAO = VolumeDAO()
        self._srvDAO = FileServerDAO()
        self._CFG = conf
        if self._CFG.DB_CACHE:
            import sqlalchemy.orm
            self.DbSession= sqlalchemy.orm.sessionmaker(bind=self._CFG.DB_ENGINE)
    
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
    
        #ALWAYS REAL DATA on single volume    
        vol=self._volDAO.getVolume(id,cellname, self._TOKEN)
        
        #STORE info into  CACHE
        if self._CFG.DB_CACHE:
            import sqlalchemy.orm
            session=self.DbSession()
            # update by simple delete and re-add
            session.query(Volume.vid, Volume.serv, Volume.part).filter(Volume.vid == vol.vid).filter(Volume.serv == vol.serv).filter(Volume.part == vol.part).delete()
            session.add(vol)
            session.commit()
            session.refresh(vol)
            session.close()
            # detach vol-object from the session
            sqlalchemy.orm.session.make_transient(vol)
        return vol
    
    """
    Retrieve Volume Information by Name
    """
    def getVolByName(self,name, **kwargs):
        cellname = self._TOKEN._CELL_NAME
        
        if kwargs.get("cellname"):
            cellname = kwargs.get("cellname")
    
        #ALWAYS REAL DATA on single volume  
        vol=self._volDAO.getVolume(name, cellname, self._TOKEN)
        
        #STORE info into  CACHE
        if self._CFG.DB_CACHE:
            import sqlalchemy.orm
            session  = self.DbSession()
            # update by simple delete and re-add
            session.query(Volume.vid, Volume.serv, Volume.part).filter(Volume.vid == vol.vid).filter(Volume.serv == vol.serv).filter(Volume.part == vol.part).delete()
            session.add(vol)
            session.commit()
            session.refresh(vol)
            session.close()
            # detach vol-object from the session
            sqlalchemy.orm.session.make_transient(vol)
        return  vol
    
    """
    Retrieve Volume extended information
    """
    def getVolExtended(self,id):
        pass
    
    

    

    
    
    
 
    
