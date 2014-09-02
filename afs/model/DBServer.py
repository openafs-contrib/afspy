"""
Declares Model object of a database-server
"""
from afs.model.BaseModel import BaseModel

class DBServer(BaseModel):
    """
    Model object of a database-server
    """

    ## for db index
    db_id = None
    ## list of DNS-hostnames
    servernames = None
    servernames_js = ""
    ## list of ipaddrs
    ipaddr = ""
    ## Flag if it is a clone or real db-server
    is_clone = True
    ## type of db : vldb or ptdb
    afsdb_type = ""
    ## local version of the DB
    local_afsdb_version = ""
    ## rxdebug version string 
    version = ""
    build_date = ""
    ## list of attributes not to put into the DB
    unmapped_attributes_list= ['BNode', 'ExtServAttr' ]

    def __init__(self):
        """
        initialize an empty object.
        """
        BaseModel.__init__(self)
