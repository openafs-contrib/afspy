from VLDBDAOError import VLDBDAOError
import afs

def getFsServList(rc,output,outerr,parseParamList,Logger):
    noresolve=parseParamList["kwargs"]["noresolve"]
    _cfg=parseParamList["kwargs"]["_cfg"]
    if rc :
        raise VLDBDAOError("Error: %s " %  outerr)
    servers = []
    i = 0
    while i < len(output) :
        if output[i].startswith("UUID:"):
            server = {}
            splits = output[i].split()
            server['uuid'] = splits[1]
            i = i + 1
            try :
                DNSInfo=afs.LOOKUP_UTIL[_cfg.cell].get_dns_info(output[i])
            except :
                server['name_or_ip'] = output[i]
                Logger.warn("Cannot resolv name_or_ip \'%s\'. Leaving it as it is." % output[i]  )
                continue
            if noresolve :
                server['name_or_ip'] = DNSInfo["ipaddrs"][0]
            else :
                server['name_or_ip'] = DNSInfo["names"][0]
            servers.append(server)
        i += 1
    return servers

def get_fileserver_uuid(rc,output,outerr,parseParamList,Logger) :
    if rc :
        raise VLDBDAOError("Error: %s " %  outerr)
    uuid=output[0].split()[1]
    return uuid

def getVolumeList(rc,output,outerr,parseParamList,Logger) :
    noresolve=parseParamList["kwargs"]["noresolve"]
    _cfg=parseParamList["kwargs"]["_cfg"]
    if rc :
        raise VLDBDAOError("Error: %s " %  outerr)
    Volumes=[]
    # header is always 2 lines
    i = 1
    while i < len(output) :
        if "Total entries:" in output[i] or "Volume is currently LOCKED" in output[i] or "Volume is locked for a" in output[i]  :
            i += 1 
            continue
        Logger.debug("getVolumeList: parsing %s" % output[i:i+10]) 
         
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
            DNSInfo = afs.LOOKUP_UTIL[_cfg.cell].get_dns_info(splits[1])
            if splits[4] == "RW" :
                if noresolve :
                    Volume["RWSite"] = DNSInfo["ipaddrs"][0]
                else :
                    Volume["RWSite"] = DNSInfo["names"][0]
            elif splits[4] == "RO" :
                if noresolve :
                    Volume["ROSites"].append(DNSInfo["ipaddrs"][0])
                else :
                    Volume["ROSites"].append(DNSInfo["names"][0])
        i = i + 3 + Volume["numSites"]
        Volumes.append(Volume)
    Logger.debug("getVolumeList: returning %s" % Volumes[:10])     
    return Volumes 

def unlock(rc,output,outerr,parseParamList,Logger) :
    if rc :
        raise VLDBDAOError("Error: %s " %  outerr)
    raise VLDBDAOError("Not Implemented.")

def lock(rc,output,outerr,parseParamList,Logger) :
    if rc :
        raise VLDBDAOError("Error: %s " %  outerr)
    raise VLDBDAOError("Not Implemented.")

def syncVLDB(rc,output,outerr,parseParamList,Logger) :
    if rc :
        raise VLDBDAOError("Error: %s " %  outerr)
    raise VLDBDAOError("Not Implemented.")

def setaddrs(rc,output,outerr,parseParamList,Logger) :
    if rc :
        raise VLDBDAOError("Error: %s " %  outerr)
    raise VLDBDAOError("Not Implemented.")

def addsite(rc,output,outerr,parseParamList,Logger) :
    if rc :
        raise VLDBDAOError("Error: %s " %  outerr)
    return 

def remsite(rc,output,outerr,parseParamList,Logger) :
    if rc :
        raise VLDBDAOError("Error: %s " %  outerr)
    raise VLDBDAOError("Not Implemented.")

def syncServ(rc,output,outerr,parseParamList,Logger) :
    if rc :
        raise VLDBDAOError("Error: %s " %  outerr)
    raise VLDBDAOError("Not Implemented.")

