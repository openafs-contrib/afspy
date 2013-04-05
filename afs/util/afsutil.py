#!/usr/bin/python

import re,types, socket, logging,string
import afs


useRXOSD=True
# log-level is set in AfsConfig
Logger=logging.getLogger("afs.util")
SizeUnit=['K', 'M','G','T','P']
PartRX=re.compile("/?(?:vicep)?([a-z][a-z]?)")
HumanSizeRX=re.compile("(\d+)([KMGTP]?)")


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

def parseHumanWriteableSize(Size) :
    """
    return absolute Value of sth like 100M
    base 1024 used.
    """ 
    MObj=HumanSizeRX.match(Size)
    if not MObj:
	raise utilError("Cannot parse value %s. Should be an integer with an optional size-unit of [K,M,G,T,P]")  
    number,su=MObj.groups()
    number=int(number)
    multi=1
    if len(su) != 0 : 
        for s in range(len(SizeUnit)) :
            if su == SizeUnit[s] :
                multi = 1024**(s+1)
                break

    return multi*number            


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

def isName(ambiguous) :
    """
    checks if name_or_ip or name_or_id is acutally the name or an numerical ID
    """
    # first, convert to string 
    ambiguous = "%s" % ambiguous    
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
