
from afs.factory.ServerTypeFactory import ServerType
from afs.model.BaseModel import BaseModel

class Partition(BaseModel):
    """
    Model object of  a Partition
    """
       
    def __init__(self):
        """
        initialize an empty object
        """
        self.id    = ''
        self.name  = 0
        self.free  = 0
        self.total = 0
        self.used  = 0
