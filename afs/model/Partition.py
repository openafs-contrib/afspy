"""
Declares model object of the live-data of a partition
"""
from afs.model.BaseModel import BaseModel

class Partition(BaseModel):
    """
    Model object of the live-data of a partition
    """

    ## UUID of fileserver
    fileserver_uuid = ""
    ## canonicalized partition name e.g "ad" for "/vicepad"
    name = ""
    ## free size in Kbytes
    free_kb = -1
    ## total size in Kbytes
    size_kb = -1
    ## used size in Kbytes
    used_kb = -1
    ## list of attributes not to put into the DB
    unmapped_attributes_list = [ "ExtAttr" ]

    def __init__(self):
        """
        initialize an empty object
        """
        BaseModel.__init__(self)
