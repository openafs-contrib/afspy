from afs.service.BaseService import BaseService
from afs.service.FsService import FsService
from afs.model.Server import Server
from afs.exceptions.AfsError import AfsError
from afs.model.ExtendedVolumeAttributes import ExtVolAttr
from afs.model.Volume import Volume
from afs.model.Partition import Partition
from afs.util  import afsutil


class OSDFsService (FsService):
    """
    Provides Service about a FileServer
    """
    
    _CFG    = None
    
    def __init__(self,conf=None):
        BaseService.__init__(self, conf, DAOList=["osdfs", "bnode", "vl"])

    ###############################################
    # Volume Section
    ###############################################    
    
    def getVolList(self,servername, partname=None, cached=False):
        """
        Retrieve Volume List
        """
        vols = []
            
        if partname:    
            vols = self._osdfsDAO.getVolList( servername,partname,self._CFG.CELL_NAME, self._CFG.Token)
        else:
            parts = self.getPartitions(servername,cached=cached)
            for part in parts:
                vols += self._osdfsDAO.getVolList(servername,parts[part]["name"], self._CFG.CELL_NAME, self._CFG.Token)
        return vols
    
    ###############################################
    # File Server Section
    ###############################################
    
    def getPartitions(self, name_or_ip, cached=False):
        """
        return dict ["partname"]={"numROVolumes", "numRWVolumes","usage","free","total" }
        """
        serv_uuid=afsutil.getFSUUIDByName_IP(name_or_ip, self._CFG,cached)
        if cached :
            partDict={}
            for p in self.DBManager.getFromCache(Partition,mustBeunique=False,serv_uuid=serv_uuid) :
                partDict[p.name] = p.getDict()
            return partDict

        partList = self._osdfsDAO.getPartList(name_or_ip, self._CFG.CELL_NAME, self._CFG.Token)
        partDict={}
        for p in partList :
            partDict[p["name"]]=p
        return partDict

    def getVolStati(self, name_or_ip):
        """
        get number of online and offline volumes
        """
        StatDict={"total": -1, "on-line" : -1, "off-line" : -1}
        return StatDict
