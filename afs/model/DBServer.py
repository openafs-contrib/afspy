from afs.model.BaseModel import BaseModel
from datetime import datetime


class DBServer(BaseModel):
    """
    Model object of a server of any type
    """
    
    def __init__(self):
        """
        initialize an empty object.
        """
        ## for db index
        self.id = None
        ## list of DNS-hostnames
        self.servernames = None
        self.servernames_js = ""
        ## list of ipaddrs
        self.ipaddr = "" 
        ## Flag if it is a clone or real db-server
        self.isClone = True
        ## type of db : vldb or ptdb
        self.type=""
        ## local version of the DB
        self.localDBVersion=""
        ## rxdebug version string and builddate
        self.version = ""
        self.builddate = ""
        ## Date of object creation
        self.cdate   = datetime.now()
        ## Date of last object update
        self.udate   = datetime.now()
        ## list of attributes not to put into the DB
        self.ignAttrList= ['BNode','ExtServAttr']
