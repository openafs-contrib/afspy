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
        """
        BaseModel.__init__(self)
        ## list of DNS-hostnames
        self.servernames = None
        self.servernames_js = ""
        ## list of ipaddrs
        self.ipaddrs = None
        self.ipaddrs_js = ""
        ## list of superusers
        self.superusers = None
        self.superusers_js = ""
        ## list of cell hosts (dbservers)
        self.db_servers = None
        self.db_servers_js = ""
        ## rxdebug version string and builddate
        self.version = ""
        self.build_date = ""
        ## Date of general restart Time
        self.general_restart_time = ""
        ## Date of newbinary restart Time
        self.newbinary_restart_time = ""
        ## list of attributes not to put into the DB
        ## these contain (lists of) independent objects
        ## or convenience attributes
        ## bnodes: list of BNode objects
        ## servername short for servernames[0]
        self.unmapped_attributes_list = ['bnodes', 'servername']
