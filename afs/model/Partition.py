from datetime import datetime
from afs.model.BaseModel import BaseModel


class Partition(BaseModel):
    """
    Model object of  a Partition
    """
       
    def __init__(self, id='', serv='', name='', free=0, size=0, used=0, perc=0):
        """
        initialize an empty object
        """
        ## DB - ID
        self.id = None
        self.serv   = serv
        ## canonicalized partition name e.g "ad" for "/vicepad"
        self.name   = name
        ## device-file
        self.device = ''
        self.fstype = ''
        self.category  = ''
        self.free   = free
        self.size   = size
        self.used   = used
        self.perc   = perc
        self.status = ''
        self.description = ''
        self.cdate   = datetime.now()
        self.udate   = datetime.now()
        self.sync    = 0
        self.isComplete = False
