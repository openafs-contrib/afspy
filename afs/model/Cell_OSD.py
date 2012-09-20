from datetime import datetime
from afs.model.BaseModel import BaseModel

class Cell(BaseModel) : 
    """
    empty Model for Cell
    """
    def __init__(self):
        """
        Initializes empty shell
        The attributes 'DBServers','FSServers' are lists of Server objects
        for convenience
        """
        ## Database definitions
        ## DB - ID
        self.id = None
        ## Cellname
        self.Name=""
        ## OSDDB-Version
        self.OSDDBVersion=-1
        ## OSDDD-syncsite, hostname
        self.OSDDBSyncSite=""
        ## Total number of volumes,
        ## distinguished by OSD and normal
        self.numRW = -1
        self.numRW_OSD = -1
        self.numRO = -1
        self.numRO_OSD = -1
        self.numBK = -1
        self.numBK_OSD = -1
        ## Total Size, etc
        self.size=-1
        self.allocated=-1
        self.allocated_stale=-1
        ## number of blocks stored on Fileserver directly
        self.block_fs       = block_fs
        ## number of blocks which are on-line
        self.block_osd_on  = block_osd_on
        ## number of off-line blocks
        self.block_osd_off = block_osd_off
        ## storage histogram
        ## "vos traverse"
        self.StorageUsage=None
        self.StorageUsage_js=''
        ## Creation date 
        self.cdate = datetime.now()
        ## update date 
        self.udate = datetime.now()
        ## list of attributes not to put into the DB
        self.ignAttrList= []
        return
