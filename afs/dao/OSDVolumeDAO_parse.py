import re,sys,string
from datetime import datetime
from afs.exceptions.VolError import VolError
from afs.util import afsutil

def create(rc,output,outerr,parseParamList,Logger) :
    if rc:
        raise VolError("Error", outerr)
    return

def getVolume(rc,output,outerr,parseParamList,Logger) : 
    """
    returns list of Volumes matching name_or_id
    """
       
    if rc:
        raise VolError("Error", outerr)
    name_or_id=parseParamList["args"][0]
    serv=parseParamList["kwargs"]["serv"]

    Logger.debug("getVolume: got=%s" % output)

    line_no = 0
    line = output[line_no]
   
    if re.search("Could not fetch the entry",line) or line == "VLDB: no such entry"  or re.search("Unknown volume ID or name",line) \
        or re.search("does not exist in VLDB",line) :
        Logger.info("Did not find volume %s in VLDB" % name_or_id)
        return None
    
    # first line gives Name, ID, Type, Used and Status 
    find = False    
    vol  = []
    instanceNo = -1
    i = 0
    while i < len(output):
        splits = output[i].split()
        #Beginnig block
        if splits[0] == "name":
            Logger.debug("Reading line: %s" % output[i])
            instanceNo += 1
            vol.append({})
            line1 = output[i].split()
            line2 = output[i+1].split()
            line3 = output[i+2].split()
            line4 = output[i+3].split()
            if ((line1[1] == str(name_or_id) or line2[1] == str(name_or_id) ) and \
                (line3[1] == serv or line3[2] == serv or serv == None)) :
                find = True
                splits = output[i].split()
                vol[instanceNo]['name']     = splits[1]
                splits = output[i+1].split()
                vol[instanceNo]['vid']      = int(splits[1])
                splits = output[i+2].split()
                vol[instanceNo]['serv']     = splits[1]
                if len(splits) > 2:
                    vol[instanceNo]['servername']     = splits[2]
                splits = output[i+3].split()
                vol[instanceNo]['part']     = afsutil.canonicalizePartition(splits[1])
                splits = output[i+4].split()
                vol[instanceNo]['status']     = splits[1]
                splits = output[i+5].split()
                vol[instanceNo]['backupID'] = int(splits[1])
                splits = output[i+6].split()
                vol[instanceNo]['parentID'] = int(splits[1])
                splits = output[i+7].split()
                vol[instanceNo]['cloneID']  = int(splits[1])
                splits = output[i+8].split()
                vol[instanceNo]['inUse']    = splits[1]
                splits = output[i+9].split()
                vol[instanceNo]['needsSalvaged'] = splits[1]
                splits = output[i+10].split()
                vol[instanceNo]['destroyMe']     = splits[1]
                splits = output[i+11].split()
                vol[instanceNo]['type']          = splits[1]
                splits = output[i+12].split()
                vol[instanceNo]['creationDate']  =  datetime.fromtimestamp(float(splits[1]))
                splits = output[i+13].split()
                vol[instanceNo]['accessDate']  =  datetime.fromtimestamp(float(splits[1]))
                splits = output[i+14].split()
                vol[instanceNo]['updateDate']    = datetime.fromtimestamp(float(splits[1]))
                splits = output[i+15].split()
                vol[instanceNo]['backupDate']     = datetime.fromtimestamp(float(splits[1]))
                splits = output[i+16].split()
                vol[instanceNo]['copyDate']      = datetime.fromtimestamp(float(splits[1]))
                splits = output[i+17].split()
                vol[instanceNo]['flags']         = splits[1]
                splits = output[i+18].split()
                vol[instanceNo]['diskused']      = int(splits[1])
                splits = output[i+19].split()
                vol[instanceNo]['maxquota']      = int(splits[1])
                splits = output[i+20].split()
                vol[instanceNo]['filecount']     = int(splits[1])
                splits = output[i+21].split()
                vol[instanceNo]['dayUse']        = int(splits[1])
                splits = output[i+22].split()
                vol[instanceNo]['weekUse']       = int(splits[1])
                splits = output[i+23].split()
                vol[instanceNo]['osdPolicy']        = int(splits[1])
                splits = output[i+24].split()
                vol[instanceNo]['filequota']        = int(splits[1])
                i += 25
            else:
                Logger.debug("Dismissing because of :")
                Logger.debug("line1=%s" % line1)
                Logger.debug("line2=%s" % line2)
                Logger.debug("line3=%s" % line3)
                i = i+25
        else :
            Logger.debug("Skipping: %s" % output[i])
            i += 1
    if not find :
        Logger.info("Did not find volume %s" % name_or_id)
        vol = None
    return vol

def traverse(rc,output,outerr,parseParamList,Logger) :
    if rc or "AFSVolTraverse failed" in string.join(outerr) :
        raise VolError("Cannot traverse volume: %s" % outerr)
    histogram={}
    Converter={"B" : 1, "KB" : 1024, "MB" : 1024*1024, "GB" : 1024*1024*1024, "TB" : 1024*1024*1024*1024, "PB" : 1024*1024*1024*1024*1024}
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
    Logger.debug("splits=%s"% splits) 
    histogram["totals"]={"logical": {"numFiles" : int(splits[1]),"Data" : round(float(splits[3])*Converter[splits[4]])}}
    # "storage usage"
    i+=3
    splits=output[i].split()
    Logger.debug("splits=%s"% splits) 
    # localdisk
    Logger.debug("splits=%s"% splits) 
    histogram["storageUsage"]={"fileserver" : {"numFiles" : int(splits[2]),"Data" :  round(float(splits[4])*Converter[splits[5]])}}
    histogram["storageUsage"]["online"] = {"numFiles" : 0, "Data" : 0}
    histogram["storageUsage"]["archival"] = {"numFiles" : 0, "Data" : 0} 
    histogram["storageUsage"]["detailed"] = []
    i+=1
    while 1 :
        if "---------" in output[i] : break
        splits=output[i].split()
        Logger.debug("splits=%s"% splits) 
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
    Logger.debug("splits=%s"% splits) 
    histogram["totals"]["storageUsage"]={"numFiles" : int(splits[1]),"Data" : round(float(splits[3])*Converter[splits[4]])}
    # data without a copy
    i+=3 
    # localdisk
    splits=output[i].split()
    Logger.debug("splits=%s"% splits) 
    histogram["withoutCopy"]={"fileserver":{"numFiles" : int(splits[4]),"Data" :  round(float(splits[6])*Converter[splits[7]])}}
    histogram["withoutCopy"]["online"] = {"numFiles" : 0, "Data" : 0}
    histogram["withoutCopy"]["archival"] = {"numFiles" : 0, "Data" : 0}
    histogram["withoutCopy"]["detailed"] = []
    i+=1 
    while 1 :
        if "---------" in output[i] : break
        splits=output[i].split()
        Logger.debug("splits=%s"% splits) 
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
    Logger.debug("splits=%s"% splits) 
    histogram["totals"]["withoutCopy"]={"numFiles" : int(splits[1]),"Data" : round(float(splits[3])*Converter[splits[4]])}
    Logger.debug("returning : %s" % histogram) 
    return histogram
