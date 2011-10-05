#!/usr/bin/python

import string,os,sys
import subprocess,types

VOSBIN="/usr/sbin/vos"
RXDEBUGBIN="/usr/sbin/rxdebug"
FSBIN="/usr/bin/fs"
OSDBIN="osd"
BOSBIN="/usr/sbin/bos"

def execute(CmdList) :
    if dryrun :
        print "DRYRUN: exec \"%s\"" % (string.join(CmdList))
        return 0,[],[]
    pipo=subprocess.Popen(CmdList,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    _output,_outerr=pipo.communicate()
    if pipo.returncode != 0 :
        sys.stderr.write("cmd: \"%s\" failed with %d\n" % (string.join(CmdList),pipo.returncode))
        sys.stderr.write("STDERR: %s\n" % _outerr)
        sys.exit(pipo.returncode)

    # get rid of whitespace
    _output=map(safeStrip,_output.split("\n"))
    _outerr=map(safeStrip,_outerr.split("\n"))

    output=[]
    for line in _output :
        if line == "" : continue
        output.append(line)

    outerr=[]
    for line in _outerr :
        if line == "" : continue
        outerr.append(line)
   
    return pipo.returncode,output,outerr


def safeStrip(Thing) :
    if type(Thing) == types.StringType :
        return Thing.strip()
    return
