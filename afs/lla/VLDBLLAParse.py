from VLDBLLAError import VLDBLLAError
import afs

def get_fileserver_list(rc, output, outerr, parseParamList, Logger):
    noresolve = parseParamList["kwargs"]["noresolve"]
    _cfg = parseParamList["kwargs"]["_cfg"]
    if rc :
        raise VLDBLLAError("Error: %s " %  outerr)
    servers = []
    i = 0
    while i < len(output) :
        if output[i].startswith("UUID:"):
            server = {}
            splits = output[i].split()
            server['uuid'] = splits[1]
            i = i + 1
            try :
                DNSInfo = afs.LOOKUP_UTIL[_cfg.cell].get_dns_info(output[i])
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

def get_fileserver_uuid(rc, output, outerr, parseParamList, Logger) :
    if rc :
        raise VLDBLLAError("Error: %s " %  outerr)
    uuid=output[0].split()[1]
    return uuid

def get_volume_list(rc, output, outerr, parseParamList, Logger) :
    noresolve = parseParamList["kwargs"]["noresolve"]
    _cfg = parseParamList["kwargs"]["_cfg"]
    if rc :
        raise VLDBLLAError("Error: %s " %  outerr)
    volumes = []
    # header is always 2 lines
    i = 1
    while i < len(output) :
        if "Total entries:" in output[i] or "Volume is currently LOCKED" in output[i] or "Volume is locked for a" in output[i]  :
            i += 1 
            continue
        Logger.debug("get_volume_list: parsing %s" % output[i:i+10]) 
         
        volume = {}
        # mpe.integr.revol.0010 
        volume["name"] = output[i].strip() 
        # RWrite: 536985599     ROnly: 536985600 
        splits=output[i+1].split()             
        if len(splits) == 6 :
            volume["BK"] = splits[5]
        elif len(splits) == 4 :
            volume["RO"] = splits[3]
        elif len(splits) == 2 :
            volume["BK"] = splits[1]
        volume["num_sites"] = int(output[i+2].split()[4])
        volume["rw_site"] = ""
        volume["ro_sites"] = []
        for l in range(volume["num_sites"]) :
            splits = output[i+3+l].split()
            DNSInfo = afs.LOOKUP_UTIL[_cfg.cell].get_dns_info(splits[1])
            if splits[4] == "RW" :
                if noresolve :
                    volume["rw_site"] = DNSInfo["ipaddrs"][0]
                else :
                    volume["rw_site"] = DNSInfo["names"][0]
            elif splits[4] == "RO" :
                if noresolve :
                    volume["ro_sites"].append(DNSInfo["ipaddrs"][0])
                else :
                    volume["ro_sites"].append(DNSInfo["names"][0])
        i = i + 3 + volume["num_sites"]
        volumes.append(volume)
    Logger.debug("get_volume_list: returning %s" % volumes[:10])     
    return volumes 

def unlock(rc, output, outerr, parseParamList, Logger) :
    if rc :
        raise VLDBLLAError("Error: %s " %  outerr)
    return True

def lock(rc, output, outerr, parseParamList, Logger) :
    if rc :
        raise VLDBLLAError("Error: %s " %  outerr)
    return True

def sync_vldb(rc, output, outerr, parseParamList, Logger) :
    if rc :
        raise VLDBLLAError("Error: %s " %  outerr)
    return True

def setaddrs(rc,output,outerr,parseParamList,Logger) :
    if rc :
        raise VLDBLLAError("Error: %s " %  outerr)
    raise VLDBLLAError("Not Implemented.")

def addsite(rc, output ,outerr, parseParamList, Logger) :
    if rc :
        raise VLDBLLAError("Error: %s " %  outerr)
    return True

def remsite(rc, output, outerr, parseParamList, Logger) :
    if rc :
        raise VLDBLLAError("Error: %s " %  outerr)
    return True

def sync_serv(rc,output,outerr,parseParamList,Logger) :
    if rc :
        raise VLDBLLAError("Error: %s " %  outerr)
    return True

