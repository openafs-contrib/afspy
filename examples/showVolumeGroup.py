#!/usr/bin/env python

import sys
sys.path.append("..")
from afs.util.AfsConfig import setupDefaultConfig

from afs.service.VolService import VolService
import afs

setupDefaultConfig()
afs.defaultConfig.CELL_NAME="ipp-garching.mpg.de"
volMng = VolService()
VolName="root.cell"
VolG=volMng.getVolGroup(VolName)
print "Volume Group: %s " %VolG

for v in VolG.RO :
    vol=volMng.getVolume(v["id"],v["serv"],v["part"])
    print "RO-Volume id=%s, server=%s,paritions=%s: %s " % (v["id"],v["serv"],v["part"], vol)

