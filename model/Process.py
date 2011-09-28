
from afs.model.BaseModel import BaseModel

class Process(BaseModel):
    
    def __init__(self, BNodeType):
        self.Status=""
        self.lastStart=0
        self.numStarts=0
        self.BNodeType=BNodeType
        # FIXME : what to do with procs of type cron ? Need to check, man pages dont say much
        self.generalRestart=-1
        self.binaryRestart=-1
        self.Commands= []
