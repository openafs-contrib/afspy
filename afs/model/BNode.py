"""
Declares model object of a bosserver child process (bnode)
"""
from afs.model.BaseModel import BaseModel

class BNode(BaseModel):
    """
    Model object of a bosserver child process (bnode)
    """

    def __init__(self, bnode_type = "N/A", bos_db_id = -1):
        """
        initialize an empty object
        """
        BaseModel.__init__(self)

        ## DB-ID of bosserver
        self.bos_db_id = bos_db_id
        self.bnode_type = bnode_type
        # FIXME : what to do with procs of type cron ?
        # Need to check, man pages dont say much
        self.commands = ''
        self.status = ''
        self.start_date = ''
        self.start_count = ''
        self.last_exit_date = ''
        self.notifier = ''
        self.error_stop  = ''
        self.core = ''
        self.error_exit_date = ''
        self.error_exit_due = ''
        self.error_exit_signal = ''
        self.error_exit_code = ''
