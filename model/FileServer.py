
from afs.factory.ServerTypeFactory import ServerType
from afs.factory.BNodeTypeFactory import BNodeType
from afs.model.BaseModel import BaseModel
from afs.model.Process import Process


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
