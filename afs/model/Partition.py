from datetime import datetime
from afs.model.BaseModel import BaseModel


class Partition(BaseModel):
    """
    Model object of  a Partition
    """
       
    def __init__(self, id='', serv_uuid='', name='', free=-1, size=-1, used=-1, usedPerc=-1):
        """
        initialize an empty object
        """
        ## DB - ID
        self.id = None
        ## UUID of fileserver
        self.serv_uuid   = serv_uuid
        ## canonicalized partition name e.g "ad" for "/vicepad"
        self.name   = name
        ## device-file
        self.device = ''
        ## CSV-list of projects-id 
        ## json-encodedlist of projectIDs having volumes on that partition
        self.projectIDs_js       = '[]'
        self.projectIDs=None
        ## free size in bytes
        self.free   = free
        ## total size in bytes
        self.size   = size
        ## used size in bytes
        self.used   = used
        ## used perc in bytes
        self.usedPerc   = usedPerc
        ## ?
        self.status = ''
        ## ?
        self.description = ''
        self.cdate   = datetime.now()
        self.udate   = datetime.now()
        ## ??
        self.sync    = 0
        ## ??
        self.isComplete = False
        ## list of attributes not to put into the DB
        self.ignAttrList= []
