from datetime import datetime
from afs.model.BaseModel import BaseModel

class Bos(BaseModel):
    """
    Model object of a BOS ()
    """
    
    def __init__(self):
        self.generalRestartTime=""
        self.binaryRestartTime=""
        self.cdate   = datetime.now()
        self.udate   = datetime.now()
        self.sync    = 0
