#!/usr/local/bin/python

import argparse,time,sys
import afs
from afs.util.AfsConfig import parseDefaultConfig
from afs.service.OSDCellService import OSDCellService

updateInterval=5*60 # Every 5 mins.

myParser=argparse.ArgumentParser(parents=[afs.argParser], add_help=False)
parseDefaultConfig(myParser)
CS=OSDCellService()

while 1 :
    CS.getCellInfo(cached=False)
    time.sleep(updateInterval)
