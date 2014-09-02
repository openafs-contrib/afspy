"""
Declares model object of extra attributes for a partition
"""
from afs.model.BaseModel import BaseModel

class ExtPartAttr(BaseModel):
    """
    model object of extra attributes for a partition.
    IN DB_CACHE, this is stored in an own table
    """

    ##  (fileserver_uuid,name) is foreign key to partition-table
    name = ""
    fileserver_uuid = ""
    ## Owner of the Partition (string)
    owner = ""
    ## json-encoded dict { "projectID" : "numVolumes" }
    ## showing ProjectIDs having numVolumes  volumes on that partition
    project_ids_js = '{}'
    project_ids = {}
    ## allocated (by quota) size in Kbytes
    allocated = -1
    ## stale_allocated, same as allocated,
    ## but for volumes which had not been accessed in $StaleTime days
    allocated_stale = -1
    ## number of volumes with unlimited quota
    unlimited_volumes = -1
    ## Total number of volumes
    num_vol_rw = -1
    num_vol_ro = -1
    num_vol_bk = -1
    num_vol_offline = -1

    def __init__(self) :
        """
        initialize an empty object
        """
        BaseModel.__init__(self)
