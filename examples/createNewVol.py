#!/usr/bin/python

import string,datetime,sys,argparse,os,stat
import afs
from afs.util.AfsConfig import parseDefaultConfig
from afs.util.afsutil import parseHumanWriteableSize
from afs.service.ProjectService import ProjectService
from afs.model.Volume import Volume
from afs.lla.VolumeLLA import VolumeLLA
from afs.lla.VLDbLLA import VLDbLLA
from afs.lla.FileSystemLLA import FileSystemLLA


myParser=argparse.ArgumentParser(parents=[afs.argParser], add_help=False)
myParser.add_argument("--volname", dest="VolumeName", required=True, help="Name of Volume")
myParser.add_argument("--voltype", dest="VolumeType", default="RW", help="Type of Volume")
myParser.add_argument("--size", dest="VolumeSize", default="5000", help="Size of Volume in KB")
myParser.add_argument("--mpt", dest="Mountpoint", help="Mountpoint for the new volume.")
myParser.add_argument("--mpttype", dest="MountpointType", default="RW", choices=['RW', 'RO'], help="Type of mountpoint: RW or RO. Defaults to RW.")
myParser.add_argument("--aclpath", dest="ACLOrigin", help="path in AFS to copy ACLs from.")
myParser.add_argument("--prj", dest="ProjectName", help="Name of Project")
myParser.add_argument("--force", action='store_true', dest="force", default=False, help="force creation, even if Volume does not fit in given project")

parseDefaultConfig(myParser)
VD=VolumeLLA()
VlD=VLDbLLA()
FsD=FileSystemLLA()

VolumeType = afs.defaultConfig.VolumeType
if afs.defaultConfig.VolumeName[-9:] == ".readonly"  :
    VolumeName = afs.defaultConfig.VolumeName[:-9]
    VolumeType = "RO"
else :
    VolumeName = afs.defaultConfig.VolumeName

VolSize=parseHumanWriteableSize(afs.defaultConfig.VolumeSize)/1024
PS=ProjectService()
# we get a list of Projects, sorted by the Nesting Level.
# only get the most specific one

PrjObj=PS.getProjectsByVolumeName(VolumeName)[0]
if afs.defaultConfig.ProjectName != None :
    thisPrjObj=PS.getProjectByName(afs.defaultConfig.ProjectName)
    if thisPrjObj == None :
        myParser.error("Project \"%s\" does not exist" % afs.defaultConfig.ProjectName)
    if thisPrjObj.id != PrjObj.id :
        if not afs.defaultConfig.force :
            myParser.error("VolumeName \"%s\" not matched by given Project \"%s\"\n" % (VolumeName,afs.defaultConfig.ProjectName))
            sys.exit(1)
        PrjObj = thisPrjObj
    
if not PrjObj :
    sys.stderr.write("Cannot guess Project for volume %s" % VolumeName)
VolObj=Volume()
VolObj.name=VolumeName
VolObj.type=VolumeType
if VolObj.type == "RW" :
    RWServ,RWPart=(PS.getNewVolumeLocation(PrjObj.name,VolObj))
    print "Creating new volume %s of type %s on %s %s with size %d" % (VolObj.name, VolObj.type, RWServ,RWPart,VolSize)
    VD.create(VolObj.name,RWServ,RWPart,VolSize)
    print "Creating accompanying RO"
    VlD.addsite(VolObj.name,RWServ,RWPart)
    # XXX it's a bit shitty, but we have to release after each addsite for now, since we get the locations from vos examine atm and not from vos listvldb
    VD.release(VolObj.name)
    for i in range(1,PrjObj.minnum_ro) :
        print "Creating additional RO-copy number %s" % i
        ROServ,ROPart=(PS.getNewVolumeLocation(PrjObj.name,VolObj))
        VlD.addsite(VolObj.name,ROServ,ROPart)
        VD.release(VolObj.name)
elif VolObj.type == "RO" :
    ROServ,ROPart=(PS.getNewVolumeLocation(PrjObj.name,VolObj))
    print "Creating new volume %s of type %s on %s %s" % (VolObj.name, VolObj.type, ROServ,ROPart)
    VlD.addsite(VolObj.name,ROServ,ROPart)
    VD.release(VolObj.name)
else :
    print "Only volumes tpye sRW and RO are supported."
    sys.exit(1)
  

if afs.defaultConfig.Mountpoint != None :
    print "Creating mountpoint %s of type %s" % (afs.defaultConfig.Mountpoint,afs.defaultConfig.MountpointType)
    if afs.defaultConfig.MountpointType == "RW" :
        FsD.makeMountpoint(afs.defaultConfig.Mountpoint,VolObj.name,toRW=True)
    else :
        FsD.makeMountpoint(afs.defaultConfig.Mountpoint,VolObj.name,toRW=False)
        
    if afs.defaultConfig.ACLOrigin != None :
        print "Copying ACLs from %s to new Mountpoint %s" % (afs.defaultConfig.ACLOrigin,afs.defaultConfig.Mountpoint)  
        FsD.copyACL(afs.defaultConfig.ACLOrigin,afs.defaultConfig.Mountpoint)
  
    print "Setting Unix-permissions of mountpoint to 755"
    os.chmod(afs.defaultConfig.Mountpoint,stat.S_IWUSR | stat.S_IRUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)


