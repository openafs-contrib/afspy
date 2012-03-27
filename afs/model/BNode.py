from datetime import datetime
from afs.model.BaseModel import BaseModel

class BNode(BaseModel):
    """
    Model object of a process (bnode)
    """
    
    def __init__(self, BNodeType="N/A", bos_id=-1):
        """
        initialize an empty object
        """
        ## DB - ID
        self.id = None
        ## DB-ID of bosserver
        self.bos_id = bos_id
        self.BNodeType=BNodeType
        # FIXME : what to do with procs of type cron ? Need to check, man pages dont say much
        self.Commands= []       
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
  
  
