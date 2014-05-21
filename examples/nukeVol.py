#!/usr/bin/python

import string,datetime,sys,argparse,os,stat
import afs
from afs.util.AfsConfig import parseDefaultConfig
from afs.util.afsutil import parseHumanWriteableSize
from afs.service.VolService import VolService
from afs.model.Volume import Volume
from afs.lla.VolumeLLA import VolumeLLA
from afs.lla.VLDbLLA import VLDbLLA
from afs.lla.FileSystemLLA import FileSystemLLA


myParser=argparse.ArgumentParser(parents=[afs.argParser], description="nuke a volume. Remove RW and all ROs", add_help=False)
myParser.add_argument("--volname", dest="VolumeName", required=True, help="Name of Volume")

parseDefaultConfig(myParser)
VD=VolumeLLA()
VS=VolService()

try :
    VolGroup=VS.getVolGroup(afs.defaultConfig.VolumeName)
except:
    print "Cannot get Volume group for %s. Are you sure it exists?" % afs.defaultConfig.VolumeName
    sys.exit(2)


print "Removing volume %s on following sites:" % afs.defaultConfig.VolumeName
print afs.defaultConfig.VolumeName,VolGroup["RW"][0].servername,VolGroup["RW"][0].part


for v in VolGroup["RO"] :
    print v.servername,v.part

sure=raw_input('Are you sure: [y/N] ?')

if not sure in ["y","Y"]:
    print "Aborted."
    sys.exit(1)
print "Removing RW from: ", VolGroup["RW"][0].servername,VolGroup["RW"][0].part
VD.remove(afs.defaultConfig.VolumeName,VolGroup["RW"][0].servername,VolGroup["RW"][0].part)

for v in VolGroup["RO"] :
    print "Removing RO from :", v.servername,v.part
    VD.remove(afs.defaultConfig.VolumeName+".readonly",v.servername,v.part)

