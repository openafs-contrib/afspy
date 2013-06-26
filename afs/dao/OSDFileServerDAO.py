from afs.dao.BaseDAO import exec_wrapper
from afs.dao.FileServerDAO import FileServerDAO
from afs.util import afsutil
import ParseOSDFileServerDAO as PM

class OSDFileServerDAO(FileServerDAO) :
    """
    low level access to the FileServer/VolServer pair
    """

    def __init__(self) :
        FileServerDAO.__init__(self)
        return

    @exec_wrapper   
    def getVolList(self, serv, part, _cfg=None) :
        """
        List Volume entry via vos listvol from vol-server. 
        return list of dictionaries
        """
        part = afsutil.canonicalizePartition(part)
        CmdList = [_cfg.binaries["vos"],"listvol", "-server", "%s"  % serv , "-part", "%s"  % part ,"-format","-cell", "%s" %  _cfg.CELL_NAME]

        return CmdList,PM.getVolList   
        
        
    @exec_wrapper   
    def getIdVolList(self, server, part, _cfg=None):
        """
        return  Volumes in partition
        """
        part = afsutil.canonicalizePartition(part)
        CmdList=[_cfg.binaries["vos"],"listvol", "-server", "%s" % server, "-partition", "%s" % part ,"-fast" , "-cell","%s" % _cfg.CELL_NAME]
        return CmdList,PM.getIdVolList   
