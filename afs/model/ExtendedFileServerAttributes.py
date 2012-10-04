from datetime import datetime
from afs.model.BaseModel import BaseModel


class ExtFileServAttr(BaseModel):
    """
    Model object of extra Attributes to a server.
    IN DB_CACHE, this is stored in an own table
    """
    
    def __init__(self):
        """
        initialize an empty object
        """
         
        ## for db index
        self.id = None
        ## id of server in DB Table tbl_servers
        self.server_id=None
        ## physical Location of the server (string)
        self.location = ""
        ## Owner of the server (string)
        self.owner = ""
        ## custom description about HW etc.
        self.description = ""
        ## creation date of this object
        self.cdate         = datetime.now()
        ## update date of this object
        self.udate         = datetime.now()
        ## list of attributes not to put into the DB
        self.ignAttrList= []
