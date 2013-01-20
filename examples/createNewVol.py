#!/usr/bin/python

import string,datetime,sys,argparse
import afs
from afs.util.AfsConfig import parseDefaultConfig
from afs.util.DBManager import DBManager
from afs.service.OSDVolService import OSDVolService
from afs.service.OSDCellService import OSDCellService
from afs.service.OSDFsService import OSDFsService
from afs.service.DBsService import DBsService
from afs.service.ProjectService import ProjectService
from afs.model.Volume import Volume
from afs.model.Partition import Partition
from afs.model.ExtendedPartitionAttributes import ExtPartAttr
from afs.dao.UbikPeerDAO import UbikPeerDAO
from afs.dao.OSDVolumeDAO import OSDVolumeDAO


myParser=argparse.ArgumentParser(parents=[afs.argParser], add_help=False)
myParser.add_argument("--prj", dest="ProjectName", help="Name of Project")
myParser.add_argument("--volname", dest="VolumeName", required=True, help="Name of Volume")
myParser.add_argument("--voltype", dest="VolumeType", default="RW", help="Type of Volume")
myParser.add_argument("--force", action='store_true', dest="force", default=False, help="force creation, even if Volume does not fit in given project")

parseDefaultConfig(myParser)

PS=ProjectService()
# we get a list of Projects, sorted by the Nesting Level.
# only get the most specific one
PrjObj=PS.getProjectsByVolumeName(afs.defaultConfig.VolumeName)[0]

if afs.defaultConfig.ProjectName != None :
    thisPrjObj=PS.getProjectByName(afs.defaultConfig.ProjectName)
    if thisPrjObj == None :
        myParser.error("Project \"%s\" does not exist" % afs.defaultConfig.ProjectName)
    if thisPrjObj.id != PrjObj.id :
        if not afs.defaultConfig.force :
            myParser.error("VolumeName \"%s\" not matched by given Project \"%s\"\n" % (afs.defaultConfig.VolumeName,afs.defaultConfig.ProjectName))
            sys.exit(1)
        PrjObj = thisPrjObj

print (PS.getNewVolumeLocation(thisPrjObj.name,afs.defaultConfig.VolumeType))
