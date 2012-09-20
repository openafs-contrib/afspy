from datetime import datetime
from afs.model.BaseModel import BaseModel

class Cell(BaseModel) : 
    """
    empty Model for Cell
    """
    def __init__(self):
        """
        Initializes empty shell
        The ignored attributes 'DBServers','FSServers' are lists of Server objects
        for convenience. Same for Projects
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
        ## Total number of volumes
        self.numRW = -1
        self.numRO = -1
        self.numBK = -1
        ## Total Size, etc
        self.size=-1
        self.allocated=-1
        self.allocated_stale=-1
        ## Creation date 
        self.cdate = datetime.now()
        ## update date 
        self.udate = datetime.now()
        ## list of attributes not to put into the DB
        self.ignAttrList= ['DBServers','FSServers','Projects']
        return
