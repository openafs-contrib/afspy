

from afs.model.BaseModel import BaseModel


class VolumeGroup(BaseModel) :
    
    def __init__(self):
        ## DB - ID
        self.id = None
        ## name of RW-volume
        self.name=""
        ## json encoded RW volume dict
        self.RW_js = ""
        ## to be decoded RW volume dict, not mapped to DB
        self.RW = {}
        ## json encoded list of RO-Volume dicts
        self.RO_js = ""
        ## to be decoded list of RO volume dict, not mapped to DB
        self.RO = []
        ## json encoded BK volume dict
        self.BK_js = ""
        ## to be decoded BK volume dict, not mapped to DB
        self.BK = {}
        ## list of attributes not to put into the DB
        self.ignAttrList= []
        return
    

        
    
