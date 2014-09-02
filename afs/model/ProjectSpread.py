"""
Declares model object of the spread of a project
"""
from afs.model.BaseModel import BaseModel

class ProjectSpread(BaseModel):
    """
    Model object of the spread of a project :
    This is a helper table to show how many volumes of what size
    are stored on different server partition of a single project
    """

    ## DB ID of Project 
    project_id = -1
    ## UUID of FSServer
    fileserver_uuid = -1
    ## partition
    part = ""
    ## type of volumes
    vol_type = ""
    ## number of volumes of that type
    num_vol = -1
    ## total used kilobytes 
    used_kb = -1
    ## osd - cruft
    blocks_fs = -1
    blocks_osd_on = -1
    blocks_osd_off = -1

    def __init__(self):
        """
        initialize an empty object
        """
        BaseModel.__init__(self)
