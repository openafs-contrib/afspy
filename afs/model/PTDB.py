"""
Declares model object fot protection database
"""

from afs.model.BaseModel import BaseModel

class PTDB(BaseModel) :
    """
    Model for Protection Database.
    This defines a logical view on the DB.
    The single copies of it are defined in the
    DBServer model.
    """

    def __init__(self):
        """
        Initializes empty model object
        """

        # declare db-internal attributes
        BaseModel.__init__(self)
    
        ## list of servers providing this DB
        self.dbservers_ipaddrs__js = "[]"
        self.dbservers_ipaddrs = []
        ## syncsite, master-server
        self.sync_server_ipaddrs = ""
        ## FIXME: add more attributes like e.g. num_groups
        ## DB-version
        self.ptdb_version = -1
        ## list of attributes not to put into the DB
        self.unmapped_attributes_list = [ 'parts', 'ExtServAttr' ]
