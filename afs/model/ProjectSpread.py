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

        # declare db-internal attributes
        BaseModel.__init__(self)
    
        ## DB ID of Project 
        self.project_id = -1
        ## UUID of FSServer
        self.fileserver_uuid = -1
        ## partition
        self.part = ""
        ## type of volumes
        self.vol_type = ""
        ## number of volumes of that type
        self.num_vol = -1
        ## total used kilobytes 
        self.used_kb = -1
        ## list of attributes not to put into the DB
        self.unmapped_attributes_list = [ 'parts', 'ExtServAttr' ]
