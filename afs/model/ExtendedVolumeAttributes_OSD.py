"""
Declares model object of extra attributes for an osd-volume
"""
from afs.model.BaseModel import BaseModel

class ExtVolAttr_OSD(BaseModel):
    """
    Model object of  a Partition
    """
       
    def __init__(self, vid=-1, filequota=0, files_fs=0,files_osd=0,blocks_fs=0, blocks_osd_on=0, blocks_osd_off=0, osdPolicy=0):
        """
        initialize an empty object
        """
        BaseModel.__init__(self)

        ## ID of Volume, foreign key to volume-table
        self.vid            = vid
        ## file-quota number of files allowed in this volume
        self.filequota        = filequota
        ## number of files still on fileserver
        self.files_fs = files_fs
        ## number of OSD-objects 
        self.files_osd = files_osd
        ## number of blocks stored on Fileserver directly
        self.blocks_fs       = blocks_fs
        ## number of blocks which are on-line
        self.blocks_osd_on  = blocks_osd_on
        ## number of off-line blocks
        self.blocks_osd_off = blocks_osd_off
        ## osd policy
        self.osdPolicy     = osdPolicy
