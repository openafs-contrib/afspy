from afs.dao.BaseDAO import BaseDAO, exec_wrapper
import ParseVolumeDAO as PM
from afs.util import afsutil

class VolumeDAO(BaseDAO) :
    """
    Provides Methods to query and modify live AFS-Volumes
    """
    
    def __init__(self) :
        BaseDAO.__init__(self)
        return

    @exec_wrapper
    def move(self,ID, SrcServer, SrcPartition, DstServer,DstPartition, _cfg=None ) :
        """
        moves a volume to a new Destination. 
        """
        CmdList=[_cfg.binaries["vos"], "move","%s" % ID, "-fromserver", "%s" % SrcServer, "-frompartition" , "%s" % SrcPartition, "-toserver" , "%s" % DstServer, "-topartition", "%s" % DstPartition,  "-cell",  "%s" % _cfg.cell ]
        return CmdList,PM.move

    @exec_wrapper
    def release(self,ID, _cfg=None) :
        """
        release this volume
        """
        CmdList=[_cfg.binaries["vos"], "release","%s" % ID, "-cell",  "%s" % _cfg.cell]
        return CmdList,PM.release
    
    @exec_wrapper
    def setBlockQuota(self,ID, BlockQuota, _cfg=None) :
        """
        sets Blockquota
        """
        CmdList=[_cfg.binaries["vos"], "setfield","-id" ,"%s" % ID,"-maxquota","%s" % BlockQuota, "-cell",  "%s" % _cfg.cell]
        return CmdList,PM.setBlockQuota
        
    @exec_wrapper
    def dump(self,ID, DumpFile, _cfg=None) :
        """
        Dumps a volume into a file
        """
        CmdList=[_cfg.binaries["vos"], "dump","-id" ,"%s" % ID, "-file" ,"%s" % DumpFile, "-cell",  "%s" % _cfg.cell]
        return CmdList,PM.dump

    @exec_wrapper
    def restore(self,VolName,Server,Partition,DumpFile, _cfg=None) :
        """
        Restores this (abstract) volume from a file.
        """
        CmdList=[_cfg.binaries["vos"], "restore","-server", "%s" % Server, "-partition", "%s" % Partition, "-name", "%s" % VolName, "-file" ,"%s" % DumpFile, "-cell",  "%s" % _cfg.cell]
        return CmdList,PM.restore
    
    @exec_wrapper
    def convert(self,VolName,Server,Partition, _cfg=None) :
        """
        converts this RO-Volume to a RW
        """
        CmdList=[_cfg.binaries["vos"], "convertROtoRW","-server", "%s" % Server, "-partition", "%s" % Partition, "-id", "%s" % VolName, "-cell",  "%s" % _cfg.cell]
        return CmdList,PM.convert

    @exec_wrapper
    def create(self,VolName,Server,Partition,MaxQuota, _cfg=None) :
        """
        create a Volume
        """
        CmdList=[_cfg.binaries["vos"], "create","-server", "%s" % Server, "-partition", "%s" % Partition, "-name", "%s" % VolName , "-maxquota", "%s" % MaxQuota, "-cell",  "%s" % _cfg.cell]
        return CmdList,PM.create
    
    @exec_wrapper
    def remove(self,VolName,Server, Partition, _cfg=None) :
        """
        remove this Volume from the Server
        """
        CmdList=[_cfg.binaries["vos"], "remove","-server", "%s" % Server, "-partition", "%s" % Partition, "-id", "%s" % VolName, "-cell",  "%s" % _cfg.cell ]
        return CmdList,PM.remove
   
    @exec_wrapper
    def getVolIDList(self, Server, _cfg=None, Partition=""): 
        CmdList=[_cfg.binaries["vos"], "listvol","-server", "%s" % Server, "-fast", "-cell",  "%s" % _cfg.cell ]
        if Partition != "" :
            CmdList += ["-partition", "%s" % Partition]    
        return CmdList,PM.getVolIDList
    
    @exec_wrapper
    def getVolume(self, name_or_id, serv=None, _cfg=None) :
        """
        Volume entry via vos examine from vol-server. 
        If Name is given, it takes precedence over ID
        """
        CmdList = [_cfg.binaries["vos"],"examine",  "%s"  % name_or_id ,"-format","-cell", "%s" % _cfg.cell]
        return CmdList,PM.getVolume
