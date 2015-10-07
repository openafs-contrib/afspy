"""
Declares model object of the live-data of a partition
"""

from afs.model.BaseModel import BaseModel

class Partition(BaseModel):
    """
    Model object of the live-data of a partition
    """

    def __init__(self):
        """
        initialize an empty object
        """

        # declare db-internal attributes
        BaseModel.__init__(self)
    
        ## UUID of fileserver
        self.fileserver_uuid = ""
        ## canonicalized partition name e.g "ad" for "/vicepad"
        self.name = ""
        ## free size in Kbytes
        self.free_kb = -1
        ## total size in Kbytes
        self.size_kb = -1
        ## used size in Kbytes
        self.used_kb = -1
        ## list of attributes not to put into the DB
        self.unmapped_attributes_list = [ "ExtAttr" ]
