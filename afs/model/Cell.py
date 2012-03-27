from datetime import datetime
from afs.model.BaseModel import BaseModel

class Cell(BaseModel) : 
    """
    empty Model for Cell
    """
    def __init__(self):
        """
        Initializes empty shell
        """
        
        ## Database definitions
        ## DB - ID
        self.id = None
        ## Cellname
        self.Name=""
        ## DB-Server python list of DB-ServerDicts
        self.DBServers=[]
        ## VLDb-Version
        self.VLDBVersion=-1
        ## VLDb-syncsite, hostname
        self.VLDBSyncSite=""
        ## PTDb-Version
        self.PTDBVersion=-1
        ## PTDb-syncsite, hostname
        self.PTDBSyncSite=""
        ## FileServer python list of FS-ServerDicts
        self.FileServers=[]
        self.cdate   = datetime.now()
        self.udate   = datetime.now()
        return
