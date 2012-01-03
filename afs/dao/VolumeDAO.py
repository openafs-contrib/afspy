import string,re,sys,time
import afs.dao.bin

from datetime import datetime
from afs.exceptions.VolError import VolError
from afs.util import afsutil


class VolumeDAO(object) :
    """
    Provides Methods to query and modify live AFS-Volumes
    """
    
    def __init__(self) :
        pass

    def move(self,ID, DstServer,DstPartition, cellname, token) :
        """
        moves this volume to a new Destination. In case of a RO, do 
        an remove/addsite/release
        """
        CmdList=["vos", "move","%s" % ID, "-cell",  "%s" % cellname ]
        rc,output,outerr=afs.dao.bin.execute(CmdList)
        # use output for logging.
        if rc:
            raise VolError("Error", outerr)

    def release(self,ID, cellname, token) :
        """
        release this volume
        """
        CmdList=["vos", "release","%s" % ID, "-cell",  "%s" % cellname]
        rc,output,outerr=afs.dao.bin.execute(CmdList)
        if rc:
            raise VolError("Error", outerr)
    
    def setBlockQuota(self,ID, BlockQuota, cellname, token) :
        """
        sets Blockquota
        """
        CmdList=["vos", "setfield","-id" ,"%s" % ID,"-maxquota","%s" % BlockQuota, "-cell",  "%s" % cellname]
        rc,output,outerr=afs.dao.bin.execute(CmdList)
        if rc:
            raise VolError("Error", outerr)
        
    def dump(self,ID, DumpFile,cellname, token) :
        """
        Dumps a volume into a file
        """
        CmdList=["vos", "dump","-id" ,"%s" % ID, "-file" ,"%s" % DumpFile, "-cell",  "%s" % cellname]
        rc,output,outerr=afs.dao.bin.execute(CmdList)
        if rc:
             raise VolError("Error", outerr)

    def restore(self,VolName,Server,Partition,DumpFile,cellname, token) :
        """
        Restores this (abstract) volume from a file.
        """
        CmdList=["vos", "restore","-server", "%s" % Server, "-partition", "%s" % Partition, "-name", "%s" % Name, "-file" ,"%s" % DumpFile, "-cell",  "%s" % cellname]
        rc,output,outerr=afs.dao.bin.execute(CmdList)
        if rc:
             raise VolError("Error", outerr)
    
    def convert(self,VolName,Server,Partition,cellname, token) :
        """
        converts this RO-Volume to a RW
        """
        CmdList=["vos", "convertROtoRW","-server", "%s" % Server, "-partition", "%s" % Partition, "-id", "%s" % VolName, "-cell",  "%s" % cellname]
        rc,output,outerr=afs.dao.bin.execute(CmdList)
        if rc:
             raise VolError("Error", outerr)

    def create(self,VolName,Server,Partition,MaxQuota, cellname, token) :
        """
        create a Volume
        """
        id = 0
        CmdList=["vos", "create","-server", "%s" % Server, "-partition", "%s" % Partition, "-name", "%s" % Name , "-maxquota", "%s" % Quota, "-cell",  "%s" % cellname]
        rc,output,outerr=afs.dao.bin.execute(CmdList)
        if rc:
             raise VolError("Error", outerr)
        
        return id
    
    def remove(self,VolName,Server, Partition, cellname, token) :
        """
        remove this Volume from the Server
        """
        CmdList=["vos", "remove","-server", "%s" % Server, "-partition", "%s" % Partition, "-id", "%s" % VolName, "-cell",  "%s" % cellname ]
        rc,output,outerr=afs.dao.bin.execute(CmdList) 
        if rc:
             raise VolError("Error", outerr)
    
    
    def getVolGroupList(self, vid, cellname, token) :
        """
        update entry via vos examine from vol-server. 
        """
        
        CmdList = [afs.dao.bin.VOSBIN,"examine", "-id", "%s"  % vid , "-format","-cell", "%s" %  cellname]
        rc,output,outerr=afs.dao.bin.execute(CmdList)
       
        if rc :
            raise VolError("Error", outerr)
        

        line_no = 0
        line = output[line_no]
        volGroup = []
        if re.search("Could not fetch the entry",line) or line == "VLDB: no such entry"  or re.search("Unknown volume ID or name",line) \
            or re.search("does not exist in VLDB",line) :
            return volGroup
            
        # first line gives Name, ID, Type, Used and Status  
        #volList = {"RW": [], "RO": [] }
        
        roID = 0
        rwID = 0
        bkId = 0
        numSite = 0
        numServer = 0
        
        #FIXME Escape line when you find 
        for i in range(0, len(output)):
            splits = output[i].split()
            #search server list section
            if splits[0] == "name":
                volname = splits[1]
                i += 26
            
            elif splits[0] == "RWrite:":
                # id Volume by type
                vid = {}
                vid['RW'] = splits[1]
                vid['RO'] = splits[3]
                if len(splits) > 4 :
                  vid['RO'] = splits[5] 
                  
                # Number of Sites
                i += 1
                splits = output[i].split() 
                numSite =  int(splits[4]) 
                
                for n in range(1, numSite):
                    splits = output[i+n].split()
                    type = splits[4]
                    volGroup.append({"id":vid[type], 'volname': volname, "type":type,"serv":splits[1],"part":afsutil.canonicalizePartition(splits[3])})
          
                break
        
        return volGroup
       

    def getVolume(self, vid, serv, part, cellname, token) :
        """
        Volume entry via vos examine from vol-server. 
        If Name is given, it takes precedence over ID
        """
        part = afsutil.canonicalizePartition(part)
        CmdList = [afs.dao.bin.VOSBIN,"examine",  "%s"  % vid ,"-format","-cell", "%s" % cellname]
        rc,output,outerr=afs.dao.bin.execute(CmdList)
        if rc :
            raise VolError("Error", outerr)
        
        line_no = 0
        line = output[line_no]
        vol = None
       
        if re.search("Could not fetch the entry",line) or line == "VLDB: no such entry"  or re.search("Unknown volume ID or name",line) \
            or re.search("does not exist in VLDB",line) :
            return vol
       
        # first line gives Name, ID, Type, Used and Status 
        find = False    
        vol  = {}
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
                    vol['vid']      = int(splits[1])
                    splits = output[i+2].split()
                    vol['serv']     = splits[1]
                    if len(splits) > 2:
                        vol['servername']     = splits[2]
                    splits = output[i+3].split()
                    vol['part']     = afsutil.canonicalizePartition(splits[1])
                    splits = output[i+4].split()
                    vol['status']     = splits[1]
                    splits = output[i+5].split()
                    vol['backupID'] = int(splits[1])
                    splits = output[i+6].split()
                    vol['parentID'] = int(splits[1])
                    splits = output[i+7].split()
                    vol['cloneID']  = int(splits[1])
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
                    vol['diskused']      = int(splits[1])
                    splits = output[i+19].split()
                    vol['maxquota']      = int(splits[1])
                    splits = output[i+20].split()
                    vol['minquota']      = int(splits[1])
                    splits = output[i+21].split()
                    vol['filecount']     = int(splits[1])
                    splits = output[i+22].split()
                    vol['dayUse']        = int(splits[1])
                    splits = output[i+23].split()
                    vol['weekUse']       = int(splits[1])
                    splits = output[i+24].split()
                    vol['spare2']        = splits[1]
                    splits = output[i+25].split()
                    vol['spare3']        = splits[1]
                                     
                    break
                else:
                    i = i+25
        
        if not find :
            vol = None
                    
        return vol
    
    
    def getVolStat(self, vid, serv, part, cellname, token):
        """
        Volume stats via vos examine extended from vol-server. 
        If Name is given, it takes precedence over ID
        """
        """
        CmdList = [afs.dao.bin.VOSBIN,"examine",  "%s"  % vid ,"-extended","-cell", "%s" % cellname]
        rc,output,outerr=afs.dao.bin.execute(CmdList)
        if rc :
            raise VolError("Error", outerr)
        
        line_no = 0
        line = output[line_no]
        vol = None
       
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
                    vol['vid']      = int(splits[1])
                    splits = output[i+2].split()
                    vol['serv']     = splits[1]
        """
    
    
