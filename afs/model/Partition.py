from datetime import datetime
from afs.model.BaseModel import BaseModel


class Partition(BaseModel):
    """
    Model object of  a Partition
    """
       
    def __init__(self, id='', serv_uuid='', name='', free=-1, size=-1, allocated=-1, allocated_stale = -1,used=-1, usedPerc=-1,unLimVol=-1):
        """
        initialize an empty object
        """
        ## DB - ID
        self.id = None
        ## UUID of fileserver
        self.serv_uuid = serv_uuid
        ## canonicalized partition name e.g "ad" for "/vicepad"
        self.name = name
        ## device-file
        self.device = ''
        ## CSV-list of projects-id 
        ## json-encodedlist of projectIDs having volumes on that partition
        self.projectIDs_js       = '[]'
        self.projectIDs=None
        ## free size in Kbytes
        self.free   = free
        ## total size in Kbytes
        self.size   = size
        ## allocated (by quota) size in Kbytes, useless if we have volumes with unlimited quota
        self.allocated = allocated
        ## stale_allocated, same as allocated, 
        ## but for volumes which had not been accessed in $StaleTime days
        self.allocated_stale = allocated_stale
        ## used size in Kbytes
        self.used = used
        ## used size in percentage 
        self.usedPerc = usedPerc
        ## number of volumes with unlimited quota
        self.unLimitedVolumes = unLimVol
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
