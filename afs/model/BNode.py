"""
Declares model object of a bosserver child process (bnode)
"""
from afs.model.BaseModel import BaseModel

class BNode(BaseModel):
    """
    Model object of a bosserver child process (bnode)
    """

    def __init__(self, bnode_type = "N/A", bos_id = -1):
        """
        initialize an empty object
        """
        BaseModel.__init__(self)

        ## DB-ID of bosserver
        self.bos_id = bos_id
        self.bnode_type = bnode_type
        # FIXME : what to do with procs of type cron ?
        # Need to check, man pages dont say much
        self.commands = ''
        self.status = ''
        self.startdate = ''
        self.startcount = ''
        self.exitdate = ''
        self.notifier = ''
        self.state = ''
        self.errorstop  = ''
        self.core = ''
        self.errorexitdate = ''
        self.errorexitdue = ''
        self.errorexitsignal = ''
        self.errorexitcode = ''
