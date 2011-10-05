import re,string,os,sys
import afs.dao.bin

class VLDbDAO() :
    """
    Provides low-level acces to the Volume Location Database
    """
    def __init__(self) :
        return
    
    def getFsServerList(self,servername,cellname):
        """
        get Information about a single Server
        """
        
        CmdList=[afs.dao.bin.VOSBIN,"listaddrs", "-host","%s" % servername, "-printuuid", "-cell","%s" % cellname ]
        rc,output,outerr=afs.dao.bin.execute(CmdList)
        if rc :
            raise VolError("Error", outerr)
       
        server = FileServer()
        for i in range (0,len(output)) :
            if output[i].startswith("UUID:"):
                splits = output[i].split()
                server.uuid = splits[1]
                i = i +1
                server.name = output[i]                                   
        return server
        
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
        rc,output,outerr=afs.dao.bin.execute(CmdList) 
        if rc:
            raise VolError("Error", outerr)
    
    def remsite(self,VolName,Server,Partition,cellname, token) :
        """
        removes entry for a RO-Volume in VLDB
        """
        CmdList=["vos", "remsite","-server", "%s" % Server, "-partition", "%s" % Partition, "-name", "%s" % VolName, "-cell",  "%s" % cellname ]
        rc,output,outerr=afs.dao.bin.execute(CmdList) 
        if rc:
            raise VolError("Error", outerr)
        
    def lock(self,ID, cellname, token) :
        """
        locks volume in VLDB
        """
        CmdList=["vos", "lock","-id" ,"%s" % ID, "-cell",  "%s" % cellname]
        rc,output,outerr=afs.dao.bin.execute(CmdList)
        if rc:
            raise VolError("Error", outerr)
    
    def unlock(self,ID, cellname, token) :
        """
        unlocks volume in VLDB
        """
        CmdList=["vos", "unlock","-id" ,"%s" % ID, "-cell",  "%s" % cellname]
        rc,output,outerr=afs.dao.bin.execute(CmdList)
        if rc:
            raise VolError("Error", outerr)
    
