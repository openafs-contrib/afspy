import afs.dao.bin
from afs.exceptions.VLDbError import VLDbError
from afs.dao.BaseDAO import BaseDAO
from afs.util import afsutil

class VLDbDAO(BaseDAO) :
    """
    Provides low-level acces to the Volume Location Database
    """

    def __init__(self) :
        BaseDAO.__init__(self)
        return
    
    def getFsServList(self,cellname, token, noresolve=False):
        """
        get list of dicts of all fileservers registered in the VLDB
        """
        CmdList=[afs.dao.bin.VOSBIN,"listaddrs", "-printuuid", "-cell","%s" % cellname ]
        if noresolve :
            CmdList.append("-noresolve")
        rc,output,outerr=self.execute(CmdList)
        if rc :
            raise VLDbError("Error", outerr)
       
        servers = []
        i = 0
        while i < len(output) :
            if output[i].startswith("UUID:"):
                server = {}
                splits = output[i].split()
                server['uuid'] = splits[1]
                i = i +1
                hostnames,ipaddrs=afsutil.getDNSInfo(output[i])
                if noresolve :
                    server['name_or_ip'] = ipaddrs[0]
                else :
                    server['name_or_ip'] = hostnames[0]
                servers.append(server)
            i += 1
        return servers

    def getFsUUID(self, name_or_ip, cellname, token) :
        CmdList=[afs.dao.bin.VOSBIN,"listaddrs", "-host",name_or_ip,"-printuuid", "-cell","%s" % cellname ]
        rc,output,outerr=self.execute(CmdList)
        if rc :
            raise VLDbError("Error", outerr)
        uuid=output[0].split()[1]
        return uuid

    def getVolumeList(self,name_or_ip, cellname,token,part="",noresolve=False) :
        """
        Return list of volumes on a server
        """
        CmdList=[afs.dao.bin.VOSBIN,"listvldb", "-server", "%s" % name_or_ip, "-cell","%s" % cellname ]
        if part != "" :
            CmdList += ["-part", "%s" % part]
        if noresolve :
            CmdList.append("-noresolve")
        rc,output,outerr=self.execute(CmdList)
        if rc :
            raise VLDbError("Error", outerr)

        Volumes=[]
        # header is always 2 lines
        i = 1
        while i < len(output) :
            if "Total entries:" in output[i] or "Volume is currently LOCKED" in output[i] or "Volume is locked for a" in output[i]  :
                i += 1 
                continue
            self.Logger.debug("getVolumeList: parsing %s" % output[i:i+10]) 
             
            Volume={}
            # mpe.integr.revol.0010 
            Volume["name"]=output[i].strip() 
            # RWrite: 536985599     ROnly: 536985600 
            splits=output[i+1].split()             
            if len(splits) == 6 :
                Volume["BK"] = splits[5]
            elif len(splits) == 4 :
                Volume["RO"] = splits[3]
            elif len(splits) == 2 :
                Volume["BK"] = splits[1]
            Volume["numSites"] = int(output[i+2].split()[4])
            Volume["RWSite"] = ""
            Volume["ROSites"] = []
            for l in range(Volume["numSites"]) :
                splits=output[i+3+l].split()
                hostnames,ipaddrs = afsutil.getDNSInfo(splits[1])
                if splits[4] == "RW" :
                    if noresolve :
                        Volume["RWSite"] = ipaddrs[0]
                    else :
                        Volume["RWSite"] = hostnames[0]
                elif splits[4] == "RO" :
                    if noresolve :
                        Volume["ROSites"].append(ipaddrs[0])
                    else :
                        Volume["ROSites"].append(hostnames[0])
            i = i + 3 + Volume["numSites"]
            Volumes.append(Volume)
        self.Logger.debug("getVolumeList: returning %s" % Volumes[:10])     
        return Volumes 
    
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
    
