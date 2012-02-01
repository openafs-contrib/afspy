#!/usr/bin/env python

import sys, os, string
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

# get a light-weight list of all fileservers :

FileServerList=CS.getFsList()
print "FileServers"
print "========="
for srv in FileServerList :
    print "%s: %s" %( string.join(srv.servernames, ","), string.join(srv.ipaddrs) )

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

