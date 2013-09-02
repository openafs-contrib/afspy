"""
declares model object of a volume
"""
from datetime import datetime
from afs.magix import VolStatus
from afs.model.BaseModel import BaseModel

class Volume(BaseModel) :
    """
    Provides information about AFS-Volumes and methods to change them
    """

    def __init__(self) :
        """
        initializes to an empty Volume
        """
        BaseModel.__init__(self)

        ## name of the volume in the VLDB
        self.name = ''
        ## numerical ID of the volume, can be RW, RO or BK
        self.vid = -1
        ## ServerUUID where this volume is stored
        self.fileserver_uuid = ""
        ## Partitionname, where this volume is stored.
        self.part = ""
        ## hostname, not to be used for queries
        self.servername = ""
        ## numerical ID of  RW Volume
        self.parent_id = 0
        ## numerical ID of Backup Volume
        self.backup_id = 0
        self.clone_id  = 0
        self.in_use = ""
        self.needs_salvage = ""
        self.destroy_me = ""
        self.type = ""
        self.creation_date = datetime.fromtimestamp(0)
        self.access_date = datetime.fromtimestamp(0)
        self.backup_date = datetime.fromtimestamp(0)
        self.copy_date = datetime.fromtimestamp(0)
        self.flags = 0
        self.diskused = -1
        self.maxquota = -1
        self.minquota = -1
        self.status = VolStatus.OK
        self.filecount = 0
        self.day_use  = 0
        self.week_use = 0
        self.spare2  = 0
        self.spare3  = 0
        ## list of attributes not to put into the DB
        self.unmapped_attributes_list =  ['ExtAttr', 'OsdAttr']
