"""
Declares model object of extra attributes for a volume
"""

from afs.model.BaseModel import BaseModel

class ExtVolAttr(BaseModel):
    """
    Model object of extra Attributes to a volume.
    IN DB_CACHE, this is stored in an own table
    """

    def __init__(self):
        """
        initialize an empty object
        """

        # declare db-internal attributes
        BaseModel.__init__(self)
    
        ## ID of Volume, foreign key to volume-table
        ## SHOULD point to RWID
        self.vid = -1
        ## number of RO required for this volume, overrrides project
        self.num_min_ro = -1
        ## Owner of the volume (string)
        self.owner = ""
        ## json-encodedlist of projectIDs this Volume belongs to
        self.project_ids_js = '[]'
        self.project_ids = []
        ## if volume should stay on the present server.
        self.pinned_on_server = 0
        ## list of attributes not to put into the DB
        self.unmapped_attributes_list = [ 'parts', 'ExtServAttr' ]
