from afs.dao.BaseDAO import BaseDAO
from afs.dao.BaseDAO import execwrapper
from afs.util import afsutil
import VLDbDAO_parse as PM
import string

class VLDbDAO(BaseDAO) :
    """
    Provides low-level acces to the Volume Location Database
    """

    def __init__(self) :
        BaseDAO.__init__(self)
        return
    
    @execwrapper
    def getFsServList(self,_cfg=None, noresolve=False):
        """
        get list of dicts of all fileservers registered in the VLDB
        """
        CmdList=[_cfg.binaries["vos"],"listaddrs", "-printuuid", "-cell","%s" % _cfg.CELL_NAME ]
        if noresolve :
            CmdList.append("-noresolve")
        return CmdList,PM.getFsServList

    @execwrapper
    def getFsUUID(self, name_or_ip, _cfg) :
        CmdList=[_cfg.binaries["vos"],"listaddrs", "-host",name_or_ip,"-printuuid", "-cell","%s" % _cfg.CELL_NAME ]

        return CmdList,PM.getFsUUID

    @execwrapper
    def getVolumeList(self, name_or_ip, _cfg, part="", noresolve=False) :
        """
        Return list of volumes on a server
        """
        CmdList=[_cfg.binaries["vos"],"listvldb", "-server", "%s" % name_or_ip, "-cell","%s" % _cfg.CELL_NAME ]
        if part != "" :
            CmdList += ["-part", "%s" % part]
        if noresolve :
            CmdList.append("-noresolve")
        return CmdList,PM.getVolumeList

    @execwrapper
    def syncVLDb(self, name_or_ip, part="", volume="",_cfg=None):
        """
        Check that volumes residing at given Fileserver/partition have a correct  VLDB entries.
        """
        CmdList=[_cfg.binaries["vos"], "syncvldb", "-server", "%s" % name_or_ip ,  "-cell",  "%s" % _cfg.CELL_NAME ]
        if part != "" :
            CmdList += [ "-part", "%s" % part]
        if volume != "" :
            CmdList += [ "-volume", "%s" % volume]
        return CmdList,PM.syncVLDB
        
    @execwrapper
    def syncServ(self, name_or_ip, part="",_cfg=None):
        """
        Verifies VLDB that entries pointing to a specified site are really on that Fileserver/Partition
        """
        CmdList=[_cfg.binaries["vos"], "syncserv", "-server", "%s" % name_or_ip ,  "-cell",  "%s" % _cfg.CELL_NAME ]
        if part != "" :
            CmdList += [ "-part", "%s" % part]
        return CmdList,PM.syncServ
    
    @execwrapper
    def setaddrs(self, UUID, hostlist, _cfg=None): 
        """
        set the list of IP address for a given UUID in the VLDB
        Usage: vos setaddrs -uuid <uuid of server> -host <address of host>+ [-cell <cell name>] [-noauth] [-localauth] [-verbose] [-encrypt] [-noresolve] [-help]
        """
        CmdList=[_cfg.binaries["vos"], "setaddrs","-uuid", "%s" % UUID, "-host", "%s" % string.join(hostlist," "),  "-cell",  "%s" % _cfg.CELL_NAME ]
        return CmdList,PM.setaddrs
        
    @execwrapper
    def addsite(self,VolName,DstServer,DstPartition, _cfg=None) :
        """
        adds entry for a RO-Volume on Dst/Part in VLDB
        """
        CmdList=[_cfg.binaries["vos"], "addsite","-server", "%s" % DstServer, "-partition", "%s" % DstPartition, "-name", "%s" % VolName, "-cell",  "%s" % _cfg.CELL_NAME ]
        return CmdList,PM.addsite
    
    @execwrapper
    def remsite(self,VolName,Server,Partition, _cfg=None) :
        """
        removes entry for a RO-Volume in VLDB
        """
        CmdList=[_cfg.binaries["vos"], "remsite","-server", "%s" % Server, "-partition", "%s" % Partition, "-name", "%s" % VolName, "-cell",  "%s" % _cfg.CELL_NAME ]
        return CmdList,PM.remsite
        
    @execwrapper
    def lock(self,ID, _cfg=None) :
        """
        locks volume in VLDB
        """
        CmdList=[_cfg.binaries["vos"], "lock","-id" ,"%s" % ID, "-cell",  "%s" % _cfg.CELL_NAME]
        return CmdList,PM.lock
    
    @execwrapper
    def unlock(self,ID, _cfg=None) :
        """
        unlocks volume in VLDB
        """
        CmdList=[_cfg.binaries["vos"], "unlock","-id" ,"%s" % ID, "-cell",  "%s" % _cfg.CELL_NAME]
        return CmdList,PM.unlock
    
