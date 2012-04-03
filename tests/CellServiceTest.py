#!/usr/bin/env python

global CellInfo_live, CellInfo_cached
CellInfo_live=None
CellInfo_cached=None

import unittest
import sys, os
from ConfigParser import ConfigParser

sys.path.append("..")

from afs.util.AfsConfig import  setupDefaultConfig
from afs.util.options import define, options
from afs.service import CellService

class TestCellServiceMethods(unittest.TestCase):
    """
    Tests CellService Methods
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
        self.minUbikDBVersion=self.TestCfg.get("general","minUbikDBVersion")
        self.allDBs.sort()
        self.FS=self.TestCfg.get("CellService", "FS")
        self.FsUUID=self.TestCfg.get("CellService", "FsUUID")
        return
    
    def test_Cellinfo_DBList_live(self) :
        DBList=CellInfo_live.DBServers
        DB_IPs=[]
        for db in DBList :
            DB_IPs.append(db['ipaddrs'][0])
        DB_IPs.sort()
        self.assertEqual(self.allDBs, DB_IPs)
        return

    def test_getDBList_cached(self) :
        DBList=CellInfo_cached.DBServers
        DB_IPs=[]
        for db in DBList :
            DB_IPs.append(db['ipaddrs'][0])
        DB_IPs.sort()
        self.assertEqual(self.allDBs, DB_IPs)
        return
        
    def test_getFSServers_live(self) :
        FSList=CellInfo_live.FileServers
        self.assertEqual(self.numFSs, len(FSList))
        return

    def test_getFSServers_cached(self) :
        FSList=CellInfo_cached.FileServers
        self.assertEqual(self.numFSs, len(FSList))
        return
        
    def test_getFsUUID_live(self) :
        uuid=self.CellService.getFsUUID(self.FS, cached=False)
        self.assertEqual(self.FsUUID, uuid)
        return

    def test_getFsUUID_cached(self) :
        uuid=self.CellService.getFsUUID(self.FS,cached=True)
        self.assertEqual(self.FsUUID, uuid)
        return
        
    def test_PTDBVersion_cached(self):
        DBVersion=CellInfo_cached.PTDBVersion
        self.assertTrue((DBVersion>self.minUbikDBVersion))
        return
        
    def test_PTDBVersion_live(self):
        DBVersion = CellInfo_live.PTDBVersion
        self.assertTrue((DBVersion>self.minUbikDBVersion))
        return

    def test_PTDBSyncSite_cached(self):
        DBSyncSite=CellInfo_cached.PTDBSyncSite
        self.assertTrue((DBSyncSite in self.allDBs))
        return
        
    def test_PTDBSyncSite_live(self):
        DBSyncSite=CellInfo_live.PTDBSyncSite
        self.assertTrue((DBSyncSite in self.allDBs))
        return

    def test_VLDBVersion_cached(self):
        DBVersion=CellInfo_cached.VLDBVersion
        self.assertTrue((DBVersion>self.minUbikDBVersion))
        return
        
    def test_VLDBVersion_live(self):
        DBVersion=CellInfo_live.VLDBVersion
        self.assertTrue((DBVersion>self.minUbikDBVersion))
        return

    def test_VLDBSyncSite_cached(self):
        DBSyncSite=CellInfo_cached.VLDBSyncSite
        self.assertTrue((DBSyncSite in self.allDBs))
        return
        
    def test_VLDBSyncSite_live(self):
        DBSyncSite=CellInfo_live.VLDBSyncSite
        self.assertTrue((DBSyncSite in self.allDBs))
        return

if __name__ == '__main__' :
    define("setup", default="./Test.cfg", help="path to Testconfig")
    setupDefaultConfig()
    if not os.path.exists(options.setup) :
        sys.stderr.write("Test setup file %s does not exist.\n" % options.setup)
        sys.exit(2)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCellServiceMethods)
    CS=CellService.CellService()
    CellInfo_live=CS.getCellInfo(cached=False)
    CellInfo_cached=CS.getCellInfo(cached=True)
    unittest.TextTestRunner(verbosity=2).run(suite)
