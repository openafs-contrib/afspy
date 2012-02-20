from datetime import datetime
from afs.model.BaseModel import BaseModel


class Project(BaseModel):
    """
    Model object of  a Project :
    A project is a group of Volumes defined by the Volume names
    and size.
    A project then defines other attributes such as  (geographical) location,
    contact person, owner(organisation), on which server partition-pairs
    the volumes should reside.
    """
       
    def __init__(self, id='',  name=''):
        """
        initialize an empty object
        """
        ## DB - ID
        self.id = None
        ## name
        self.name   = ""
        ## python list of regexes
        self.volnameRegEx=[]
        ## python list of additional Volumenames
        self.additionalVolnames=[]
        ## python list of excluded Volumenames
        self.excludedVolnames=[]
        ## minimum Size for a Volume
        self.minSize_kB=-1
        ## maximum Size for a volume
        self.maxSize_kB=-1
        ## contact 
        self.contact = ""
        ## owner 
        self.owner = ""
        ## python list of locations for RW-Volumes
        self.rw_locations=[]
        ## python list of locations for RO-Volumes
        self.ro_locations=[]
        ## python list of server/partition pairs for RW-Volumes
        self.rw_serverparts=[]
        ## python list of server/partition pairs for RO-Volumes
        self.ro_serverparts=[]
        ## minimum number of RO-replicas
        self.minnum_ro=-1
        ## creation date in database
        self.cdate   = datetime.now()
        ## update date in database
        self.udate   = datetime.now()
        ## ???
        self.sync    = 0
