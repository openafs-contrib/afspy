"""
Declares Model object of a database-server
"""
from afs.model.BaseModel import BaseModel

class DBServer(BaseModel):
    """
    Model object of a database-server
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
        self.ipaddr = ""
        ## Flag if it is a clone or real db-server
        self.is_clone = True
        ## type of db : vldb or ptdb
        self.db_type = ""
        ## local version of the DB
        self.local_db_version = ""
        ## rxdebug version string and builddate
        self.version = ""
        self.build_date = ""
        ## list of attributes not to put into the DB
        self.unmapped_attributes_list = ['BNode','ExtServAttr']
