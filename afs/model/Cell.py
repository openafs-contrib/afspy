from afs.model.BaseModel import BaseModel
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Cell(BaseModel, Base) : 
    """
    empty Model for Cell
    """
    def __init__(self):
        """
        Initializes empty shell
        """
        ## Database definitions
        ## Cellname
        self.Name=""
        ## DB-Server CSV-list of hostnames
        self.DbServers=""
        ## VLDb-Version
        self.VLDbVer=-1
        ## VLDb-syncsite, hostname
        self.SyncVLDbServer=""
        ## PTDb-Version
        self.PTDbVer=-1
        ## PTDb-syncsite, hostname
        self.SyncPTDbServer=""
        ## FileServer CSV-list of hostnames
        self.FileServer=[]
        ## linked Cells
        self.linkedCells=[]
        return
