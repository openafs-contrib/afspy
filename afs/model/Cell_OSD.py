from afs.model.BaseModel import BaseModel

class Cell_OSD(BaseModel) : 
    """
    empty Model for Cell
    """
    def __init__(self):
        """
        Initializes empty shell
        The attributes 'DBServers','FSServers' are lists of Server objects
        for convenience
        """
        BaseModel.__init__(self)

        ## Database definitions
        ## Cellname
        self.Name=""
        ## OSDDB-Version
        self.OSDDBVersion=-1
        ## OSDDD-syncsite, hostname
        self.OSDDBSyncSite=""
        ## list of RXOSD-Servers (hostnames only)
        self.RXOSDServers=[]
        self.RXOSDServers_js=""
        ## Total number of volumes,
        ## distinguished by OSD and normal
        self.numRW = -1
        self.numRW_OSD = -1
        self.numRO = -1
        self.numRO_OSD = -1
        self.numBK = -1
        self.numBK_OSD = -1
        ## Total Size, etc
        ## distinguished by OSD and normal
        self.size=-1
        self.allocated=-1
        self.allocated_stale=-1
        self.size_OSD=-1
        self.allocated_OSD=-1
        self.allocated_stale_OSD=-1
        ## number of blocks stored on Fileserver directly
        self.blocks_fs       = -1
        ## number of blocks which are on-line
        self.blocks_osd_on  = -1
        ## number of off-line blocks
        self.blocks_osd_off = -1
        ## storage histogram
        ## "vos traverse"
        self.StorageUsage=None
        self.StorageUsage_js=''
