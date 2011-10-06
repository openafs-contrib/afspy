from afs.dao.FileSystemDAO import FileSystemDAO
from afs.dao.ProcessDAO import ProcessDAO


class FsService (object):
    """
    Provides Service about a FileServer
    ...
    """
    
    _CFG    = None
    
    def __init__(self,conf=None):

        self._srvDAO = FileSystemDAO()
        self._procDAO = ProcessDAO()
        
        # LOAD Configuration from file if exist
        # FIXME Move in decorator
        if conf:
            self._CFG = conf
        else:
            self._CFG = defaultConfig
        
        # DB INIT    
        if self._CFG.DB_CACHE:
            from afs.orm.DbMapper import DbMapper
            self.DbSession     = DbMapper(['Process'])

    ###############################################
    # BNode Section
    ##############################################

    def getRestartTimes(self,name, **kwargs):
            """
            Ask Bosserver about the restart times of the fileserver
            """
            cellname = self._TOKEN._CELL_NAME
            if kwargs.get("cellname"):
                cellname = kwargs.get("cellname")
            self._procDAO.getRestartTimes()
            return
            
    
    ###############################################
    # Volume Section
    ###############################################    
    
    
    def getVolIdList(self,servername, partname=None,**kwargs):
        """
        Retrieve Volume ID List
        """
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
    
    
    def getFileServer(self,servername,**kwargs):
        """
        Retrieve Server 
        """
        cellname = self._TOKEN._CELL_NAME
     
        if kwargs.get("cellname"):
            cellname = kwargs.get("cellname")
            
        server = self._svrDAO.getServer(self,servername,cellname)
        parts = self._svrDAO.getPartList(server.name,cellname)
        server.parts = parts

        return server
