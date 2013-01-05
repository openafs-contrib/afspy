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
        ## list of regexes, json encoded
        self.volnameRegEx_js="[]"
        self.volnameRegEx=None
        ## list of additional Volumenames, json encoded
        self.additionalVolnames_js="[]"
        self.additionalVolnames=None
        ## list of excluded Volumenames , json encoded
        self.excludedVolnames_js="[]"
        self.excludedVolnames=None
        ## minimum Size for a Volume
        self.minSize_kB=-1
        ## maximum Size for a volume
        self.maxSize_kB=-1
        ## is this a retention project
        self.NestingLevel=0
        ## contact 
        self.contact = ""
        ## owner 
        self.owner = ""
        ## list of locationIDs for RW-Volumes, json encoded
        self.rw_locations_js="[]"
        self.rw_locations=None
        ## list of locationIDs for RO-Volumes, json encoded
        self.ro_locations_js="[]"
        self.ro_locations=None
        ## list of "server-uuid,partition" pairs for RW-Volumes, json encoded
        self.rw_serverparts_js="[[]]"
        self.rw_serverparts=None
        ## list of "server-uuid,partition" pairs for RO-Volumes, json encoded
        self.ro_serverparts_js="[[]]"
        self.ro_serverparts=None
        ## free form description
        self.description=""
        ## minimum number of RO-replicas
        self.minnum_ro=2
        ## creation date in database
        self.cdate   = datetime.now()
        ## update date in database
        self.udate   = datetime.now()
        ## list of attributes not to put into the DB
        self.ignAttrList= []
