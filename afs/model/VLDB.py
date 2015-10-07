"""
Declares model object for the VLDB
"""

from afs.model.BaseModel import BaseModel

class VLDB(BaseModel) :
    """
    empty model for volume Location Database.
    This defines a logical view on the DB.
    The single copies of it are defined in the
    DBServer model.
    """

    def __init__(self):
        """
        Initializes empty shell
        """

        # declare db-internal attributes
        BaseModel.__init__(self)
    
        ## list of servers providing this DB
        self.dbservers_ipaddrs_js = "[]"
        self.dbservers_ipaddrs = []
        ## syncsite, master-server
        self.sync_server_ipaddrs = ""
        ## FIXME: add more attributes like registered fileservers etc.
        ## DB-version
        self.vldb_version = -1
        ## list of attributes not to put into the DB
        self.unmapped_attributes_list = [ 'parts', 'ExtServAttr' ]
