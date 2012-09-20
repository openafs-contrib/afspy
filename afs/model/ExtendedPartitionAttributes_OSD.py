
from datetime import datetime
from afs.model.BaseModel import BaseModel


class ExtPartAttr_OSD(BaseModel):
    """
    Model object of extra Attributes to a volume.
    IN DB_CACHE, this is stored in an own table
    """
    
    def __init__(self, serv_uuid="", name="", block_fs=-1,block_osd_on=-1,block_osd_off=-1):
        """
        initialize an empty object
        """
        ## DB internal id
        self.id       = None
        ##  (serv_uuid,name) is foreign key to partition-table
        self.name=name
        self.serv_uuid=serv_uuid
        ## number of blocks stored on Fileserver directly
        self.block_fs       = block_fs
        ## number of blocks which are on-line
        self.block_osd_on  = block_osd_on
        ## number of off-line blocks
        self.block_osd_off = block_osd_off
        ## creation date of this object
        self.cdate         = datetime.now()
        ## update date of this object
        self.udate         = datetime.now()
        ## list of attributes not to put into the DB
        self.ignAttrList= []
