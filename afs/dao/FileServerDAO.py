from afs.dao.BaseDAO import BaseDAO,execwrapper
import FileServerDAO_parse as PM
from afs.util import afsutil

class FileServerDAO(BaseDAO) :
    """
    low level access to the FileServer/VolServer pair
    """

    def __init__(self) :
        BaseDAO.__init__(self)
        return

    @execwrapper    
    def getVolList(self, serv, part, _cfg=None): 
        """
        List Volume entry via vos listvol from vol-server. 
        return list of dictionaries
        """
        part = afsutil.canonicalizePartition(part)
        CmdList = [_cfg.binaries["vos"],"listvol", "-server", "%s"  % serv , "-part", "%s"  % part ,"-format","-cell", "%s" %  _cfg.CELL_NAME]
        return CmdList,PM.getVolList
        
    @execwrapper    
    def getIdVolList(self, server, part, _cfg=None):
        """
        return  Volumes in partition
        """
        part = afsutil.canonicalizePartition(part)
        CmdList=[_cfg.binaries["vos"],"listvol", "-server", "%s" % server, "-partition", "%s" % part ,"-fast" , "-cell","%s" % _cfg.CELL_NAME]
        return CmdList,PM.getIdVolList
 

    @execwrapper    
    def getPartList(self,  serv, _cfg=None) :
        """
        return list  of  Partitions-dicts
        """       
        CmdList=[_cfg.binaries["vos"],"partinfo", "%s" % serv, "-cell","%s" % _cfg.CELL_NAME]
        return CmdList,PM.getPartList
