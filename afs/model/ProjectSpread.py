from datetime import datetime
from afs.model.BaseModel import BaseModel


class ProjectSpread(BaseModel):
    """
    Model object of  the Spread of a Project :
    This is a helper table to show how many volumes of what size 
    are stored on different server partition of a single project
    """

    def __init__(self):
        """
        initialize an empty object
        """
        ## DB - ID
        self.id = None
        ## DB ID of Project 
        self.project_id = -1
        ## UUID of FSServer 
        self.serv_uuid = -1
        ## partition 
        self.part = ""
        ## blocks on FileServer
        self.blocks_fs = 0
        ## blocks on online OSD
        self.blocks_osd_on = 0
        ## blocks on offline OSD
        self.blocks_osd_off = 0 
        ## Type of volume: RW, RO or BK
        self.vol_type = ""
        ## Number of Volumes of that type
        self.num_vol = 0
        ## creation date in database
        self.cdate   = datetime.now()
        ## update date in database
        self.udate   = datetime.now()
        ## list of attributes not to put into the DB
        self.ignAttrList= []
        
