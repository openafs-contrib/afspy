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

if __name__ == "__main__"  :
   print "Some basic methods used for afspy"
   print humanReadableSize(32768*29+2342)
