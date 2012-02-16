#!/usr/bin/env python

import unittest
import sys, os
from ConfigParser import ConfigParser

sys.path.append("..")

from afs.util.AfsConfig import AfsConfig, setupDefaultConfig
from afs.util.options import define, options
from afs.service import CellService
import afs

class TestCellServiceMethods(unittest.TestCase):
    """
    Tests VolService Methods
    """
    
    def setUp(self):
        """
        setup
        """
        self.CellService = CellService.CellService()
        self.TestCfg=ConfigParser()
        self.TestCfg.read(options.setup)
        self.numFSs=int(self.TestCfg.get("CellService", "numFSs"))
        self.allDBs=self.TestCfg.get("CellService", "allDBs").split(",")
        self.allDBs.sort()
        self.FS=self.TestCfg.get("CellService", "FS")
	self.FsUUID=self.TestCfg.get("CellService", "FsUUID")
        return
    
    def test_getDBList_live(self) :
        DBList=self.CellService.getDBList(self.FS, db_cache=False)
        DB_IPs=[]
        for db in DBList :
            DB_IPs.append(db.ipaddrs[0])
        DB_IPs.sort()
        self.assertEqual(self.allDBs, DB_IPs)
        return

    def test_getDBList_cached(self) :
        DBList=self.CellService.getDBList(self.FS, db_cache=True)
        DB_IPs=[]
        for db in DBList :
            DB_IPs.append(db.ipaddrs[0])
        DB_IPs.sort()
        self.assertEqual(self.allDBs, DB_IPs)
        return
        
    def test_getFSList_live(self) :
        FSList=self.CellService.getFsList(self.FS, db_cache=False)
        self.assertEqual(self.numFSs, len(FSList))
        return

    def test_getFSList_cached(self) :
        FSList=self.CellService.getFsList(self.FS, db_cache=True)
        self.assertEqual(self.numFSs, len(FSList))
        return
        
    def test_getFsUUID_live(self) :
        uuid=self.CellService.getFsUUID(self.FS, db_cache=False)
        self.assertEqual(self.FsUUID, uuid)
        return

    def test_getFsUUID_cached(self) :
        uuid=self.CellService.getFsUUID(self.FS, db_cache=True)
        self.assertEqual(self.FsUUID, uuid)
        return

    
    
    
if __name__ == '__main__' :
    define("setup", default="./Test.cfg", help="path to Testconfig")
    setupDefaultConfig()
    if not os.path.exists(options.setup) :
        sys.stderr.write("Test setup file %s does not exist.\n" % options.setup)
        sys.exit(2)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCellServiceMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
