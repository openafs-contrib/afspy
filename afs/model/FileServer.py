from afs.model.BaseModel import BaseModel
from datetime import datetime


class FileServer(BaseModel):
    """
    Model object of a server of any type
    """
    
    def __init__(self):
        """
        initialize an empty object.
        Partitions are not in the same Table in DB_CACHE as 
        Server, so the attribute 'parts' will be inserted by the FsService
        """
        ## for db index
        self.id = None
        ## AFS Server UUID
        self.uuid = ""
        ## list of DNS-hostnames
        self.servernames = None
        self.servernames_js = ""
        ## list of ipaddrs
        self.ipaddrs = None 
        self.ipaddrs_js = ""
        ## rxdebug version string and builddate
        self.version = ""
        self.builddate = ""
        ## Date of object creation
        self.cdate   = datetime.now()
        ## Date of last object update
        self.udate   = datetime.now()
        ## list of attributes not to put into the DB
        self.ignAttrList= ['BNode','parts','ExtServAttr']
