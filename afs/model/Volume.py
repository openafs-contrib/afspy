from datetime import datetime
from afs.factory.VolTypeFactory import VolType
from afs.factory.VolStatusFactory import VolStatus 
from afs.model.BaseModel import BaseModel


class Volume(BaseModel) :
    """
    Provides information about AFS-Volumes and methods to change them
    """
    #FIXME param in the call
    def __init__(self, list=None) :
        """
        initializes to an empty Volume
        """
        ##Name of the Volume in the VLDB
        
        self.name     = ''
        ##numerical ID of the Volume
        self.vid      = -1
        ## Servername, where this volume is stored
        self.serv     = ""
        ## Partitionname, where this volume is stored.
        self.part     = ""
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
        self.diskused = 0
        self.maxquota = 0 
        self.minquota = 0
        self.status   = VolStatus.OK
        self.filecount = 0
        self.dayUse  = 0
        self.weekUse = 0
        self.spare2  = 0 
        self.spare3  = 0
        self.cdate   = datetime.now()
        self.udate   = datetime.now()
        self.sync    = 0
        
        if list:
            self.setValues(list)
    
    
    #@property
    #  create property for timestamp
  
    def __repr__(self):
        return "<Volume('%s','%s', %s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s', '%s', '%s', '%s','%s', '%s', '%s', '%s','%s', '%s', '%s', '%s','%s', '%s')>" % ( self.id, self.name, self.vid, self.serv,  self.part, self.parentID, self.backupID, self.cloneID, self.inUse, self.needsSalvaged, self.destroyMe, self.type,  self.creationDate, self.accessDate, self.updateDate, self.backupDate, self.copyDate, self.flags, self.diskused,  self.maxquota,   self.minquota, self.status,  self.filecount, self.dayUse, self.weekUse, self.spare2, self.spare3 ) 

   
