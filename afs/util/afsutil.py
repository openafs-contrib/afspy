#!/usr/bin/python

import re,types, socket, logging,string
import afs


useRXOSD=True
# log-level is set in AfsConfig
Logger=logging.getLogger("afs.util")

SizeUnit=['kB','MB','GB','TB','PB']
PartRX=re.compile("/?(?:vicep)?([a-z][a-z]?)")


class utilError(Exception):
    def __init__(self, message, Errors=[]):
        Exception.__init__(self, message)
        # Now for your custom code...
        self.Errors = Errors
  
    def __str__(self):
      #FIXME parse build a complete message with stack
      return repr(self.message)

def humanReadableSize(Size) :
    for s in range(len(SizeUnit)) :
        if float(Size) / (1024**(s+1)) < 1 : break
    return "%3.2f %s" % (float(Size) / (1024**s),SizeUnit[s])  

def canonicalizePartition(part) :
    if type(part) == types.StringType :
       if part.isdigit() :
           part=int(part)
    if type(part) == types.IntType : 
       firstLetter=part/26
       secondLetter=part%26
       partition=""
       if firstLetter != 0 :
           partition += chr(ord("a")+firstLetter) 
       partition += chr(ord("a")+secondLetter) 
    else :
       MObj=PartRX.match(part)
       if not MObj :
           raise utilError("Cannot canonicalize \"%s\"" % part)
       partition=MObj.groups()[0] 
    return partition
 
 
def canonicalizeVolume(volname):
    
    if volname.endswith(".readonly"):
        return volname[0:len(volname)-9]
    
    if volname.endswith(".backup"):
        return volname[0:len(volname)-6]

def getDNSInfo(name_or_ip):
    """ 
    get DNS-info about server
    """
    if name_or_ip in afs.defaultConfig.hosts.keys() :
        Logger.debug("%s is hard-mapped to (%s,%s)" % (name_or_ip, [name_or_ip,], afs.defaultConfig.hosts[name_or_ip]))
        return [name_or_ip,],afs.defaultConfig.hosts[name_or_ip]
    for hn in afs.defaultConfig.hosts :
        if name_or_ip in afs.defaultConfig.hosts[hn] :
            Logger.debug("%s is hard-mapped to (%s,%s)" % (name_or_ip, [hn,],afs.defaultConfig.hosts[hn]))
            return [hn,],afs.defaultConfig.hosts[hn]            
    DNSInfo=socket.gethostbyaddr(name_or_ip)
    servernames=[DNSInfo[0]]+DNSInfo[1]
    ipaddrs=DNSInfo[2]
    Logger.debug("%s resolves to (%s,%s)" % (name_or_ip, servernames, ipaddrs))
    if "nxdomain" in servernames[0] : raise utilError("cannot resolve DNS")
    return servernames, ipaddrs

def isName(ambiguous) :
    """
    checks if name_or_ip or name_or_id is acutally the name
    """
    ambiguous=ambiguous.strip()
    if len(ambiguous) == 0 :
        raise utilError("isName called with empty string!")
    Logger.debug("isName: got '%s'" % ambiguous)
    if ambiguous[0] in string.digits : 
        return False
    else :
        return True


#
# FSUUID - translations
#
# In AFS all fileservers have a uuid. This is used in the database
# to identify a fileserver
# 

def getFSUUIDByName_IP(name_or_ip,CFG,cached=False):
    """
    returns UUID of a fileserver, which is used as key for server-entries
    in other tables. This does not silently update the Cache
    """
    if cached :
        return getFSUUIDByName_IP_FromCache(name_or_ip,CFG)
    from afs.dao.VLDbDAO import VLDbDAO
    Logger.debug("getFSUUID: called with %s" % name_or_ip)
    servernames, ipaddrs=getDNSInfo(name_or_ip)
    uuid=""
    _vlDAO=VLDbDAO()
    uuid=_vlDAO.getFsUUID(name_or_ip,CFG.CELL_NAME,None)
    return uuid

def getFSUUIDByName_IP_FromCache(name_or_ip,CFG):
    """
    get data from Cache
    """
    from DBManager import DBManager
    from afs.model.Server import Server
    if not CFG.DB_CACHE:
        raise AfsError("DB_CACHE not configured")
    DBManager=DBManager(CFG)
    Logger.debug("getFSUUIDFromCache: called with %s" % name_or_ip)
    if isName(name_or_ip) :
        list=DBManager.getFromCacheByListElement(Server,Server.servernames_js,name_or_ip)         
    else :
        list=DBManager.getFromCacheByListElement(Server,Server.ipaddrs_js,name_or_ip)         
    uuidlist=[] 
    for l in list :
        uuidlist.append(l.uuid)
    if len(uuidlist) == 0:
        return None
    elif len(uuidlist) == 1 :
        return uuidlist[0]
    else :
        return uuidlist

def getHostnameByFSUUID(uuid,CFG,cached=False) :
    """
    returns hostname of a fileserver by uuid
    """
    from afs.dao.VLDbDAO import VLDbDAO
    _vlDAO=VLDbDAO()
    for fs in _vlDAO.getFsServList(CFG.CELL_NAME,None ) :
        if fs['uuid'] == uuid :
           return fs['name_or_ip']
    return None

def getHostnameByFSUUIDFromCache(uuid,CFG,cached=False) :
    """
    return first hostname for given uuid 
    """
    from DBManager import DBManager
    from afs.model.Server import Server
    if not CFG.DB_CACHE:
        raise AfsError("DB_CACHE not configured")
    list=DBManager.getFromCacheByListElement(Server,Server.uuid,uuid)         
    if len(list) > 0 :
        return list[0]
    else :
        return None
    


if __name__ == "__main__"  :
   print "Some basic methods used for afspy"
   print humanReadableSize(32768*29+2342)
