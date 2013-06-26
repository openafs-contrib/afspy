"""
Declares Model object of extra Attributes to a server.
"""
from datetime import datetime
from afs.model.BaseModel import BaseModel


class ExtDBServAttr(BaseModel):
    """
    Model object of extra Attributes to a server.
    IN DB_CACHE, this is stored in an own table
    """

    def __init__(self):
        """
        initialize an empty object
        """

        BaseModel.__init__(self)

        ## id of server in DB Table tbl_servers
        self.server_db_id = None
        ## physical Location of the server (string)
        self.location = ""
        ## Owner of the server (string)
        self.owner = ""
        ## custom description about HW etc.
        self.description = ""
        ## creation date of this object
        self.db_creation_date = datetime.now()
        ## update date of this object
        self.db_update_date  = datetime.now()
