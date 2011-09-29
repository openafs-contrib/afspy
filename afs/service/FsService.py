class FsService (object):
    """
    Provides Service about a FileServer
    ...
    """
    
    _CFG    = None
    
    def __init__(self,token,conf=None):
        self._TOKEN  = token
        self._srvDAO = FileServerDAO()
        self._procDAO = ProcessDAO()
        
        # LOAD Configuration from file if exist
        # FIXME Move in decorator
        if conf:
            self._CFG = conf
        else:
            self._CFG = AfsConfig("file")
        
        # DB INIT    
        if self._CFG.DB_CACHE:
            from afs.orm.DbMapper import DbMapper
            self.DbSession     = DbMapper(['Process'])
            
    ###############################################
    # Process Section
     ##############################################
        
        def getRestartTimes(self,name, **kwargs):
    
            cellname = self._TOKEN._CELL_NAME
            if kwargs.get("cellname"):
                cellname = kwargs.get("cellname")
            self._procDAO.getRestartTimes()
            return
    
