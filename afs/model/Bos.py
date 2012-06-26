from datetime import datetime
from afs.model.BaseModel import BaseModel

class Bos(BaseModel):
    """
    Model object of a BOS ()
    """
    
    def __init__(self, servername="NA"):
        ## DB - ID
        self.id = None
        ## DNS-Name
        self.servername=servername
        self.generalRestartTime=""
        self.binaryRestartTime=""
        self.cdate   = datetime.now()
        self.udate   = datetime.now()
        self.sync    = 0
        ## list of attributes not to put into the DB
        self.ignAttrList= []
