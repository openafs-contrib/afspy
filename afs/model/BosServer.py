"""
Declares Model object of a bosserver running on a host
"""
from afs.model.BaseModel import BaseModel
import logging

class BosServer(BaseModel):
    """
    Model object of a bosserver running on a host
    """

    def __init__(self):
        """
        initialize an empty object.
        """
   
        # declare db-internal attributes
        BaseModel.__init__(self)
    
        ## list of DNS-hostnames
        self.servernames = []
        self.servernames_js = ""
        ## list of ipaddrs
        self.ipaddrs = []
        self.ipaddrs_js = ""
        ## list of superusers
        self.superusers = []
        self.superusers_js = ""
        ## list of cell hosts (dbservers)
        self.db_servers = []
        self.db_servers_js = ""
        ## rxdebug version string and builddate
        self.version = ""
        self.build_date = ""
        ## dict containing general and binary restart times
        self.restart_times = {}
        self.restart_times_js = "{}"
        ## list of attributes not to put into the DB
        ## these contain (lists of) independent objects
        ## or convenience attributes
        ## bnodes: list of BNode objects
        ## servername short for servernames[0]
        self.unmapped_attributes_list = ['bnodes']
