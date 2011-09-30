
from datetime import datetime
from afs.model.BaseModel import BaseModel


class VolumeExtra(BaseModel):
    """
    Model object of  a Partition
    """
       
    def __init__(self, id='', mincopy=0, owner='', project='', edate=datetime.now(), category=''):
        """
        initialize an empty object
        """
        self.id            = id
        self.mincopy       = mincopy
        self.owner         = owner
        self.project       = project
        self.edate         = edate
        self.category      = category
        self.cdate         = datetime.now()
        self.udate         = datetime.now()
        self.sync          = 0


    def __repr__(self):
        return "<VolumeExtra('%s',%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')>" % (self.id, self.fquota, self.blockfs, self.block_osd_on, self.block_osd_off, self.pinned, self.osdpolicy, self.cdate, self.udate, self.sync)
    
 
