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
   
        # declare db-internal attributes
        BaseModel.__init__(self)
    
        ## for db index
        self.db_id = None
        ## list of DNS-hostnames
        self.servernames = None
        self.servernames_js = ""
        ## list of ipaddrs
        self.ipaddr = ""
        ## Flag if it is a clone or real db-server
        self.is_clone = True
        ## type of db : vldb or ptdb
        self.afsdb_type = ""
        ## local version of the DB
        self.local_afsdb_version = ""
        ## rxdebug version string 
        self.version = ""
        self.build_date = ""
        ## list of attributes not to put into the DB
        self.unmapped_attributes_list= ['BNode', 'ExtServAttr' ]
