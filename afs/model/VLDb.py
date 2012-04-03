from afs.model.BaseModel import BaseModel
from datetime import datetime

class VLDB(BaseModel) : 
    """
    empty Model for Volume Location Database
    """
    def __init__(self):
        """
        Initializes empty shell
        """
        ## list of server Objs providing this DB
        self.DBServers=[]
        ## syncsite, master-server
        self.SyncServer=None
        ## ?
        self.numEntries=0
        ## DB-version
        self.DBVersion=-1
        ## creation 
        self.cdate   = datetime.now()
        ## update
        self.udate   = datetime.now()
        return
