
from afs.factory.ServerTypeFactory import ServerType
from afs.model.BaseModel import BaseModel

class FileServer(BaseModel):
    
    
    
    def __init__(self):
        self.id   = ''
        self.name = ""
        self.uuid = ""
        self.version = ""
        self.type = ServerType.FS