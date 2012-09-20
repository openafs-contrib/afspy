from datetime import datetime
from afs.model.BaseModel import BaseModel


class ExtVolAttr_OSD(BaseModel):
    """
    Model object of  a Partition
    """
       
    def __init__(self, vid=-1, filequota=0, files_fs=0,files_osd=0,block_fs=0, block_osd_on=0, block_osd_off=0, osdPolicy=0):
        """
        initialize an empty object
        """
        ## ID of Volume, foreign key to volume-table
        self.vid            = vid
        ## file-quota number of files allowed in this volume
        self.filequota        = filequota
        ## number of files still on fileserver
        self.files_fs = files_fs
        ## number of OSD-objects 
        self.files_osd = files_osd
        ## number of blocks stored on Fileserver directly
        self.block_fs       = block_fs
        ## number of blocks which are on-line
        self.block_osd_on  = block_osd_on
        ## number of off-line blocks
        self.block_osd_off = block_osd_off
        ## osd policy
        self.osdPolicy     = osdPolicy
        ## creation date of this object
        self.cdate         = datetime.now()
        ## last update of this object
        self.udate         = datetime.now()
        ## list of attributes not to put into the DB
        self.ignAttrList= []
