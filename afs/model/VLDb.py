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
        ## CSV-list of servernames providing this DB
        self.DBServers=""
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
        ## list of attributes not to put into the DB
        self.ignAttrList= []
        return
