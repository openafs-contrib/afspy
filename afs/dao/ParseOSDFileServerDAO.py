import re, datetime
from afs.util import afsutil
from afs.exceptions.FServError import FServError

def getVolList(rc,output,outerr,parseParamList,Logger) :
    if rc :
        raise FServError("Error",outerr)
    # first line gives Name, ID, Type, Used and Status 
    volList = [] 
    dateT=datetime.datetime(1970, 1, 1)
    i = 0
    while i < len(output):
        while output[i] != "BEGIN_OF_ENTRY":
             i = i+1  
             if i >= len(output): break
        if i >= len(output): break
        #Beginnig block
        splits = output[i].split()
        if splits[0] == "BEGIN_OF_ENTRY":
                vol = {}
                splits = output[i+1].split()
                # Invalid volume, something wrong
                if splits[0] != 'name':
                    #vol['valid'] = False 
                    if  splits[0] == 'id':
                        vol['vid']      = int(splits[1])
                    
                    splits = output[i+2].split()
                    if  splits[0] == 'serv':
                        vol['servername']     = splits[1] 
                    
                    splits = output[i+3].split()   
                    if  splits[0] == 'part':
                         vol['part']     = afsutil.canonicalize_partition(splits[1]) 
                         
                    splits = output[i+4].split()
                    if  splits[0] == 'status':
                        vol['status']     = splits[1] 
                    
                    while output[i] != "END_OF_ENTRY":
                        i = i+1  
                        
                # Valid volume                           
                else:  
                    vol['vid'] = "UNSET"
                    try: 
                      vol['name']     = splits[1]
                      splits = output[i+2].split()
                      Logger.debug("splits = %s" % splits)
                      vol['vid']      = int(splits[1])
                      splits = output[i+3].split()
                      Logger.debug("splits = %s" % splits)
                    except :
                        # XXX Here we need a flag to show that parsing was not complete
                        # or a list of Volumes which need to be reparsed.
                        # this will be in the return-code
                        while output[i] != "END_OF_ENTRY":
                            i = i+1
                        Logger.debug("Cannot parse name of volume with id=%s! Skipping." % vol['vid'])
                        continue
                    
                    if len(splits) > 2:
                       vol['servername']     = splits[2]
                    else:
                       #Only ip is available 
                       vol['servername']     = splits[1] 
                    splits = output[i+4].split()
                    Logger.debug("splits = %s" % splits)
                    vol['part']     = afsutil.canonicalize_partition(splits[1])
                    splits = output[i+5].split()
                    Logger.debug("splits = %s" % splits)
                    vol['status']     = splits[1]
                    if vol['status'] != "OK" : 
                        while output[i] != "END_OF_ENTRY":
                            i = i+1
                        continue
                    splits = output[i+6].split()
                    Logger.debug("splits = %s" % splits)
                    vol['backupID'] = int(splits[1])
                    splits = output[i+7].split()
                    Logger.debug("splits = %s" % splits)
                    vol['parentID'] = int(splits[1])
                    splits = output[i+8].split()
                    Logger.debug("splits = %s" % splits)
                    vol['cloneID']  = int(splits[1])
                    splits = output[i+9].split()
                    Logger.debug("splits = %s" % splits)
                    vol['inUse']    = splits[1]
                    splits = output[i+10].split()
                    Logger.debug("splits = %s" % splits)
                    vol['needsSalvaged'] = splits[1]
                    splits = output[i+11].split()
                    Logger.debug("splits = %s" % splits)
                    vol['destroyMe']     = splits[1]
                    splits = output[i+12].split()
                    Logger.debug("splits = %s" % splits)
                    vol['type']          = splits[1]
                    splits = output[i+13].split()
                    Logger.debug("splits = %s" % splits)
                    vol['creationDate']  =  dateT.fromtimestamp(float(splits[1]))
                    splits = output[i+14].split()
                    Logger.debug("splits = %s" % splits)
                    vol['accessDate']    = dateT.fromtimestamp(float(splits[1]))
                    splits = output[i+15].split()
                    Logger.debug("splits = %s" % splits)
                    vol['updateDate']    = dateT.fromtimestamp(float(splits[1]))
                    splits = output[i+16].split()
                    Logger.debug("splits = %s" % splits)
                    vol['backupDate']     = dateT.fromtimestamp(float(splits[1]))
                    splits = output[i+17].split()
                    Logger.debug("splits = %s" % splits)
                    vol['copyDate']      = dateT.fromtimestamp(float(splits[1]))
                    splits = output[i+18].split()
                    Logger.debug("splits = %s" % splits)
                    vol['flags']         = splits[1]
                    splits = output[i+19].split()
                    Logger.debug("splits = %s" % splits)
                    vol['diskused']      = int(splits[1])
                    splits = output[i+20].split()
                    Logger.debug("splits = %s" % splits)
                    vol['maxquota']      = int(splits[1])
                    splits = output[i+21].split()
                    Logger.debug("splits = %s" % splits)
                    vol['osdPolicy']     = int(splits[1])
                    splits = output[i+22].split()
                    Logger.debug("splits = %s" % splits)
                    vol['filecount']        = int(splits[1])
                    splits = output[i+23].split()
                    Logger.debug("splits = %s" % splits)
                    vol['dayUse']       = int(splits[1])
                    splits = output[i+24].split()
                    Logger.debug("splits = %s" % splits)
                    vol['weekUse']        = int(splits[1])
                    splits = output[i+25].split()
                    Logger.debug("splits = %s" % splits)
                    # ignore spare fields
                    #vol['spare2']        = int(splits[1])
                    splits = output[i+26].split()
                    Logger.debug("splits = %s" % splits)
                    vol['filequota']        = int(splits[1])
                    i = i+27
                volList.append(vol)
    return volList

def getIdVolList(rc,output,outerr,parseParamList,Logger):
    RX=re.compile("^(\d+)")
    volIds = []
    for line in output [1:]:
        m=RX.match(line)
        if not m :
            raise FServError("Error parsing output :%s " % line)
        if m :
           volIds.append(m.groups()[0]) 
    return volIds
