import string,re,sys,time
import afs.dao.bin

from datetime import datetime
from afs.model.VolError import VolError
from afs.factory.VolStatusFactory import VolStatus
from afs.factory.VolTypeFactory import VolType
from afs.util import afsutil


class VolumeDAO(object) :
    """
    Provides Methods to query and modify live AFS-Volumes
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
        if rc:
            raise VolError("Error", outerr)

    def release(self,ID, cellname, token,dryrun=0,lethal=1) :
        """
        release this volume
        """
        CmdList=["vos", "release","%s" % ID, "-cell",  "%s" % cellname]
        rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=dryrun,lethal=lethal)
        if rc:
            raise VolError("Error", outerr)
    
    def setBlockQuota(self,ID, BlockQuota, cellname, token,dryrun=0,lethal=1) :
        """
        sets Blockquota
        """
        CmdList=["vos", "setfield","-id" ,"%s" % ID,"-maxquota","%s" % BlockQuota, "-cell",  "%s" % cellname]
        rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=dryrun,lethal=lethal)
        if rc:
            raise VolError("Error", outerr)
        
    def dump(self,ID, DumpFile,cellname, token,dryrun=0,lethal=1) :
        """
        Dumps a volume into a file
        """
        CmdList=["vos", "dump","-id" ,"%s" % ID, "-file" ,"%s" % DumpFile, "-cell",  "%s" % cellname]
        rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=dryrun,lethal=lethal)
        if rc:
             raise VolError("Error", outerr)

    def restore(self,VolName,Server,Partition,DumpFile,cellname, token,dryrun=0,lethal=1) :
        """
        Restores this (abstract) volume from a file.
        """
        CmdList=["vos", "restore","-server", "%s" % Server, "-partition", "%s" % Partition, "-name", "%s" % Name, "-file" ,"%s" % DumpFile, "-cell",  "%s" % cellname]
        rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=dryrun,lethal=lethal)
        if rc:
             raise VolError("Error", outerr)
    
    def convert(self,VolName,Server,Partition,cellname, token,dryrun=0,lethal=1) :
        """
        converts this RO-Volume to a RW
        """
        CmdList=["vos", "convertROtoRW","-server", "%s" % Server, "-partition", "%s" % Partition, "-id", "%s" % VolName, "-cell",  "%s" % cellname]
        rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=dryrun,lethal=lethal)
        if rc:
             raise VolError("Error", outerr)

    def create(self,VolName,Server,Partition,MaxQuota, cellname, token,dryrun=0,lethal=1) :
        """
        create a Volume
        """
        id = 0
        CmdList=["vos", "create","-server", "%s" % Server, "-partition", "%s" % Partition, "-name", "%s" % Name , "-maxquota", "%s" % Quota, "-cell",  "%s" % cellname]
        rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=dryrun,lethal=lethal)
        if rc:
             raise VolError("Error", outerr)
        
        return id
    
    def remove(self,VolName,Server, Partition, cellname, token,dryrun=1,lethal=1) :
        """
        remove this Volume from the Server
        """
        CmdList=["vos", "remove","-server", "%s" % Server, "-partition", "%s" % Partition, "-id", "%s" % VolName, "-cell",  "%s" % cellname ]
        rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=dryrun,lethal=lethal) 
        if rc:
             raise VolError("Error", outerr)
    
    def getVolGroup(self, vid, cellname, token, dryrun=0, lethal=1) :
        """
        update entry via vos examine from vol-server. 
        """
        
        CmdList = [afs.dao.bin.VOSBIN,"examine", "-id", "%s"  % vid , "-format","-cell", "%s" %  cellname]
        rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=dryrun,lethal=lethal)
       
        if rc :
            raise VolError("Error", outerr)
        
        volGroup = {}
        line_no = 0
        line = output[line_no]
        
        if re.search("Could not fetch the entry",line) or line == "VLDB: no such entry"  or re.search("Unknown volume ID or name",line) \
            or re.search("does not exist in VLDB",line) :
            return volGroup
            
        # first line gives Name, ID, Type, Used and Status  
        #volList = {"RW": [], "RO": [] }
        
        roID = 0
        rwID = 0
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
            #FIXME check BK !!!   
            # 1 = server, 3 = partitions, 4 type
            if splits[0] == "server":
                numServer = numServer +1
                type = splits[4]
                
                if not volGroup.get(type,None):
                    volGroup[type] = []
               
                if type =="RW":                 
                    volGroup["RW"].append({"id":rwID,"serv":splits[1],"part":splits[3]})
                elif type =="RO":
                    volGroup["RO"].append({"id":roID,"serv":splits[1],"part":splits[3]})
                else:
                    volGroup["BK"].append({"id":roID,"serv":splits[1],"part":splits[3]})
                    
                if numSite == numServer:
                    break
        
        return volGroup
       

    def getVolume(self, vid, serv, part, cellname, token,  dryrun=0, lethal=1) :
        """
        update entry via vos examine from vol-server. 
        If Name is given, it takes precedence over ID
        """
        part = afsutil.canonicalizePartition(part)
        CmdList = [afs.dao.bin.VOSBIN,"examine",  "%s"  % vid ,"-format","-cell", "%s" % cellname]
        rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=dryrun,lethal=lethal)
        if rc :
            raise VolError("Error", outerr)
        
        line_no = 0
        line = output[line_no]
        vol = {}
       
        if re.search("Could not fetch the entry",line) or line == "VLDB: no such entry"  or re.search("Unknown volume ID or name",line) \
            or re.search("does not exist in VLDB",line) :
            return vol
       
        # first line gives Name, ID, Type, Used and Status 
        find = False    

        for i in range(0, len(output)):
            splits = output[i].split()
            #Beginnig block
            if splits[0] == "name":
                line1 = output[i].split()
                line2 = output[i+1].split()
                line3 = output[i+2].split()
                line4 = output[i+3].split()
                if ((line1[1] == str(vid) or\
                     line2[1] == str(vid) ) and \
                     (line3[1] == serv or\
                      line3[2] == serv) and\
                      (afsutil.canonicalizePartition(line4[1]) == part)):

                    find = True
                    splits = output[i].split()
                    vol['name']     = splits[1]
                    splits = output[i+1].split()
                    vol['vid']      = splits[1]
                    splits = output[i+2].split()
                    vol['serv']     = splits[1]
                    if len(splits) > 2:
                        vol['servname']     = splits[2]
                    splits = output[i+3].split()
                    vol['part']     = afsutil.canonicalizePartition(splits[1])
                    splits = output[i+4].split()
                    vol['status']     = splits[1]
                    splits = output[i+5].split()
                    vol['backupID'] = splits[1]
                    splits = output[i+6].split()
                    vol['parentID'] = splits[1]
                    splits = output[i+7].split()
                    vol['cloneID']  = splits[1]
                    splits = output[i+8].split()
                    vol['inUse']    = splits[1]
                    splits = output[i+9].split()
                    vol['needsSalvaged'] = splits[1]
                    splits = output[i+10].split()
                    vol['destroyMe']     = splits[1]
                    splits = output[i+11].split()
                    vol['type']          = splits[1]
                    splits = output[i+12].split()
                    vol['creationDate']  =  datetime.fromtimestamp(float(splits[1]))
                    splits = output[i+13].split()
                    vol['accessDate']  =  datetime.fromtimestamp(float(splits[1]))
                    splits = output[i+14].split()
                    vol['updateDate']    = datetime.fromtimestamp(float(splits[1]))
                    splits = output[i+15].split()
                    vol['backupDate']     = datetime.fromtimestamp(float(splits[1]))
                    splits = output[i+16].split()
                    vol['copyDate']      = datetime.fromtimestamp(float(splits[1]))
                    splits = output[i+17].split()
                    vol['flags']         = splits[1]
                    splits = output[i+18].split()
                    vol['diskused']      = splits[1]
                    splits = output[i+19].split()
                    vol['maxquota']      = splits[1]
                    splits = output[i+20].split()
                    vol['minquota']      = splits[1]
                    splits = output[i+21].split()
                    vol['filecount']     = splits[1]
                    splits = output[i+22].split()
                    vol['dayUse']        = splits[1]
                    splits = output[i+23].split()
                    vol['weekUse']       = splits[1]
                    splits = output[i+24].split()
                    vol['spare2']        = splits[1]
                    splits = output[i+25].split()
                    vol['spare3']        = splits[1]
                                     
                    break
                else:
                    i = i+25
        return vol
    
    def getVolList(self, serv, part,  cellname, token,  dryrun=0, lethal=1) :
        """
        update entry via vos examine from vol-server. 
        If Name is given, it takes precedence over ID
        """
        part = afsutil.canonicalizePartition(part)
        CmdList = [afs.dao.bin.VOSBIN,"listvol", "-server", "%s"  % serv , "-part", "%s"  % part ,"-format","-cell", "%s" %  cellname]
        
        rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=dryrun,lethal=lethal)
        if rc :
            raise VolError("Error",outerror)
        
        line_no = 0
        line = output[line_no]
       
       
        # first line gives Name, ID, Type, Used and Status 
        volList = [] 
        
        for i in range(0, len(output)):
            splits = output[i].split()
            #Beginnig block
            if splits[0] == "BEGIN_OF_ENTRY":
                    vol = {}
                    splits = output[i+1].split()
                    vol['name']     = splits[1]
                    splits = output[i+2].split()
                    vol['vid']      = splits[1]
                    splits = output[i+3].split()
                    vol['serv']     = splits[1]
                    if len(splits) > 2:
                        vol['servname']     = splits[2]
                    splits = output[i+4].split()
                    vol['part']     = afsutil.canonicalizePartition(splits[1])
                    splits = output[i+5].split()
                    vol['status']     = splits[1]
                    splits = output[i+6].split()
                    vol['backupID'] = splits[1]
                    splits = output[i+7].split()
                    vol['parentID'] = splits[1]
                    splits = output[i+8].split()
                    vol['cloneID']  = splits[1]
                    splits = output[i+9].split()
                    vol['inUse']    = splits[1]
                    splits = output[i+10].split()
                    vol['needsSalvaged'] = splits[1]
                    splits = output[i+11].split()
                    vol['destroyMe']     = splits[1]
                    splits = output[i+12].split()
                    vol['type']          = splits[1]
                    splits = output[i+13].split()
                    vol['creationDate']  =  datetime.fromtimestamp(float(splits[1]))
                    splits = output[i+14].split()
                    vol['updateDate']    = datetime.fromtimestamp(float(splits[1]))
                    splits = output[i+15].split()
                    vol['backupDate']     = datetime.fromtimestamp(float(splits[1]))
                    splits = output[i+16].split()
                    vol['copyDate']      = datetime.fromtimestamp(float(splits[1]))
                    splits = output[i+17].split()
                    vol['flags']         = splits[1]
                    splits = output[i+18].split()
                    vol['diskused']      = splits[1]
                    splits = output[i+19].split()
                    vol['maxquota']      = splits[1]
                    splits = output[i+20].split()
                    vol['minquota']      = splits[1]
                    splits = output[i+21].split()
                    vol['filecount']     = splits[1]
                    splits = output[i+22].split()
                    vol['dayUse']        = splits[1]
                    splits = output[i+23].split()
                    vol['weekUse']       = splits[1]
                    splits = output[i+24].split()
                    vol['spare2']        = splits[1]
                    splits = output[i+25].split()
                    vol['spare3']        = splits[1]
                    volList.append(vol)
                    i = i+26
              
        return volList
        
        def getIdVolList(self, part, server, cell):
            """
            return  Volumes in partitions
            """
            part = afsutil.canonicalizePartition(part)
            RX=re.compile("^(\d+)")
            CmdList=[afs.dao.bin.VOSBIN,"listvol", "-server", "%s" % server, "-partition", "%s" % part ,"-fast" , "-cell","%s" % cell]
 
            rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=0,lethal=1)
            if rc :
                 raise VolError("Error", outerr)
            volIds = {}
            
            for line in output :
                m=RX.match(line)
                if not m :
                    raise VolError("Error parsing output" , line)
                if m :
                   vid = m.groups()
                   volIds.append(vid) 
                
            return volIds
        
        def getPartList(self,  servername, cellname) :
            """
            return dict of  Partitions
            """
            RX=re.compile("Free space on partition /vicep(\S+): (\d+) K blocks out of total (\d+)")
            CmdList=[afs.dao.bin.VOSBIN,"partinfo", "%s" % servername, "-cell","%s" % cellname]
            rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=0,lethal=1)
            if rc :
                 raise VolError("Error", outerr)
            
            partitions= {}
            for line in output :
                m=RX.match(line)
                if not m :
                    raise VolError("Error parsing output" , line)

                name, free, total=m.groups()
                name = afsutil.canonicalizePartition(name)
                used = long(total)-long(free)
                partitions.append({"name":name,"total" : total,  "used" : used,  "free" : free})
            return partitions
