
from afs.factory.ServerTypeFactory import ServerType
from afs.factory.BNodeTypeFactory import BNodeType
from afs.model.BaseModel import BaseModel
from datetime import datetime


class Server(BaseModel):
    """
    Model object of a server of any type
    """
    
    def __init__(self):
        """
        initialize an empty object
        """
        self.id = None
        self.uuid = ""
        self.servernames = []
        self.ipaddrs = []
        self.fileserver = 0
        self.parts={}
        self.dbserver  = 0
        self.clonedbserver = 0
        self.confserver = 0
        self.distserver = 0
        self.version = ""
        self.category = ''
        self.status   = ''
        self.id_location = 0
        self.description = ''
        self.cdate   = datetime.now()
        self.udate   = datetime.now()
        self.sync    = 0


    def __repr__(self):
        return "<Server('%s',%s', '%s', '%s','%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s')>" %   (self.id,  self.uuid, self.servernames, self.ipaddrs, self.fileserver, self.parts, self.dbserver, self.clonedbserver, self.confserver, self.distserver, self.version, self.category, self.status, self.id_location, self.description, self.cdate, self.udate, self.sync)     
