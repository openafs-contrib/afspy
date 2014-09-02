"""
Declares Model object of extra Attributes of a fileserver.
"""
from datetime import datetime
from afs.model.BaseModel import BaseModel


class ExtFileServAttr(BaseModel):
    """
    Model object of extra Attributes of a fileserver.
    IN DB_CACHE, this is stored in an own table
    """
    ## id of server in DB Table tbl_servers
    server_db_id = None
    ## physical Location of the server (string)
    location = ""
    ## Owner of the server (string)
    owner = ""
    ## custom description about HW etc.
    description = ""

    def __init__(self):
        """
        initialize an empty object
        """
        BaseModel.__init__(self)
