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
        return rc,outerr

    def release(self,ID, cellname, token,dryrun=0,lethal=1) :
        """
        release this volume
        """
        CmdList=["vos", "release","%s" % ID, "-cell",  "%s" % cellname]
        rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=dryrun,lethal=lethal)
        return rc,outerr
    

    def setBlockQuota(self,ID, BlockQuota, cellname, token,dryrun=0,lethal=1) :
        """
        sets Blockquota
        """
        CmdList=["vos", "setfield","-id" ,"%s" % ID,"-maxquota","%s" % BlockQuota, "-cell",  "%s" % cellname]
        rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=dryrun,lethal=lethal)
        return rc,outerr
        
    def lock(self,ID, cellname, token,dryrun=0,lethal=1) :
        """
        locks volume in VLDB
        """
        CmdList=["vos", "lock","-id" ,"%s" % ID, "-cell",  "%s" % cellname]
        rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=dryrun,lethal=lethal)
        return rc,outerr
    
    def unlock(self,ID, cellname, token,dryrun=0,lethal=1) :
        """
        unlocks volume in VLDB
        """
        CmdList=["vos", "unlock","-id" ,"%s" % ID, "-cell",  "%s" % cellname]
        rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=dryrun,lethal=lethal)
        return rc,outerr

    
    def sync(self,ID, cellname, token,dryrun=0,lethal=1) :
        """
        Sync Volumeinfo on VLDB
        """
        CmdList=["vos", "syncvldb","-volume" ,"%s" % ID, "-cell",  "%s" % cellname]
        rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=dryrun,lethal=lethal)
        return rc,outerr
    
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
        return rc,outerr
    
    def convert(self,VolName,Server,Partition,cellname, token,dryrun=0,lethal=1) :
        """
        converts this RO-Volume to a RW
        """
        CmdList=["vos", "convertROtoRW","-server", "%s" % Server, "-partition", "%s" % Partition, "-id", "%s" % VolName, "-cell",  "%s" % cellname]
        rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=dryrun,lethal=lethal)
        return rc,outerr

    def create(self,VolName,Server,Partition,MaxQuota, cellname, token,dryrun=0,lethal=1) :
        """
        creates this abstract Volume
        """
        CmdList=["vos", "create","-server", "%s" % Server, "-partition", "%s" % Partition, "-name", "%s" % Name , "-maxquota", "%s" % Quota, "-cell",  "%s" % cellname]
        rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=dryrun,lethal=lethal)
        return rc,outerr

    def addsite(self,VolName,DstServer,DstPartition,cellname, token,dryrun=0,lethal=1) :
        """
        creates a RO-Volume on Dst
        """
        CmdList=["vos", "addsite","-server", "%s" % DstServer, "-partition", "%s" % DstPartition, "-name", "%s" % VolName, "-cell",  "%s" % cellname ]
        rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=dryrun,lethal=lethal) 
        return rc,outerr
    
    def remove(self,VolName,Server, Partition, cellname, token,dryrun=1,lethal=1) :
        """
        remove this Volume from the Server
        """
        CmdList=["vos", "remove","-server", "%s" % Server, "-partition", "%s" % Partition, "-id", "%s" % VolName, "-cell",  "%s" % cellname ]
        rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=dryrun,lethal=lethal) 
        return rc,outerr
    
    
    def getVolGroup(self, vid, cellname, token, dryrun=0, lethal=1) :
        """
        update entry via vos examine from vol-server. 
        If Name is given, it takes precedence over ID
        """
        if vid : 
             CmdList = [afs.dao.bin.VOSBIN,"examine", "-id", "%s"  % vid , "-format","-cell", "%s" %  cellname]
        else :
            return 1 ,"Neither Volume Name or ID known"
        
        rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=dryrun,lethal=lethal)
       
        if rc :
            return rc,outerr

        line_no = 0
        line = output[line_no]
        if re.search("Could not fetch the entry",line) or line == "VLDB: no such entry"  or re.search("Unknown volume ID or name",line) \
            or re.search("does not exist in VLDB",line) :
            return 1, ["Vol with ID %s not existant" % (vid)]
            
        # first line gives Name, ID, Type, Used and Status  
        volList = {"RW": [], "RO": [] }
        roID = 0
        rwId = 0
        numSite = 0
        numServer = 0
        for line in output:
            splits = line.split()
            #search server list section
            if splits[0] == "RWrite:":
                rwID = splits[1]
                roID = splits[3]
            
            if splits[0] == "number":  
                numSite =  splits[4] 
                
            # 1 = server, 3 = partitions, 4 type
            if splits[0] == "server":
                numServer = numServer +1
                if splits[4] =="RW":                  
                    volList["RW"].append({"id":rwID,"serv":splits[1],"part":splits[3]})
                else:
                    volList["RO"].append({"id":roID,"serv":splits[1],"part":splits[3]})
                
                if numSite == numServer:
                    break
          
        return 0,outerr,volList
       

    def getVolume(self, vid, serv, part, vol, cellname, token,  dryrun=0, lethal=1) :
        """
        update entry via vos examine from vol-server. 
        If Name is given, it takes precedence over ID
        """
        if vid : 
             CmdList = [afs.dao.bin.VOSBIN,"listvol", "-server", "%s"  % serv , "-part", "%s"  % part ,"-format","-cell", "%s" %  cellname]
        else :
            return 1 ,"Neither Volume Name or ID known"
        
        rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=dryrun,lethal=lethal)
        if rc :
            return rc,outerr

        line_no = 0
        line = output[line_no]
       
        if re.search("Could not fetch the entry",line) or line == "VLDB: no such entry"  or re.search("Unknown volume ID or name",line) \
            or re.search("does not exist in VLDB",line) :
            return 1, ["Vol with ID %s not existant" % (vid)]
            
        # first line gives Name, ID, Type, Used and Status 
        find = False    
         
        for i in range(0, len(output)):
            splits = output[i].split()
            #Beginnig block
            if splits[0] == "BEGIN_OF_ENTRY":
                line1 = output[i+1].split()
                line2 = output[i+2].split()
                line3 = output[i+3].split()
                line4 = output[i+4].split()
                if ((line1[1] == vid or\
                     line2[1] == vid ) and \
                     (line3[1] == serv or\
                      line3[2] == serv) and\
                      (line4[1] == part)):

                    find = True
                    splits = output[i+1].split()
                    vol.name     = splits[1]
                    splits = output[i+2].split()
                    vol.vid      = splits[1]
                    splits = output[i+3].split()
                    vol.serv     = splits[1]
                    splits = output[i+4].split()
                    vol.part     = splits[1]
                    splits = output[i+5].split()
                    vol.status     = splits[1]
                    splits = output[i+6].split()
                    vol.backupID = splits[1]
                    splits = output[i+7].split()
                    vol.parentID = splits[1]
                    splits = output[i+8].split()
                    vol.cloneID  = splits[1]
                    splits = output[i+9].split()
                    vol.inUse    = splits[1]
                    splits = output[i+10].split()
                    vol.needsSalvaged = splits[1]
                    splits = output[i+11].split()
                    vol.destroyMe     = splits[1]
                    splits = output[i+12].split()
                    vol.type          = splits[1]
                    splits = output[i+13].split()
                    vol.creationDate  =  datetime.fromtimestamp(float(splits[1]))
                    splits = output[i+14].split()
                    vol.updateDate    = datetime.fromtimestamp(float(splits[1]))
                    splits = output[i+15].split()
                    vol.backupDate     = datetime.fromtimestamp(float(splits[1]))
                    splits = output[i+16].split()
                    vol.copyDate      = datetime.fromtimestamp(float(splits[1]))
                    splits = output[i+17].split()
                    vol.flags         = splits[1]
                    splits = output[i+18].split()
                    vol.diskused      = splits[1]
                    splits = output[i+19].split()
                    vol.maxquota      = splits[1]
                    splits = output[i+20].split()
                    vol.minquota      = splits[1]
                    splits = output[i+21].split()
                    vol.filecount     = splits[1]
                    splits = output[i+22].split()
                    vol.dayUse        = splits[1]
                    splits = output[i+23].split()
                    vol.weekUse       = splits[1]
                    splits = output[i+24].split()
                    vol.spare2        = splits[1]
                    splits = output[i+25].split()
                    vol.spare3        = splits[1]
                    splits = output[i+26].split()
                    break
                else:
                    i = i+26
        
        if find:
            rc = 0
        else:
            rc = 1      
        return rc, "Not Found"


   
