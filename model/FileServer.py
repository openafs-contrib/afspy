
from afs.factory.ServerTypeFactory import ServerType, BNodeType
from afs.model.BaseModel import BaseModel, Process


class FileServer(BaseModel):
    """
    Model object of a Fileserver
    """
    
    def __init__(self):
        """
        initialize an empty object
        """
        self.id   = ''
        self.name = ""
        self.uuid = ""
        self.version = ""
        self.type = ServerType.FS
        self.proc = Process(BNodeType.fs)
        self.partitions=[]
