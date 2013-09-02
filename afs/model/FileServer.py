"""
Declares model object of a fileserver
"""
from afs.model.BaseModel import BaseModel

class FileServer(BaseModel):
    """
    Model object of a fileserver 
    """

    def __init__(self):
        """
        initialize an empty object.
        Partitions are not in the same Table in DB_CACHE as
        Server, so the attribute 'partitions' will be inserted by the FsService
        """
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
        self.unmapped_attributes_list = [ 'BNode', 'parts', 'ExtServAttr' ]
