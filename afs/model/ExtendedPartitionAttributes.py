
from datetime import datetime
from afs.model.BaseModel import BaseModel


class ExtPartAttr(BaseModel):
    """
    Model object of extra Attributes to a volume.
    IN DB_CACHE, this is stored in an own table
    """
    
    def __init__(self, serv_uuid="", name="", owner='', unLimitedVolumes = -1, allocated=-1, allocated_stale=-1 ,projectIDs={}):
        """
        initialize an empty object
        """
        ## DB internal id
        self.id       = None
        ##  (serv_uuid,name) is foreign key to partition-table
        self.name=name
        self.serv_uuid=serv_uuid
        ## Owner of the Partition (string)
        self.owner         = owner
        ## json-encoded dict { "projectID" : "numVolumes" } showing ProjectIDs havingnumVolumes  volumes on that partition
        self.projectIDs_js       = '{}'
        self.projectIDs=None
        ## allocated (by quota) size in Kbytes, useless if we have volumes with unlimited quota
        self.allocated = allocated
        ## stale_allocated, same as allocated, 
        ## but for volumes which had not been accessed in $StaleTime days
        self.allocated_stale = allocated_stale
        ## number of volumes with unlimited quota
        self.unLimitedVolumes = unLimitedVolumes
        ## creation date of this object
        self.cdate         = datetime.now()
        ## update date of this object
        self.udate         = datetime.now()
        ## list of attributes not to put into the DB
        self.ignAttrList= []
