"""
Declares Model object of a Cell
"""
from datetime import datetime
from afs.model.BaseModel import BaseModel

class Cell(BaseModel) :
    """
    empty Model for a Cell
    """
    def __init__(self):
        """
        Initializes empty shell
        """
        BaseModel.__init__(self)
        
        ## Database definitions
        ## Cellname
        self.name = ""
        ## VLDb-Version
        self.vldb_version = -1
        ## VLDb-syncsite, hostname
        self.vldb_sync_site = ""
        ## VLDB-State (aka "Recovery state")
        self.vldb_state = ""
        ## PTDB-Version
        self.ptdb_version = -1
        ## PTDB-syncsite, hostname
        self.ptdb_sync_site = ""
        ## PTDB-State (aka "Recovery state")
        self.ptdb_state = ""
        ## Number of users in PTDB
        self.num_users = -1
        ## Number of groups in PTDB
        self.num_groups = -1
        ## Total number of volumes
        self.num_rw_vols = -1
        self.num_ro_vols = -1
        self.num_bk_vols = -1
        self.num_offline_vols = -1
        ## List of DBServers (hostnames only)
        self.db_servers = []
        self.db_servers_js = ""
        ## List of FileServers (hostnames only)
        self.file_servers = []
        self.file_servers_js = ""
        ## List of Projects (names only)
        self.projects = []
        self.projects_js = ""
        ## Total Size, etc
        self.size = -1
        self.used = -1
        self.free = -1
        self.allocated = -1
        self.allocated_stale = -1
        return
