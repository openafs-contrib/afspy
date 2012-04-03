from datetime import datetime
from afs.factory.VolStatusFactory import VolStatus 
from afs.model.BaseModel import BaseModel


class Volume(BaseModel) :
    """
    Provides information about AFS-Volumes and methods to change them
    """
    #FIXME param in the call
    def __init__(self) :
        """
        initializes to an empty Volume
        """
        ## DB internal id
        self.id       = None
        ##Name of the Volume in the VLDB
        self.name     = ''
        ##numerical ID of the Volume, can be RW, RO or BK
        self.vid      = -1
        ## ServerUUID where this volume is stored
        self.serv_uuid   = ""
        ## Partitionname, where this volume is stored.
        self.part     = ""
        ## hostname, not to be used for queries
        self.servername = ""
        ## numerical ID of  RW Volume
        self.parentID = 0
        ## numerical ID of Backup Volume
        self.backupID = 0
        self.cloneID  = 0
        self.inUse         = ""
        self.needsSalvaged = "N"
        self.destroyMe     = "N"
        self.type          = "RW"
        self.creationDate  = datetime.fromtimestamp(0)
        self.accessDate    = datetime.fromtimestamp(0)
        self.updateDate    = datetime.fromtimestamp(0)
        self.backupDate    = datetime.fromtimestamp(0)
        self.copyDate      = datetime.fromtimestamp(0)
        self.flags    = 0
        self.diskused = -1
        self.maxquota = -1
        self.minquota = -1
        self.status   = VolStatus.OK
        self.filecount = 0
        self.dayUse  = 0
        self.weekUse = 0
        self.spare2  = 0 
        self.spare3  = 0
        self.cdate   = datetime.now()
        self.udate   = datetime.now()
        self.sync    = 0    
    
    #@property
    #  create property for timestamp
  

   
