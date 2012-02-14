#!/usr/bin/env python

import sys, string, time
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

def printServerList(FileServerList, DBServerList):
    print "FileServers"
    print "========="
    for srv in FileServerList :
        print "%s: %s" %( srv.servernames[0], string.join(srv.ipaddrs, ",") )
        for p in srv.parts :
            print "\t%s, total: %u free: %u " % (p.name, p.size, p.free)
    print "DBServer"
    print "======="
    for srv in  DBServerList :
        print "%s: %s" %( srv.servernames[0], string.join(srv.ipaddrs, ",") ), 
        if srv.clonedbserver :
            print " --- CLONE"
        else :
            print

# get a light-weight list of all fileservers and dbservers querying the Cell

startTime=time.mktime(time.localtime())
FileServerList=CS.getFsList(includeParts=True, db_cache=False)
DBServerList=CS.getDBList(FileServerList[0].servernames[0], db_cache=False)
endTime=time.mktime(time.localtime())

printServerList(FileServerList, DBServerList)
print "Time required to get information : %d secs" % (endTime-startTime)


# get a light-weight list of all fileservers and dbservers querying the Cell

startTime=time.mktime(time.localtime())
FileServerList=CS.getFsList(includeParts=True, db_cache=True)
DBServerList=CS.getDBList(FileServerList[0].servernames[0], db_cache=True)
endTime=time.mktime(time.localtime())

printServerList(FileServerList, DBServerList)
print "Time required to get information : %d secs" % (endTime-startTime)
