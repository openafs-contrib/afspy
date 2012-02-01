#!/usr/bin/env python

import sys, os, string, logging
sys.path.append("..")
from afs.util.AfsConfig import AfsConfig, setupDefaultConfig
from afs.util.options import define, options
from afs.service.CellService import CellService
import afs


# setup Config
setupDefaultConfig()
afs.defaultConfig.CELL_NAME="ipp-garching.mpg.de"

# init services
CS = CellService()

# uncomment if debug wanted
#CS.Logger.setLevel(logging.DEBUG)

# get a light-weight list of all fileservers :

FileServerList=CS.getFsList(includeParts=True)
print "FileServers"
print "========="
for srv in FileServerList :
    print "%s: %s" %( string.join(srv.servernames, ","), string.join(srv.ipaddrs) )
    for p in srv.parts :
        print "\t%s, total: %u free: %u " % (p.name, p.size, p.free)
# get a light-weight list of all dbservers

print "DBServer"
print "======="
DBServerList=CS.getDBList(FileServerList[0].servernames[0])
for srv in  DBServerList :
    print "%s: %s" %( string.join(srv.servernames, ","), string.join(srv.ipaddrs) ), 
    if srv.clonedbserver :
        print " --- CLONE"
    else :
        print

