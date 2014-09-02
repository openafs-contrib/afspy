"""
Declares model object of a bosserver child process (bnode)
"""
from datetime import datetime
from afs.model.BaseModel import BaseModel

class BNode(BaseModel):
    """
    Model object of a bosserver child process (bnode)
    """

    ## DB-ID of owning bosserver
    bos_db_id = -1
    instance_name = ""
    bnode_type = ""
    # FIXME : what to do with procs of type cron ?
    ## list of commands run for this bnode
    commands = ''
    commands_js = ''
    status = ''
    start_date = datetime.fromtimestamp(0)
    start_count = ''
    last_exit_date = datetime.fromtimestamp(0)
    notifier = ''
    error_stop  = ''
    core = ''
    error_exit_date = datetime.fromtimestamp(0)
    error_exit_due = ''
    error_exit_signal = ''
    error_exit_code = ''

    def __init__(self, instance_name = "N/A", bnode_type = "N/A", bos_db_id = -1):
        """
        initialize an empty object
        """
        BaseModel.__init__(self)
        ## DB-ID of owning bosserver
        bos_db_id = bos_db_id
        instance_name = instance_name
        bnode_type = bnode_type
    
