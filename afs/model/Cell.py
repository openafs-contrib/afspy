"""
Declares Model object of a Cell
"""
from datetime import datetime
from afs.model.BaseModel import BaseModel

class Cell(BaseModel) :
    """
    empty Model for a Cell
    """
        
    ## Database definitions
    ## Cellname
    name = ""
    ## VLDb-Version
    vldb_version = -1
    ## VLDb-syncsite, hostname
    vldb_sync_site = ""
    ## VLDB-State (aka "Recovery state")
    vldb_state = ""
    ## PTDB-Version
    ptdb_version = -1
    ## PTDB-syncsite, hostname
    ptdb_sync_site = ""
    ## PTDB-State (aka "Recovery state")
    ptdb_state = ""
    ## Number of users in PTDB
    num_users = -1
    ## Number of groups in PTDB
    num_groups = -1
    ## Total number of volumes
    num_vol_rw = -1
    num_vol_ro = -1
    num_vol_bk = -1
    num_vol_offline = -1
    ## List of DBServers (hostnames only)
    db_servers = []
    db_servers_js = ""
    ## List of FileServers (hostnames only)
    file_servers = []
    file_servers_js = ""
    ## List of Projects (names only)
    projects = []
    projects_js = ""
    ## Total Size, etc
    size_kb = -1
    used_kb = -1
    free_kb = -1
    allocated_kb = -1
    allocated_stale_kb = -1

    def __init__(self):
        """
        Initializes empty shell
        """
        BaseModel.__init__(self)
