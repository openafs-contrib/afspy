import re,string,os,sys
import afs.dao.bin

from afs.exceptions.VLDbError import VLDbError
from afs.dao.BaseDAO import BaseDAO

class VLDbDAO(BaseDAO) :
    """
    Provides low-level acces to the Volume Location Database
    """

    def __init__(self) :
        BaseDAO.__init__(self)
        return
    
    def getFsServList(self,cellname, token, noresolve=False):
        """
        get list of all fileservers registered in the VLDB
        """
        if noresolve:
            CmdList=[afs.dao.bin.VOSBIN,"listaddrs", "-printuuid", "-cell","%s" % cellname, "-noresolve" ]
        else:
            CmdList=[afs.dao.bin.VOSBIN,"listaddrs", "-printuuid", "-cell","%s" % cellname ]
        rc,output,outerr=self.execute(CmdList)
        if rc :
            raise VLDbError("Error", outerr)
       
        servers = []
        for i in range (0,len(output)) :
            if output[i].startswith("UUID:"):
                server = {}
                splits = output[i].split()
                server['uuid'] = splits[1]
                i = i +1
                server['name_or_ip'] = output[i]                            
                servers.append(server)
        return servers

    def  getFsUUID(self, name_or_ip, cellname, token) :
        CmdList=[afs.dao.bin.VOSBIN,"listaddrs", "-host",name_or_ip,"-printuuid", "-cell","%s" % cellname ]
        rc,output,outerr=self.execute(CmdList)
        if rc :
            raise VLDbError("Error", outerr)
        uuid=output[0].split()[1]
        return uuid
    
    def syncVLDb(self):
        """
        Check that volumes residing at given Fileserver/partition have a correct  VLDB entries.
        """
        pass
        
    def syncServ(self):
        """
        Verifies VLDB that entries pointing to a specified site are really on that Fileserver/Partition
        """
        pass 
    
    def changeVolLocation(self):
        """
        change the location of a Volume in the VLDB only
        """
        pass

    def setFSaddrs(self, UUID, hostlist, cellname, token): 
        """
        set the list of IP address for a given UUID in the VLDB
        """
        pass
        
    def addsite(self,VolName,DstServer,DstPartition,cellname, token) :
        """
        adds entry for a RO-Volume on Dst/Part in VLDB
        """
        CmdList=["vos", "addsite","-server", "%s" % DstServer, "-partition", "%s" % DstPartition, "-name", "%s" % VolName, "-cell",  "%s" % cellname ]
        rc,output,outerr=self.execute(CmdList) 
        if rc:
            raise VLDbError("Error", outerr)
    
    def remsite(self,VolName,Server,Partition,cellname, token) :
        """
        removes entry for a RO-Volume in VLDB
        """
        CmdList=["vos", "remsite","-server", "%s" % Server, "-partition", "%s" % Partition, "-name", "%s" % VolName, "-cell",  "%s" % cellname ]
        rc,output,outerr=self.execute(CmdList) 
        if rc:
            raise VLDbError("Error", outerr)
        
    def lock(self,ID, cellname, token) :
        """
        locks volume in VLDB
        """
        CmdList=["vos", "lock","-id" ,"%s" % ID, "-cell",  "%s" % cellname]
        rc,output,outerr=self.execute(CmdList)
        if rc:
            raise VLDbError("Error", outerr)
    
    def unlock(self,ID, cellname, token) :
        """
        unlocks volume in VLDB
        """
        CmdList=["vos", "unlock","-id" ,"%s" % ID, "-cell",  "%s" % cellname]
        rc,output,outerr=self.execute(CmdList)
        if rc:
            raise VLDbError("Error", outerr)
    
