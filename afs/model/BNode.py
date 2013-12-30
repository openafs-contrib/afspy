"""
Declares model object of a bosserver child process (bnode)
"""
from datetime import datetime
from afs.model.BaseModel import BaseModel

class BNode(BaseModel):
    """
    Model object of a bosserver child process (bnode)
    """

    def __init__(self, instance_name = "N/A", bnode_type = "N/A", bos_db_id = -1):
        """
        initialize an empty object
        """
        BaseModel.__init__(self)
        ## DB-ID of owning bosserver
        self.bos_db_id = bos_db_id
        self.instance_name = instance_name
        self.bnode_type = bnode_type
        # FIXME : what to do with procs of type cron ?
        ## list of commands run for this bnode
        self.commands = ''
        self.commands_js = ''
        self.status = ''
        self.start_date = datetime.fromtimestamp(0)
        self.start_count = ''
        self.last_exit_date = datetime.fromtimestamp(0)
        self.notifier = ''
        self.error_stop  = ''
        self.core = ''
        self.error_exit_date = datetime.fromtimestamp(0)
        self.error_exit_due = ''
        self.error_exit_signal = ''
        self.error_exit_code = ''
