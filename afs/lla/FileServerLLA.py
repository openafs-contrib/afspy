from afs.lla.BaseLLA import BaseLLA, exec_wrapper
import FileServerLLAParse as PM
from afs.util import misc

class FileServerLLA(BaseLLA) :
    """
    low level access to the FileServer/VolServer pair
    """

    def __init__(self) :
        BaseLLA.__init__(self)
        return

    @exec_wrapper    
    def get_volume_list(self, fileserver, part="", _cfg=None): 
        """
        List Volume entry via vos listvol from vol-server. 
        return list of dictionaries
        """
        CmdList = [_cfg.binaries["vos"],"listvol", "-server", "%s"  % \
            fileserver.servernames[0], "-format", "-cell", "%s" %  _cfg.cell]
        if part != "" :
            part = misc.canonicalize_partition(part)
            CmdList += ["-partition", "%s" % part] 
        return CmdList, PM.get_volume_list
        
    @exec_wrapper    
    def get_volume_id_list(self, fileserver, part="", _cfg=None):
        """
        return  Volumes in partition
        """
        CmdList=[_cfg.binaries["vos"], "listvol", "-server", "%s" % \
            fileserver.servernames[0],  "-fast", "-cell","%s" % _cfg.cell]
        if part != "" :
            part = misc.canonicalize_partition(part)
            CmdList += ["-partition", "%s" % part] 
        return CmdList, PM.get_volume_id_list
 

    @exec_wrapper    
    def get_partitions(self, fileserver, _cfg=None) :
        """
        return list of Partitions-objects
        """       
        CmdList=[_cfg.binaries["vos"], "partinfo", "-server", "%s" % \
            fileserver.servernames[0], "-cell", "%s" % _cfg.cell]
        return CmdList, PM.get_partitions
