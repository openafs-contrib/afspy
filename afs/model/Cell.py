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
        ## VLDb-Version
        self.VLDBVersion=-1
        ## VLDb-syncsite, hostname
        self.VLDBSyncSite=""
        ## PTDb-Version
        self.PTDBVersion=-1
        ## PTDb-syncsite, hostname
        self.PTDBSyncSite=""
        ## list of FileServers,json encoded
        self.FileServers=[]
        self.FileServers_js="[]"
        ## list of DB-Servers, json encoded 
        self.DBServers=[]
        self.DBServers_js="[]"
        self.cdate   = datetime.now()
        self.udate   = datetime.now()
        ## list of attributes not to put into the DB
        self.ignAttrList= []
        return
