"""
Declares Model object of a bosserver running on a host
"""
from afs.model.BaseModel import BaseModel

class BosServer(BaseModel):
    """
    Model object of a bosserver running on a host
    """

    def __init__(self):
        """
        initialize an empty object.
        Partitions are not in the same Table in DB_CACHE as
        Server, so the attribute 'parts' will be inserted by the FsService
        """
        BaseModel.__init__(self)
        ## list of DNS-hostnames
        self.servernames = None
        self.servernames_js = ""
        ## list of ipaddrs
        self.ipaddrs = None
        self.ipaddrs_js = ""
        ## rxdebug version string and builddate
        self.version = ""
        self.build_date = ""
        ## Date of general restart Time
        self.general_restart_time = ""
        ## Date of binary restart Time
        self.binary_restart_time = ""
        ## list of attributes not to put into the DB
        self.unmapped_attributes_list = ['BNodes']
