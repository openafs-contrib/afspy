from datetime import datetime
from afs.model.BaseModel import BaseModel


class Partition(BaseModel):
    """
    Model object of the live-data of a partition
    """
       
    def __init__(self, id='', serv_uuid='', name='', free=-1, size=-1, used=-1 ):
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
        ## free size in Kbytes
        self.free   = free
        ## total size in Kbytes
        self.size   = size
        ## used size in Kbytes
        self.used = used
        self.cdate   = datetime.now()
        self.udate   = datetime.now()
        ## list of attributes not to put into the DB
        self.ignAttrList= ['ExtAttr']
