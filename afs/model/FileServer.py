"""
Declares model object of a fileserver
"""
from datetime import datetime

from afs.model.BaseModel import BaseModel

class FileServer(BaseModel):
    """
    Model object of a fileserver 
    initialize an empty object.
    Partitions are not in the same Table in DB_CACHE as
    Server, so the attribute 'partitions' will be inserted by the FsService
    """

    def __init__(self):   

        # declare db-internal attributes
        BaseModel.__init__(self)
    
        ## AFS Server UUID
        self.uuid = ""
        ## list of DNS-hostnames
        self.servernames_js = '[]'
        self.servernames = []
        ## list of ipaddrs
        self.ipaddrs_js = '[]'
        self.ipaddrs = []
        ## rxdebug version string 
        self.version = ""
        ## build-date of binary according to rxdebug
        self.build_date = ""
        ## list of attributes not to put into the DB
        self.unmapped_attributes_list = [ 'parts', 'ExtAttr' ]
