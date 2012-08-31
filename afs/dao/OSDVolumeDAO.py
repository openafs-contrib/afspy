import re,sys,types,string
import afs.dao.bin

from datetime import datetime
from afs.exceptions.VolError import VolError
from afs.util import afsutil
from afs.dao.VolumeDAO import VolumeDAO

class OSDVolumeDAO(VolumeDAO) :
    """
    Provides Methods to query and modify live AFS-Volumes
    Overlay to VolumesDAO adding OSD-functionality
    """
    
    def __init__(self) :
        VolumeDAO.__init__(self)
        return

    def create(self,VolName,Server,Partition, MaxQuota, MaxFiles,osdpolicy, cellname, token) :
        """
        create a Volume
        """
        id = 0
        CmdList=[afs.dao.bin.VOSBIN, "create","-server", "%s" % Server, "-partition", "%s" % Partition, "-name", "%s" % VolName , "-maxquota", "%s" % MaxQuota, 
                 "-filequota", "%s" % MaxFiles ,"-osdpolicy" ,osdpolicy, "-cell",  "%s" % cellname]
        rc,output,outerr=self.execute(CmdList)
        if rc:
             raise VolError("Error", outerr)
        
        return id
    
    
    def getVolGroupList(self, vid, cellname, token) :
        """
        update entry via vos examine from vol-server. 
        """
        
        CmdList = [afs.dao.bin.VOSBIN,"examine", "-id", "%s"  % vid , "-format","-cell", "%s" %  cellname]
        rc,output,outerr=self.execute(CmdList)
       
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
        
        numSite = 0
        
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
                if len(splits) > 2:
                  vid['RO'] = splits[3]
                if len(splits) > 4 :
                  vid['BK'] = splits[5] 
                  
                # Number of Sites
                i += 1
                splits = output[i].split() 
                numSite =  int(splits[4]) 
                
                for n in range(0, numSite):
                    splits = output[i+1+n].split()
                    type = splits[4]
                    volGroup.append({"id":vid[type], 'volname': volname, "type":type,"serv":splits[1],"part":afsutil.canonicalizePartition(splits[3])})
          
                break
        return volGroup
       

    def getVolume(self, name_or_id, serv, part,   cellname, token) :
        """
        Volume entry via vos examine from vol-server. 
        """
        if part :
            part = afsutil.canonicalizePartition(part)
        CmdList = [afs.dao.bin.VOSBIN,"examine",  "%s"  % name_or_id ,"-format","-cell", "%s" % cellname]
        rc,output,outerr=self.execute(CmdList)
        if rc :
            raise VolError("Error", outerr)
        
        line_no = 0
        line = output[line_no]
       
        if re.search("Could not fetch the entry",line) or line == "VLDB: no such entry"  or re.search("Unknown volume ID or name",line) \
            or re.search("does not exist in VLDB",line) :
            self.Logger.info("Did not find volume %s in VLDB" % name_or_id)
            return None
        
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
                if ((line1[1] == str(name_or_id) or\
                    line2[1] == str(name_or_id) ) and \
                    (line3[1] == serv or \
                    line3[2] == serv) and \
                    ((afsutil.canonicalizePartition(line4[1]) == part) or (part == None))) :
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
                    vol['filecount']     = int(splits[1])
                    splits = output[i+21].split()
                    vol['dayUse']        = int(splits[1])
                    splits = output[i+22].split()
                    vol['weekUse']       = int(splits[1])
                    splits = output[i+23].split()
                    vol['osdPolicy']        = splits[1]
                    splits = output[i+24].split()
                    vol['filequota']        = splits[1]
                    break
                else:
                    i = i+25
        
        if not find :
            self.Logger.info("Did not find volume %s" % name_or_id)
            vol = None
                    
        return vol
   
    def traverse(self,Servers, name_or_id, cellname, token) :
        self.Logger.debug("Entering traverse with Servers=%s, name_or_id=%s, cellname=%s, token=%s" % (Servers, name_or_id, cellname, token) )
        Converter={"B" : 1, "KB" : 1024, "MB" : 1024*1024, "GB" : 1024*1024*1024, "TB" : 1024*1024*1024*1024}
        histogram={}
        if type(Servers) == types.ListType :
            Servers = string.join(Servers," ")
        CmdList=[afs.dao.bin.VOSBIN, "traverse","-server", "%s" % Servers,"-id", "%s" % name_or_id,"-cell", "%s" % cellname]
        rc,output,outerr=self.execute(CmdList)
        if rc or "AFSVolTraverse failed" in string.join(outerr) :
            raise VolError("Cannot traverse volume: %s" % outerr)
        # jump to logical histogram
        histogram["logical"]=[]
        i=0
        while 1 :
            if "File Size Range" in output[i] : break
            i += 1
        i+=2
        while 1 :
            if "---------" in output[i] : break
            lowerSize,lowerUnit,dummy,upperSize,upperUnit,numFiles,FilesPerc,runFilesPerc,data,dataUnit,DataPrc,runDataPerc= output[i].split()
            histogram["logical"].append({"lowerSize" : int(lowerSize)*Converter[lowerUnit], "upperSize" : int(upperSize)*Converter[upperUnit],
                                         "numFiles" : int(numFiles),"binData" : round(float(data)*Converter[dataUnit])})
            i += 1
        i += 1
        splits=output[i].split()
        self.Logger.debug("splits=%s"% splits) 
        histogram["totals"]={"logical": {"numFiles" : int(splits[1]),"Data" : round(float(splits[3])*Converter[splits[4]])}}
        # "storage usage"
        i+=3
        splits=output[i].split()
        # localdisk
        self.Logger.debug("splits=%s"% splits) 
        histogram["storageUsage"]={"fileserver" : {"numFiles" : int(splits[2]),"Data" :  round(float(splits[4])*Converter[splits[5]])}}
        histogram["storageUsage"]["online"] = {"numFiles" : 0, "Data" : 0}
        histogram["storageUsage"]["archival"] = {"numFiles" : 0, "Data" : 0} 
        histogram["storageUsage"]["detailed"] = []
        i+=1
        while 1 :
            if "---------" in output[i] : break
            splits=output[i].split()
            if splits[0] == "arch." :
                histogram["storageUsage"]["archival"]["numFiles"] += int(splits[4])
                histogram["storageUsage"]["archival"]["Data"] += round(float(splits[6])*Converter[splits[7]])
                histogram["storageUsage"]["detailed"].append({"isArchival" : 1,"osdid": int(splits[2]),"numFiles": int(splits[4]),"Data" : round(float(splits[6])*Converter[splits[7]])})
            else :
                histogram["storageUsage"]["online"]["numFiles"] += int(splits[3])
                histogram["storageUsage"]["online"]["Data"] += round(float(splits[5])*Converter[splits[6]])
                histogram["storageUsage"]["detailed"].append({"isArchival" : 0,"osdid": int(splits[1]),"numFiles": int(splits[3]),"Data" : round(float(splits[5])*Converter[splits[6]])})
            i += 1
        i += 1
        splits=output[i].split()
        histogram["totals"]["storageUsage"]={"numFiles" : int(splits[1]),"Data" : round(float(splits[3])*Converter[splits[4]])}
        # data without a copy
        i+=3 
        # localdisk
        splits=output[i].split()
        histogram["withoutCopy"]={"fileserver":{"numFiles" : int(splits[4]),"Data" :  round(float(splits[6])*Converter[splits[7]])}}
        histogram["withoutCopy"]["online"] = {"numFiles" : 0, "Data" : 0}
        histogram["withoutCopy"]["archival"] = {"numFiles" : 0, "Data" : 0}
        histogram["withoutCopy"]["detailed"] = []
        i+=1 
        while 1 :
            if "---------" in output[i] : break
            splits=output[i].split()
            if splits[0] == "arch." :
                histogram["withoutCopy"]["archival"]["numFiles"] += int(splits[4])
                histogram["withoutCopy"]["archival"]["Data"] += round(float(splits[6])*Converter[splits[7]])
                histogram["withoutCopy"]["detailed"].append({"isArchival" : 1,"osdid": int(splits[2]),"numFiles": int(splits[4]),"Data" : round(float(splits[6])*Converter[splits[7]])})
            else :
                histogram["withoutCopy"]["online"]["numFiles"] += int(splits[3])
                histogram["withoutCopy"]["online"]["Data"] += round(float(splits[5])*Converter[splits[6]])
                histogram["withoutCopy"]["detailed"].append({"isArchival" : 0,"osdid": int(splits[1]),"numFiles": int(splits[3]),"Data" : round(float(splits[5])*Converter[splits[6]])})
            i += 1
        i += 1
        splits=output[i].split()
        histogram["totals"]["withoutCopy"]={"numFiles" : int(splits[1]),"Data" : round(float(splits[3])*Converter[splits[4]])}
        self.Logger.debug("returning : %s" % histogram) 
        return histogram
