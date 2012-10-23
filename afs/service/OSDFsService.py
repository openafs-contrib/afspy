from afs.service.BaseService import BaseService
from afs.service.FsService import FsService
from afs.model.FileServer import FileServer
from afs.exceptions.AfsError import AfsError
from afs.model.ExtendedVolumeAttributes import ExtVolAttr
from afs.model.ExtendedPartitionAttributes import ExtPartAttr
from afs.model.Volume import Volume
from afs.model.Partition import Partition
from afs.util  import afsutil


class OSDFsService (FsService):
    """
    Provides Service about a FileServer
    """
    
    _CFG    = None
    
    def __init__(self,conf=None):
        BaseService.__init__(self, conf, DAOList=["fs","osdfs", "bnode", "vol", "vl","rx"])

    ###############################################
    # Volume Section
    ###############################################    
    
    def getVolList(self,servername, partname=None, _user="", cached=False):
        """
        Retrieve Volume List
        """
        vols = []
            
        if partname:    
            vols = self._osdfsDAO.getVolList( servername,partname, _cfg=self._CFG, _user=_user)
        else:
            parts = self.getPartitions(servername,cached=cached)
            for part in parts:
                vols += self._osdfsDAO.getVolList(servername,parts[part]["name"], _cfg=self._CFG, _user=_user)
        return vols
