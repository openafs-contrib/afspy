"""
Declares model object of a fileserver
"""
from afs.model.BaseModel import BaseModel

class FileServer(BaseModel):
    """
    Model object of a fileserver 
    initialize an empty object.
    Partitions are not in the same Table in DB_CACHE as
    Server, so the attribute 'partitions' will be inserted by the FsService
    """

    ## AFS Server UUID
    uuid = ""
    ## list of DNS-hostnames
    servernames_js = '[]'
    servernames = []
    ## list of ipaddrs
    ipaddrs_js = '[]'
    ipaddrs = []
    ## rxdebug version string 
    version = ""
    ## build-date of binary according to rxdebug
    build_date = ""
    ## list of attributes not to put into the DB
    unmapped_attributes_list = [ 'parts', 'ExtServAttr' ]

    def __init__(self):
        """
        base initialiser   
        """
        BaseModel.__init__(self)
        return
