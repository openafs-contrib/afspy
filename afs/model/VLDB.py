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

    ## list of servers providing this DB
    dbservers_ipaddrs_js = "[]"
    dbservers_ipaddrs = []
    ## syncsite, master-server
    sync_server_ipaddrs = ""
    ## FIXME: add more attributes like registered fileservers etc.
    ## DB-version
    vldb_version = -1

    def __init__(self):
        """
        Initializes empty shell
        """
        BaseModel.__init__(self)
