import re,sys
from afs.util import afsutil
from datetime import datetime
from afs.exceptions.VolError import VolError

def move(rc,output,outerr,parseParamList,Logger) :
    if rc:
        raise VolError("Error", outerr)
    return

def getVolIDList(rc,output,outerr,parseParamList,Logger) :
    if rc:
        raise VolError("Error", outerr)
    res=[]
    for l in output :
       l=l.strip()
       if len(l) == 0 or "Total" in l : continue
       res.append(int(l))
    return res

def getVolume(rc,output,outerr,parseParamList,Logger):
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
            if ((line1[1] == str(name_or_id) or\
	        line2[1] == str(name_or_id) ) and \
	        (line3[1] == serv or  line3[2] == serv or serv == None ) ) :
                find = True
                Logger.debug("Parsing.....")
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
                vol[instanceNo]['minquota']      = int(splits[1])
                splits = output[i+21].split()
                vol[instanceNo]['filecount']     = int(splits[1])
                splits = output[i+22].split()
                vol[instanceNo]['dayUse']        = int(splits[1])
                splits = output[i+23].split()
                vol[instanceNo]['weekUse']       = int(splits[1])
                splits = output[i+24].split()
                vol[instanceNo]['spare2']        = splits[1]
                splits = output[i+25].split()
                vol[instanceNo]['spare3']        = splits[1]
                i += 25
            else:
                Logger.debug("Rejected because of: %s" % (line1,line2,line3))
                i = i+25
        else :
            Logger.debug("Skipping line: %s" % output[i])
            i += 1
    if not find :
        Logger.info("Did not find volume %s" % name_or_id)
        vol = None
    return vol


def release(rc,output,outerr,parseParamList,Logger):
    if rc:
        raise VolError("Error", outerr)

def setBlockQuota(rc,output,outerr,parseParamList,Logger):
    if rc:
        raise VolError("Error", outerr)

def dump(rc,output,outerr,parseParamList,Logger):
    if rc:
        raise VolError("Error", outerr)

def restore(rc,output,outerr,parseParamList,Logger):
    if rc:
        raise VolError("Error", outerr)

def convert(rc,output,outerr,parseParamList,Logger):
    if rc:
        raise VolError("Error", outerr)

def create(rc,output,outerr,parseParamList,Logger):
    if rc:
        raise VolError("Error", outerr)

def remove(rc,output,outerr,parseParamList,Logger):
    if rc:
        raise VolError("Error", outerr)
