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

    ## list of servers providing this DB
    dbservers_ipaddrs__js = "[]"
    dbservers_ipaddrs = []
    ## syncsite, master-server
    sync_server_ipaddrs = ""
    ## FIXME: add more attributes like e.g. num_groups
    ## DB-version
    ptdb_version = -1

    def __init__(self):
        """
        Initializes empty model object
        """
        BaseModel.__init__(self)
