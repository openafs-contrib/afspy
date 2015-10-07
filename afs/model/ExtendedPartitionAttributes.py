"""
Declares model object of extra attributes for a partition
"""

from afs.model.BaseModel import BaseModel

class ExtPartAttr(BaseModel):
    """
    model object of extra attributes for a partition.
    IN DB_CACHE, this is stored in an own table
    """

    def __init__(self) :
        """
        initialize an empty object
        """

        # declare db-internal attributes
        BaseModel.__init__(self)
    
        ##  (fileserver_uuid,name) is foreign key to partition-table
        self.name = ""
        self.fileserver_uuid = ""
        ## Owner of the Partition (string)
        self.owner = ""
        ## json-encoded dict { "projectID" : "numVolumes" }
        ## showing ProjectIDs having numVolumes  volumes on that partition
        self.project_ids_js = '{}'
        self.project_ids = {}
        ## allocated (by quota) size in Kbytes
        self.allocated = -1
        ## stale_allocated, same as allocated,
        ## but for volumes which had not been accessed in $StaleTime days
        self.allocated_stale = -1
        ## number of volumes with unlimited quota
        self.unlimited_volumes = -1
        ## Total number of volumes
        self.num_vol_rw = -1
        self.num_vol_ro = -1
        self.num_vol_bk = -1
        self.num_vol_offline = -1

        self.unmapped_attributes_list = []
