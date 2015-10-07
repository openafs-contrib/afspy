"""
Declares Model object of extra Attributes of a fileserver.
"""

from afs.model.BaseModel import BaseModel


class ExtFileServAttr(BaseModel):
    """
    Model object of extra Attributes of a fileserver.
    IN DB_CACHE, this is stored in an own table
    """

    def __init__(self):
        """
        initialize an empty object
        """

        # declare db-internal attributes
        BaseModel.__init__(self)
    
        ## id of server in DB Table tbl_servers
        self.fileserver_uuid = ""
        ## physical Location of the server (string)
        self.location = ""
        ## Owner of the server (string)
        self.owner = ""
        ## custom description about HW etc.
        self.description = ""
        ## list of attributes not to put into the DB
        self.unmapped_attributes_list = [ ]
