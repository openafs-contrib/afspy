"""
Declares Model object of a bosserver running on a host
"""
from afs.model.BaseModel import BaseModel

class BosServer(BaseModel):
    """
    Model object of a bosserver running on a host
    """

    ## list of DNS-hostnames
    servernames = None
    servernames_js = ""
    ## list of ipaddrs
    ipaddrs = None
    ipaddrs_js = ""
    ## list of superusers
    superusers = None
    superusers_js = ""
    ## list of cell hosts (dbservers)
    db_servers = None
    db_servers_js = ""
    ## rxdebug version string and builddate
    version = ""
    build_date = ""
    ## Date of general restart time
    general_restart_time = ""
    ## Date of newbinary restart time
    newbinary_restart_time = ""
    ## list of attributes not to put into the DB
    ## these contain (lists of) independent objects
    ## or convenience attributes
    ## bnodes: list of BNode objects
    ## servername short for servernames[0]
    unmapped_attributes_list = ['bnodes', 'servernames']

    def __init__(self):
        """
        initialize an empty object.
        """
        BaseModel.__init__(self)
