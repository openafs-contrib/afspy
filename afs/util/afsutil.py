#!/usr/bin/python

import re,types

useRXOSD=True

SizeUnit=['kB','MB','GB','TB','PB']
PartRX=re.compile("/?(?:vicep)?([a-z][a-z]?)")

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
           raise "Cannot canonicalize \"%s\"" 
       partition=MObj.groups()[0] 
    return partition
 
 
def canonicalizeVolume(volname):
    
    if volname.endswith(".readonly"):
        return volname[0:len(volname)-9]
    
    if volname.endswith(".backup"):
         return volname[0:len(volname)-6]

 
 
if __name__ == "__main__"  :
   print "Some basic methods used for afspy"
   print humanReadableSize(32768*29+2342)
