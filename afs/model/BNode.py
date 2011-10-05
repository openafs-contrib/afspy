from datetime import datetime
from afs.model.BaseModel import BaseModel

class BNode(BaseModel):
    """
    Model object of a process (bnode)
    """
    
    def __init__(self, BNodeType):
        """
        initialize an empty object
        """
        self.BNodeType=BNodeType
        # FIXME : what to do with procs of type cron ? Need to check, man pages dont say much
        self.Commands= []       
        #FIXME create a map for db
        self.status = ''
        self.startdate = ''
        self.startcount = ''
        self.exitdate   = ''
        self.notifier   = ''
        self.state      = ''
        self.errorstop  = ''
        self.core       = ''
        self.errorexitdate = ''
        self.errorexitdue = ''
        self.errorexitsignal = ''
        self.errorexitcode = ''
        self.cdate   = datetime.now()
        self.udate   = datetime.now()
        self.sync    = 0
  
  