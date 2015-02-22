"""
Declares model object of extra attributes for a volume
"""
from afs.model.BaseModel import BaseModel

class ExtVolAttr(BaseModel):
    """
    Model object of extra Attributes to a volume.
    IN DB_CACHE, this is stored in an own table
    """

    ## ID of Volume, foreign key to volume-table
    ## SHOULD point to RWID
    vid = -1
    ## number of RO required for this volume, overrrides project
    num_min_ro = -1
    ## Owner of the volume (string)
    owner = ""
    ## json-encodedlist of projectIDs this Volume belongs to
    project_ids_js = '[]'
    project_ids = []
    ## if volume should stay on the present server.
    pinned_on_server = 0

    def __init__(self):
        """
        initialize an empty object
        """
        BaseModel.__init__(self)
