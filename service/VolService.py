import afs.util.options

from afs.dao.VolumeDAO import VolumeDAO
from afs.dao.FileServerDAO import FileServerDAO
from afs.model.Volume import Volume
from afs.model.AfsConfig import AfsConfig




class VolService (object):
    """
    Provides Service about a Volume management.
    ...
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
        self._volDAO.getVolume(id, vol, cellname)
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
        self._volDAO.getVolume(name, vol, cellname)
        
        #STORE info intp CACHE
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
    
    
    """
    Retrieve Volume List
    """
    def getVolList(self,volQuery,**kwargs):
        pass
    
    """
    Retrieve Volume ID List
    """
    def getVolIdList(self,servername, partname=None,**kwargs):
        cellname = self._TOKEN._CELL_NAME
        vols = []
        if kwargs.get("cellname"):
            cellname = kwargs.get("cellname")
            
        if partname:    
            vols = self._svrDAO.getVolIdList(partname, servername,cellname)
        else:
            parts = self._svrDAO.getPartList(servername,cellname)
            for part in parts:
                vols.extend(self._svrDAO.getVolIdList(part.name, servername,cellname))
    
        return vols
    
    ###############################################
    # File Server Section
    ###############################################
    
    """
    Retrieve Server List
    """
    def getFileServerList(self,srvQuery,**kwargs):
        pass
    
    
    """
    Retrieve Server 
    """
    def getFileServer(self,servername,**kwargs):
        cellname = self._TOKEN._CELL_NAME
     
        if kwargs.get("cellname"):
            cellname = kwargs.get("cellname")
            
        server = self._svrDAO.getServer(self,servername,cellname)
        
        parts = self._svrDAO.getPartList(server.name,cellname)
        server.parts = parts

        return server
    
 
    ###############################################
    # Volume Management Section
    ###############################################
   
    def loadVol(self, servername=None, **kwargs):
        
        # This function is good only with db
        if not self._CFG.DB_CACHE:
             return
         
        cellname = self._TOKEN._CELL_NAME
        
        if kwargs.get("cellname"):
            cellname = kwargs.get("cellname")
        
        volIdList = []
        servers = []
        
        #Create a Server List
        if servername:
            server = self._srvDAO.getServer( servername, cellname)  
            servers.append(server) 
        else:
            servers = self._srvDAO.getServerList(cellname)
        
        #Get DB Session
        session = self.DbSession()
           
            
        for server in servers:
            #List of partitions in the specific server
            parts = self._srvDAO.getPartList(server.name,cellname)
            
            for part in parts:
                volDbList = session.query(Volume).filter(Volume.serv == server.name).filter(Volume.part == part.name)
                #List of volume in the specific server and specific partition
                volSvrList = self._srvDAO.getVolIdList( part.name, server.name, cellname)
                for vol in volDbList: 
                    self._volDAO.getVolume(vol.vid, vol, cellname)
                    if volSvrList.has_key(vol.vid):  
                        volSvrList.pop(vol.vid)
                    else:
                        session.delete(vol)
                    
                session.flush()
                for vid in volSvrList:
                     vol = Volume()
                     self._volDAO.getVolume(vid, vol, cellname)
                session.flush()
            session.commit()      
            
    
       