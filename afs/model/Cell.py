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
        ## VLDB-State (aka "Recovery state")
        self.VLDBState=""
        ## PTDB-Version
        self.PTDBVersion=-1
        ## PTDB-syncsite, hostname
        self.PTDBSyncSite=""
        ## PTDB-State (aka "Recovery state")
        self.PTDBState=""
        ## Number of users in PTDB
        self.numUsers=-1
        ## Number of groups in PTDB
        self.numGroups=-1
        ## Total number of volumes
        self.numRW = -1
        self.numRO = -1
        self.numBK = -1
        self.numOffline = -1
        ## List of DBServers (hostnames only)
        self.DBServers=[]
        self.DBServers_js=""
        ## List of FileServers (hostnames only)
        self.FileServers=[]
        self.FileServers_js=""
        ## List of Projects (names only)
        self.Projects=[]
        self.Projects_js=""
        ## Total Size, etc
        self.size=-1
        self.used=-1
        self.free=-1
        self.allocated=-1
        self.allocated_stale=-1
        ## Creation date 
        self.cdate = datetime.now()
        ## update date 
        self.udate = datetime.now()
        ## list of attributes not to put into the DB
        self.ignAttrList= []
        return
