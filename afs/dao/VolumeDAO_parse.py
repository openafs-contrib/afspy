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


def getVolGroupList(rc,output,outerr,parseParamList,Logger) :
    if rc:
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
            if len(splits) > 3 :
                vid['RO'] = splits[3]
            else :
                sys.stderr.write("XXX: %s\n" % output[i])
                vid['RO'] = -1
            if len(splits) > 5 :
                vid['BK'] = splits[5] 
            else :
                vid['BK'] = -1
              
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

def getVolume(rc,output,outerr,parseParamList,Logger):
    if rc:
        raise VolError("Error", outerr)
    name_or_id=parseParamList["args"]["name_or_id"]
    serv=parseParamList["args"]["serv"]
    part=parseParamList["args"]["part"]

    line_no = 0
    line = output[line_no]

    if re.search("Could not fetch the entry",line) or line == "VLDB: no such entry"  or re.search("Unknown volume ID or name",line) \
        or re.search("does not exist in VLDB",line) :
        Logger.info("Did not find volume %s in VLDB" % name_or_id)
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
