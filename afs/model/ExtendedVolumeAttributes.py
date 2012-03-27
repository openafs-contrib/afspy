
from datetime import datetime
from afs.model.BaseModel import BaseModel


class ExtVolAttr(BaseModel):
    """
    Model object of extra Attributes to a volume.
    IN DB_CACHE, this is stored in an own table
    """
    
    def __init__(self, vid=-1, mincopy=0, owner='', projectID=-1):
        """
        initialize an empty object
        """
        ## ID of Volume, foreign key to volume-table
        ## SHOULD point to RWID
        self.vid=vid
        ## num Volumes at least required.
        self.mincopy       = mincopy
        ## Owner of the volume (string)
        self.owner         = owner
        ## projectID this Volume belongs to
        self.projectID       = projectID
        ## if volume should stay on the present server.
        self.pinnedOnServer = 0
        self.cdate         = datetime.now()
        self.udate         = datetime.now()
        self.sync          = 0


    def __repr__(self):
        return "<VolumeExtra('%s',%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')>" % (self.id, self.fquota, self.blockfs, self.block_osd_on, self.block_osd_off, self.pinned, self.osdpolicy, self.cdate, self.udate, self.sync)
