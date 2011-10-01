from afs.model.BaseModel import BaseModel

class Cell(BaseModel) : 
    """
    empty Model for Cell
    """
    def __init__(self):
        """
        Initializes empty shell
        """
        ## list of FSserver
        self.VLDB=None
        self.PTDB=None
        ## syncsite
        self.SyncServer=None
        self.linkedCells=[]
        return
