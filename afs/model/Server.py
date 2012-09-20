from afs.model.BaseModel import BaseModel
from datetime import datetime


class Server(BaseModel):
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
        ## flag if this server is a fileserver
        self.fileserver = False
        ## flag if this server is a databaseserver
        self.dbserver  = False
        ## rxdebug version string
        self.version = ""
        ## physical Location of the server (string)
        self.location = ""
        ## Owner of the server (string)
        self.owner = ""
        ## custom description about HW etc.
        self.description = ''
        ## Date of object creation
        self.cdate   = datetime.now()
        ## Date of last object update
        self.udate   = datetime.now()
        ## list of attributes not to put into the DB
        self.ignAttrList= ['parts']
