from afs.dao.BaseDAO import BaseDAO
from afs.util.Executor import exec_wrapper
import VLDBDAOParse as PM
from afs.util.AFSError import AFSError

class VLDBDAO(BaseDAO) :
    """
    Provides low-level acces to the Volume Location Database
    """

    def __init__(self) :
        BaseDAO.__init__(self)
        return
    
    @exec_wrapper
    def getFsServList(self, noresolve=False, _cfg=None):
        """
        get list of dicts of all fileservers registered in the VLDB
        """
        CmdList=[_cfg.binaries["vos"],"listaddrs", "-printuuid", "-cell","%s" % _cfg.cell]
        if noresolve :
            CmdList.append("-noresolve")
        return CmdList,PM.getFsServList

    @exec_wrapper
    def get_fileserver_uuid(self, name_or_ip, _cfg=None) :
        CmdList=[_cfg.binaries["vos"],"listaddrs", "-host",name_or_ip,"-printuuid", "-cell","%s" % _cfg.cell ]

        return CmdList,PM.get_fileserver_uuid

    @exec_wrapper
    def getVolumeList(self, name_or_ip, part="", noresolve=False, _cfg=None) :
        """
        Return list of volumes on a server
        """
        CmdList=[_cfg.binaries["vos"],"listvldb", "-server", "%s" % name_or_ip, "-cell","%s" % _cfg.cell ]
        if part != "" :
            CmdList += ["-part", "%s" % part]
        if noresolve :
            CmdList.append("-noresolve")
        return CmdList,PM.getVolumeList

    @exec_wrapper
    def syncVLDb(self, name_or_ip, part="", volume="",_cfg=None):
        """
        Check that volumes residing at given Fileserver/partition have a correct  VLDB entries.
        """
        CmdList=[_cfg.binaries["vos"], "syncvldb", "-server", "%s" % name_or_ip ,  "-cell",  "%s" % _cfg.cell ]
        if part != "" :
            CmdList += [ "-part", "%s" % part]
        if volume != "" :
            CmdList += [ "-volume", "%s" % volume]
        return CmdList,PM.syncVLDB
        
    @exec_wrapper
    def syncServ(self, name_or_ip, part="",_cfg=None):
        """
        Verifies VLDB that entries pointing to a specified site are really on that Fileserver/Partition
        """
        CmdList=[_cfg.binaries["vos"], "syncserv", "-server", "%s" % name_or_ip ,  "-cell",  "%s" % _cfg.cell ]
        if part != "" :
            CmdList += [ "-part", "%s" % part]
        return CmdList,PM.syncServ
    
    @exec_wrapper
    def setaddrs(self, UUID, hostlist, _cfg=None): 
        """
        set the list of IP address for a given UUID in the VLDB
        Usage: vos setaddrs -uuid <uuid of server> -host <address of host>+ [-cell <cell name>] [-noauth] [-localauth] [-verbose] [-encrypt] [-noresolve] [-help]
        """
        CmdList=[_cfg.binaries["vos"], "setaddrs","-uuid", "%s" % UUID, "-host", "%s" % " ".join(hostlist),  "-cell",  "%s" % _cfg.cell ]
        return CmdList,PM.setaddrs
        
    @exec_wrapper
    def addsite(self,VolName,DstServer,DstPartition, _cfg=None) :
        """
        adds entry for a RO-Volume on Dst/Part in VLDB
        """
        CmdList=[_cfg.binaries["vos"], "addsite","-server", "%s" % DstServer, "-partition", "%s" % DstPartition, "-id", "%s" % VolName, "-cell",  "%s" % _cfg.cell ]
        return CmdList,PM.addsite
    
    @exec_wrapper
    def remsite(self,VolName,Server,Partition, _cfg=None) :
        """
        removes entry for a RO-Volume in VLDB
        """
        CmdList=[_cfg.binaries["vos"], "remsite","-server", "%s" % Server, "-partition", "%s" % Partition, "-name", "%s" % VolName, "-cell",  "%s" % _cfg.cell ]
        return CmdList,PM.remsite
        
    @exec_wrapper
    def lock(self,ID, _cfg=None) :
        """
        locks volume in VLDB
        """
        CmdList=[_cfg.binaries["vos"], "lock","-id" ,"%s" % ID, "-cell",  "%s" % _cfg.cell]
        return CmdList,PM.lock
    
    @exec_wrapper
    def unlock(self,ID, _cfg=None) :
        """
        unlocks volume in VLDB
        """
        CmdList=[_cfg.binaries["vos"], "unlock","-id" ,"%s" % ID, "-cell",  "%s" % _cfg.cell]
        return CmdList,PM.unlock
    
