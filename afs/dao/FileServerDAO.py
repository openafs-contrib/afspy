from afs.dao.BaseDAO import BaseDAO
from afs.util.Executor import exec_wrapper
import FileServerDAOParse as PM
from afs.util import misc
from afs.model import FileServer

class FileServerDAO(BaseDAO) :
    """
    low level access to the FileServer/VolServer pair
    """

    def __init__(self) :
        BaseDAO.__init__(self)
        return

    @exec_wrapper    
    def getVolList(self, serv, part, _cfg=None): 
        """
        List Volume entry via vos listvol from vol-server. 
        return list of dictionaries
        """
        part = misc.canonicalize_partition(part)
        CmdList = [_cfg.binaries["vos"],"listvol", "-server", "%s"  % serv , "-part", "%s"  % part ,"-format","-cell", "%s" %  _cfg.cell]
        return CmdList,PM.getVolList
        
    @exec_wrapper    
    def getIdVolList(self, server, part, _cfg=None):
        """
        return  Volumes in partition
        """
        part = misc.canonicalize_partition(part)
        CmdList=[_cfg.binaries["vos"],"listvol", "-server", "%s" % server, "-partition", "%s" % part ,"-fast" , "-cell","%s" % _cfg.cell]
        return CmdList,PM.getIdVolList
 

    @exec_wrapper    
    def getPartList(self,  serv, _cfg=None) :
        """
        return list  of  Partitions-dicts
        """       
        CmdList=[_cfg.binaries["vos"],"partinfo", "%s" % serv, "-cell","%s" % _cfg.cell]
        return CmdList,PM.getPartList
