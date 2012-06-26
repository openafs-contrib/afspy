
from datetime import datetime
from afs.model.BaseModel import BaseModel


class ExtVolAttr(BaseModel):
    """
    Model object of extra Attributes to a volume.
    IN DB_CACHE, this is stored in an own table
    """
    
    def __init__(self, vid=-1, mincopy=0, owner='', projectIDs=""):
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
        ## json-encodedlist of projectIDs this Volume belongs to
        self.projectIDs_js       = '[]'
        self.projectIDs       = None
        ## if volume should stay on the present server.
        self.pinnedOnServer = 0
        ## creation date of this object
        self.cdate         = datetime.now()
        ## update date of this object
        self.udate         = datetime.now()
        ##  flag if this object is in sync with reality
        self.sync          = 0
        ## list of attributes not to put into the DB
        self.ignAttrList= []
