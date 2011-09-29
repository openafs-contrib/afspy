import string,re,sys,time
import afs.dao.bin

from datetime import datetime
from afs.model.Volume import Volume
from afs.factory.VolStatusFactory import VolStatus
from afs.factory.VolTypeFactory import VolType
from afs.util import afsutil


class VolumeDAO(object) :
    """
    Provides information about AFS-Volumes and methods to change them
    """
    
    def __init__(self) :
        pass

    def move(self,ID, DstServer,DstPartition, cellname, token, dryrun=0, lethal=1) :
        """
        moves this volume to a new Destination. In case of a RO, do 
        an remove/addsite/release
        """
        CmdList=["vos", "move","%s" % ID, "-cell",  "%s" % cellname ]
        rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=dryrun,lethal=lethal)
        return rc,output,outerr

    def release(self,ID, cellname, token,dryrun=0,lethal=1) :
        """
        release this volume
        """
        CmdList=["vos", "release","%s" % ID, "-cell",  "%s" % cellname]
        rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=dryrun,lethal=lethal)
        return rc,output,outerr
    

    def setBlockQuota(self,ID, BlockQuota, cellname, token,dryrun=0,lethal=1) :
        """
        sets Blockquota
        """
        CmdList=["vos", "setfield","-id" ,"%s" % ID,"-maxquota","%s" % BlockQuota, "-cell",  "%s" % cellname]
        rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=dryrun,lethal=lethal)
        return rc,output,outerr
        
    def lock(self,ID, cellname, token,dryrun=0,lethal=1) :
        """
        locks volume in VLDB
        """
        CmdList=["vos", "lock","-id" ,"%s" % ID, "-cell",  "%s" % cellname]
        rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=dryrun,lethal=lethal)
        return rc,output,outerr
    
    def unlock(self,ID, cellname, token,dryrun=0,lethal=1) :
        """
        unlocks volume in VLDB
        """
        CmdList=["vos", "unlock","-id" ,"%s" % ID, "-cell",  "%s" % cellname]
        rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=dryrun,lethal=lethal)
        return rc,output,outerr

    
    def sync(self,ID, cellname, token,dryrun=0,lethal=1) :
        """
        Sync Volumeinfo on VLDB
        """
        CmdList=["vos", "syncvldb","-volume" ,"%s" % ID, "-cell",  "%s" % cellname]
        rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=dryrun,lethal=lethal)
        return rc,output,outerr
    
    def dump(self,ID, DumpFile,cellname, token,dryrun=0,lethal=1) :
        """
        Dumps a volume into a file
        """
        CmdList=["vos", "dump","-id" ,"%s" % ID, "-file" ,"%s" % DumpFile, "-cell",  "%s" % cellname]
        rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=dryrun,lethal=lethal)
        return rc,output,outerr

    def restore(self,VolName,Server,Partition,DumpFile,cellname, token,dryrun=0,lethal=1) :
        """
        Restores this (abstract) volume from a file.
        """
        CmdList=["vos", "restore","-server", "%s" % Server, "-partition", "%s" % Partition, "-name", "%s" % Name, "-file" ,"%s" % DumpFile, "-cell",  "%s" % cellname]
        rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=dryrun,lethal=lethal)
        return rc,output,outerr
    
    def convert(self,VolName,Server,Partition,cellname, token,dryrun=0,lethal=1) :
        """
        converts this RO-Volume to a RW
        """
        CmdList=["vos", "convertROtoRW","-server", "%s" % Server, "-partition", "%s" % Partition, "-id", "%s" % VolName, "-cell",  "%s" % cellname]
        rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=dryrun,lethal=lethal)
        return rc,output,outerr

    def create(self,VolName,Server,Partition,MaxQuota, cellname, token,dryrun=0,lethal=1) :
        """
        creates this abstract Volume
        """
        CmdList=["vos", "create","-server", "%s" % Server, "-partition", "%s" % Partition, "-name", "%s" % Name , "-maxquota", "%s" % Quota, "-cell",  "%s" % cellname]
        rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=dryrun,lethal=lethal)
        return rc,output,outerr

    def addsite(self,VolName,DstServer,DstPartition,cellname, token,dryrun=0,lethal=1) :
        """
        creates a RO-Volume on Dst
        """
        CmdList=["vos", "addsite","-server", "%s" % DstServer, "-partition", "%s" % DstPartition, "-name", "%s" % VolName, "-cell",  "%s" % cellname ]
        rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=dryrun,lethal=lethal) 
        return rc,output,outerr
    
    def remove(self,VolName,Server, Partition, cellname, token,dryrun=1,lethal=1) :
        """
        remove this Volume from the Server
        """
        CmdList=["vos", "remove","-server", "%s" % Server, "-partition", "%s" % Partition, "-id", "%s" % VolName, "-cell",  "%s" % cellname ]
        rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=dryrun,lethal=lethal) 
        return rc,output,outerr

    def getVolume(self, ID, vol, cellname,token,  dryrun=0, lethal=1) :
        """
        update entry via vos examine from vol-server. 
        If Name is given, it takes precedence over ID
        """
        if ID : 
             CmdList = [afs.dao.bin.VOSBIN,"examine", "-id", "%s"  % ID , "-format","-cell", "%s" %  cellname]
        else :
            raise AttributeError,"Neither Volume Name or ID known"
        rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=dryrun,lethal=lethal)
        if rc :
            return rc,output,outerr

        line_no = 0
        line = output[line_no]
        if re.search("Could not fetch the entry",line) or line == "VLDB: no such entry"  or re.search("Unknown volume ID or name",line) \
            or re.search("does not exist in VLDB",line) :
            return 1, [""], ["Vol with ID %s not existant" % (ID)]
            
        # first line gives Name, ID, Type, Used and Status      
        for line in output:
            splits = line.split()
            if splits[0] == "name":
                vol.name = splits[1]
            elif splits[0] == "id":
                vol.vid = splits[1]
            elif splits[0] == "serv" :
                vol.serv = splits[1]
            elif splits[0] == "part":
                vol.part = afsutil.canonicalizePartition(splits[1])
            elif splits[0] =="parentID":
                vol.parentID = splits[1]
            elif splits[0] == "backupID":
                vol.backupID = splits[1]
            elif splits[0] =="cloneID":
                vol.cloneID = splits[1]
            elif splits[0] =="inUse":
                vol.inUse = splits[1]
            elif splits[0] =="needsSalvaged":
                vol.needsSalvaged = splits[1]
            elif splits[0] == "destroyMe":
                vol.destroyMe = splits[1]
            elif splits[0] == "type":
                vol.type = splits[1]
            elif splits[0] == "creationDate":
                vol.creationDate = datetime.fromtimestamp(long(splits[1])) 
            elif splits[0] == "updateDate":
                vol.updateDate = datetime.fromtimestamp(long(splits[1]))
            elif splits[0] == "backupDate":
                vol.backupDate = datetime.fromtimestamp(long(splits[1]))
            elif splits[0] == "copyDate":
                vol.copyDate = datetime.fromtimestamp(long(splits[1]))
            elif splits[0] =="flags":
                vol.flags = splits[1] 
            elif splits[0] == "diskused":
                vol.diskused = splits[1]
            elif splits[0] == "maxquota":
                vol.maxquota = splits[1]  
            elif splits[0] == "minquota":
                vol.minquota = splits[1]
            elif splits[0] == "status":
                vol.status = splits[1]  
            elif splits[0] == "filecount":
                vol.filecount = splits[1]   
            elif splits[0] == "dayUse":
                vol.dayUse = splits[1]    
            elif splits[0] == "weekUse":
                vol.weekUse = splits[1] 
            elif splits[0] == "spare2":
                vol.spare2 = splits[1] 
            elif splits[0] == "spare3":
                vol.spare3 = splits[1]     
                
        return


   
