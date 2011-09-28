
from afs.factory.ServerTypeFactory import ServerType, BNodeType
from afs.model.BaseModel import BaseModel, Process


class FileServer(BaseModel):
    
    def __init__(self):
        self.id   = ''
        self.name = ""
        self.uuid = ""
        self.version = ""
        self.type = ServerType.FS
        self.proc = Process(BNodeType.fs)
