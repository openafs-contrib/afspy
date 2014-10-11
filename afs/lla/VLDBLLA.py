from afs.lla.BaseLLA import BaseLLA, exec_wrapper
import VLDBLLAParse as PM
from afs.util.AFSError import AFSError

class VLDBLLA(BaseLLA) :
    """
    Provides low-level acces to the Volume Location Database
    """

    def __init__(self) :
        BaseLLA.__init__(self)
        return

    def get_name_or_id(self, param) :
        # XXX code replication from VolServerLLA
        try: 
            if param.vid != None :
                name_or_id = "%s" % param.vid
            elif param.name != None :
                name_or_id = param.name
            else :
                raise RuntimeError("Volume name or id required.")
        except AttributeError :
            name_or_id = param   
        return name_or_id
    
    @exec_wrapper
    def get_fileserver_list(self, noresolve=False, _cfg=None):
        """
        get list of dicts of all fileservers registered in the VLDB
        """
        command_list = [_cfg.binaries["vos"],"listaddrs", "-printuuid", "-cell","%s" % _cfg.cell]
        if noresolve :
            command_list.append("-noresolve")
        return command_list, PM.get_fileserver_list

    @exec_wrapper
    def get_fileserver_uuid(self, name_or_ip, _cfg=None) :
        command_list = [_cfg.binaries["vos"], "listaddrs", "-host", name_or_ip, "-printuuid", "-cell","%s" % _cfg.cell ]

        return command_list, PM.get_fileserver_uuid

    @exec_wrapper
    def get_volume_list(self, name_or_ip="" , part="", noresolve=False, _cfg=None) :
        """
        Return list of volumes on a server
        """
        command_list = [_cfg.binaries["vos"],"listvldb", "-cell","%s" % _cfg.cell ]
        if name_or_ip != "" :
            command_list += [ "-server", "%s" % name_or_ip ]  
        if part != "" :
            command_list += ["-part", "%s" % part]
        if noresolve :
            command_list.append("-noresolve")
        return command_list, PM.get_volume_list

    @exec_wrapper
    def sync_vldb(self, name_or_ip, part="", volume="", _cfg=None):
        """
        Check that volumes residing at given Fileserver/partition have a correct  VLDB entries.
        """
        command_list = [_cfg.binaries["vos"], "syncvldb", "-server", "%s" % name_or_ip ,  "-cell",  "%s" % _cfg.cell ]
        if part != "" :
            command_list += [ "-part", "%s" % part]
        if volume != "" :
            command_list += [ "-volume", "%s" % volume]
        return command_list, PM.sync_vldb
        
    @exec_wrapper
    def sync_serv(self, name_or_ip, part="",_cfg=None):
        """
        Verifies VLDB that entries pointing to a specified site are really on that Fileserver/Partition
        """
        command_list = [_cfg.binaries["vos"], "syncserv", "-server", "%s" % name_or_ip ,  "-cell",  "%s" % _cfg.cell ]
        if part != "" :
            command_list += [ "-part", "%s" % part]
        return command_list, PM.sync_serv
    
    @exec_wrapper
    def addsite(self, volume, _cfg=None) :
        """
        adds entry for a RO-Volume on Dst/Part in VLDB
        """
        name_or_id = self.get_name_or_id(volume)
        CmdList=[_cfg.binaries["vos"], "addsite","-server", "%s" % volume.servername, "-partition", "%s" % volume.partition, "-id", "%s" % name_or_id, "-cell",  "%s" % _cfg.cell ]
        return CmdList,PM.addsite
    
    @exec_wrapper
    def remsite(self, volume, _cfg=None) :
        """
        removes entry for a RO-Volume in VLDB
        """
        name_or_id = self.get_name_or_id(volume)
        CmdList=[_cfg.binaries["vos"], "remsite","-server", "%s" % volume.servername, "-partition", "%s" % volume.partition, "-id", "%s" % name_or_id, "-cell",  "%s" % _cfg.cell ]
        return CmdList,PM.remsite
        
    @exec_wrapper
    def lock(self, volume, _cfg=None) :
        """
        locks volume in VLDB
        """
        name_or_id = self.get_name_or_id(volume)
        CmdList=[_cfg.binaries["vos"], "lock","-id" ,"%s" % name_or_id, "-cell",  "%s" % _cfg.cell]
        return CmdList,PM.lock
    
    @exec_wrapper
    def unlock(self, volume, _cfg=None) :
        """
        unlocks volume in VLDB
        """
        name_or_id = self.get_name_or_id(volume)
        CmdList=[_cfg.binaries["vos"], "unlock","-id" ,"%s" % name_or_id, "-cell",  "%s" % _cfg.cell]
        return CmdList,PM.unlock
    
