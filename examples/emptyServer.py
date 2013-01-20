#!/usr/bin/python


import cProfile
import time,logging
import argparse, string,datetime,sys
import afs
from afs.util.AfsConfig import parseDefaultConfig
from afs.service.OSDVolService import OSDVolService
from afs.service.OSDCellService import OSDCellService
from afs.service.OSDFsService import OSDFsService
from afs.service.DBsService import DBsService
from afs.service.ProjectService import ProjectService
from afs.model.Volume import Volume

myParser=argparse.ArgumentParser(parents=[afs.argParser], add_help=False)
myParser.add_argument("--src", default="", help="server[_part] to empty")
myParser.add_argument("--dst" ,default="", help="server[_part] to be filled")

parseDefaultConfig(myParser)

if afs.defaultConfig.src == ""  :
    print "source-server required."
    sys.exit(0)  

if afs.defaultConfig.dst == ""  :
    print "emptying by project not implemented yet."
    sys.exit(0)  


FS=OSDFsService()
VS=OSDVolService()


if "_" in afs.defaultConfig.src :
    try :
        srcSrv,srcPart=afs.defaultConfig.src.split("_")
    except :
        sys.stderr.write("cannot parse server_partition %s" % afs.defaultConfig.src)
        sys.exit(1)
else :
   srcSrv = afs.defaultConfig.src
   srcPart = ""
    
srcFS=FS.getFileServer(srcSrv)
if srcFS == None :
    sys.stderr.write("src Server %s does not exist." % srcFS)
    sys.exit(0)

if "_" in afs.defaultConfig.dst :
    try :
        dstSrv,dstPart=afs.defaultConfig.dst.split("_")
    except :
        sys.stderr.write("cannot parse server_partition %s" % afs.defaultConfig.dst)
        sys.exit(1)
else :
   dstSrv = afs.defaultConfig.dst
   dstPart = ""

if dstSrv == "" :
   sys.stderr.write("Moving by project is not implemented yet.")
   sys.exit(2)

dstFS=FS.getFileServer(afs.defaultConfig.dst)
if dstFS == None :
    sys.stderr.write("dst Server %s does not exist." % srcFS)
    sys.exit(0)


# get list of volumes to move
srcVolList=FS.getVolList(srcFS.servernames[0],srcPart,cached=False)
print srcVolList
