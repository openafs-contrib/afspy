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

    def __init__(self):
        """
        initialize an empty object
        """
        BaseModel.__init__(self)

        ## DB ID of Project
        self.project_id = -1
        ## UUID of FSServer
        self.fileserver_uuid = -1
        ## partition
        self.part = ""
        ## Dict of kb on FileServer by type
        self.used_kb_by_type_js = '{"RW" : -1,  "RO" : -1,  "BK" : -1 }'
        self.used_kb_by_type = {"RW" : -1,  "RO" : -1,  "BK" : -1 }
        ## Dict of number of Volumes of all types
        self.num_vol_by_type_js = '{"RW" : -1,  "RO" : -1,  "BK" : -1 }'
        self.num_vol_by_type = {"RW" : -1,  "RO" : -1,  "BK" : -1 }
