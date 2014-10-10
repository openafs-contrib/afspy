"""
declares model object of a volume
"""
from datetime import datetime
from afs.magix import VolStatus
from afs.model.BaseModel import BaseModel

class Volume(BaseModel) :
    """
    Provides information about AFS-Volumes 
    """

    ## name of the volume in the VLDB
    name = ''
    ## numerical ID of the volume, can be RW, RO or BK
    vid = -1
    ## ServerUUID where this volume is stored
    fileserver_uuid = ""
    ## Partitionname, where this volume is stored.
    partition = ""
    ## hostname, not to be used for queries
    servername = ""
    ## numerical ID of RW Volume
    parent_id = 0
    ## numerical ID of RO Volume
    readonly_id = 0
    ## numerical ID of Backup Volume
    backup_id = 0
    clone_id  = 0
    in_use = ""
    needs_salvage = ""
    destroy_me = ""
    type = ""
    creation_date = datetime.fromtimestamp(0)
    access_date = datetime.fromtimestamp(0)
    backup_date = datetime.fromtimestamp(0)
    update_date = datetime.fromtimestamp(0)
    copy_date = datetime.fromtimestamp(0)
    flags = 0
    diskused = -1
    maxquota = -1
    minquota = -1
    status = VolStatus.OK
    filecount = 0
    day_use  = 0
    week_use = 0
    spare2  = 0
    spare3  = 0
    ## list of attributes not to put into the DB
    unmapped_attributes_list =  ['ExtAttr']

    def __init__(self) :
        """
        initializes to an empty Volume
        """
        BaseModel.__init__(self)
