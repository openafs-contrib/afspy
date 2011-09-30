from datetime import datetime
from afs.model.BaseModel import BaseModel


class VolumeOSD(BaseModel):
    """
    Model object of  a Partition
    """
       
    def __init__(self, id='', fquota=0, blockfs=0, block_osd_on=0, block_osd_off=0, pinned=0, osdpolicy=0):
        """
        initialize an empty object
        """
        self.id            = id
        self.fquota        = fquota
        self.blockfs       = blockfs
        self.block_osd_on  = block_osd_on
        self.block_osd_off = block_osd_on
        self.pinned        = pinned
        self.osdpolicy     = osdpolicy
        self.cdate         = datetime.now()
        self.udate         = datetime.now()
        self.sync          = 0


    def __repr__(self):
        return "<VolumeOSD('%s',%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')>" % (self.id, self.fquota, self.blockfs, self.block_osd_on, self.block_osd_off, self.pinned, self.osdpolicy, self.cdate, self.udate, self.sync)
    
 