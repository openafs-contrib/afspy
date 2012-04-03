from datetime import datetime
from afs.model.BaseModel import BaseModel


class ExtVolAttr_OSD(BaseModel):
    """
    Model object of  a Partition
    """
       
    def __init__(self, vid=-1, fquota=0, blockfs=0, block_osd_on=0, block_osd_off=0, pinned=0, osdpolicy=0):
        """
        initialize an empty object
        """
        ## RWID of Volume, foreign key to volume-table
        self.vid            = vid
        ## file-quota number of files allowed in this volume
        self.fquota        = fquota
        ## number of blocks stored on Fileserver directly
        self.blockfs       = blockfs
        ## number of blocks which are on-line
        self.block_osd_on  = block_osd_on
        ## number of off-line blocks
        self.block_osd_off = block_osd_on
        ## osd policy
        self.osdpolicy     = osdpolicy
        ## creation date of this object
        self.cdate         = datetime.now()
        ## last update of this object
        self.udate         = datetime.now()
        ## ?? to be removed
        self.sync          = 0
