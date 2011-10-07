#!/usr/bin/env python

import sys, os
sys.path.append("..")
from afs.util.AfsConfig import AfsConfig, setupDefaultConfig
from afs.util.options import define, options
from afs.service.VolService import VolService
import afs

setupDefaultConfig()
afs.defaultConfig.AFSCell="desy.de"
volMng = VolService()
VolName="root.cell"
VolG=volMng.getVolGroup(VolName)
print VolG
for v in VolG["RO"] :
    vol = volMng.getVolume('root.cell',v["serv"],v["part"])
    print vol
