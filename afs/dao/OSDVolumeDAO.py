import types,string
from afs.util import afsutil
from afs.dao.VolumeDAO import VolumeDAO
from afs.dao.BaseDAO import exec_wrapper
import ParseOSDVolumeDAO as PM

class OSDVolumeDAO(VolumeDAO) :
    """
    Provides Methods to query and modify live AFS-Volumes
    Overlay to VolumesDAO adding OSD-functionality
    """
    
    def __init__(self) :
        VolumeDAO.__init__(self)
        return

    @exec_wrapper
    def create(self,VolName,Server,Partition, MaxQuota, MaxFiles,osdpolicy, _cfg=None) :
        """
        create a Volume
        """
        id = 0
        CmdList=[_cfg.binaries["vos"], "create","-server", "%s" % Server, "-partition", "%s" % Partition, "-name", "%s" % VolName , "-maxquota", "%s" % MaxQuota, 
                 "-filequota", "%s" % MaxFiles ,"-osdpolicy" ,osdpolicy, "-cell",  "%s" % _cfg.CELL_NAME]
        return CmdList,PM.create
    
    @exec_wrapper
    def getVolume(self, name_or_id, serv=None, _cfg=None) :
        """
        Volume entry via vos examine from vol-server. 
        """
        CmdList = [_cfg.binaries["vos"],"examine",  "%s"  % name_or_id ,"-format","-cell", "%s" % _cfg.CELL_NAME]
        return CmdList,PM.getVolume
  
    @exec_wrapper 
    def traverse(self,Servers, name_or_id, _cfg=None) :
        if type(Servers) == types.ListType :
            Servers = string.join(Servers," ")
        CmdList=[_cfg.binaries["vos"], "traverse","-server", "%s" % Servers,"-id", "%s" % name_or_id,"-cell", "%s" % _cfg.CELL_NAME]
        return CmdList,PM.traverse
