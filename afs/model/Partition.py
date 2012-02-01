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
        self.id = None
        self.serv   = serv
        self.name   = name
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


    def __repr__(self):
        return "<Partition('%s',%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s')>" % (self.id, self.serv, self.name, self.device, self.fstype, self.category, self.free, self.size,  self.used, self.perc, self.status, self.description, self.cdate, self.udate , self.sync )
