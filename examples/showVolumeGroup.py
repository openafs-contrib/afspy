#!/usr/bin/env python
import argparse
from afs.util.AfsConfig import parseDefaultConfig
from afs.service.VolService import VolService
from afs.service.OSDVolService import OSDVolService
import afs


# setup Config
myParser=argparse.ArgumentParser(parents=[afs.argParser], add_help=False)
parseDefaultConfig(myParser)

afs.defaultConfig.CELL_NAME="ipp-garching.mpg.de"

# XXX we should have some util-function to check if we use OSD-bianries or not !?
volMng = OSDVolService()
VolName="root.cell"
VolG=volMng.getVolGroup(VolName)
print "Volume Group: %s " %VolG

for v in VolG.RO :
    vol=volMng.getVolume(v["id"],v["serv"],v["part"])
    print "RO-Volume id=%s, server=%s,paritions=%s: %s " % (v["id"],v["serv"],v["part"], vol)

