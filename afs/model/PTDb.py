from afs.model.BaseModel import BaseModel

class PTDB(BaseModel) : 
    """
    empty Model for Protection Database
    """
    def __init__(self):
        """
        Initializes empty shell
        """
        ## list of server Objs providing this DB
        self.DBServers=[]
        ## syncsite, master-server
        self.SyncServer=None
        ## ?
        self.numEntries=0
        ## DB-version
        self.DBVersion=-1
        return
