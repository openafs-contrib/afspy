#!/usr/bin/env python

import unittest
import sys
from BaseTest import parseCMDLine, basicTestSetup

import afs

from afs.service import CellService

class SetupTest(basicTestSetup) :
    """
    setup TestFs config
    """
    
    def setUp(self):
        """
        setup
        """
        basicTestSetup.setUp(self)
        self.CellService = CellService.CellService()
        self.numFSs=int(self.TestCfg.get("CellService", "numFSs"))
        self.allDBIPs=self.TestCfg.get("CellService", "allDBIPs").split(",")
        self.allDBIPs.sort()
        self.allDBHostnames=self.TestCfg.get("CellService", "allDBHostnames").split(",")
        self.allDBHostnames.sort()
        self.FS=self.TestCfg.get("CellService", "FS")
        self.FsUUID=self.TestCfg.get("CellService", "FsUUID")
        return

class TestCellServiceSetMethods(unittest.TestCase, SetupTest):
    """
    Tests CellService Methods
    """
    
    def setUp(self):
        """
        setup CellService
        """
        SetupTest.setUp(self)
        self.CellInfo = self.CellService.getCellInfo(cached=False)
        return
    
    def test_Cellinfo_DBList_live(self) :
        DBList=self.CellInfo.DBServers
        DBList.sort()
        self.assertEqual(self.allDBHostnames, DBList)
        return

    def test_getFSServers_live(self) :
        FSList=self.CellInfo.FileServers
        self.assertEqual(self.numFSs, len(FSList))
        return

    def test_PTDBVersion_live(self):
        DBVersion = self.CellInfo.PTDBVersion
        self.assertTrue((DBVersion>self.minUbikDBVersion))
        return

    def test_PTDBSyncSite_live(self):
        DBSyncSite=self.CellInfo.PTDBSyncSite
        self.assertTrue((DBSyncSite in self.allDBIPs))
        return
        
    def test_VLDBVersion_live(self):
        DBVersion=self.CellInfo.VLDBVersion
        self.assertTrue((DBVersion>self.minUbikDBVersion))
        return

    def test_VLDBSyncSite_live(self):
        DBSyncSite=self.CellInfo.VLDBSyncSite
        self.assertTrue((DBSyncSite in self.allDBIPs))
        return

class TestCellServiceCachedMethods(unittest.TestCase, SetupTest):
    """
    Tests CellService Methods using DB_CACHE
    """
    def setUp(self):
        """
        setup CellService
        """
        SetupTest.setUp(self)
        self.CellInfo = self.CellService.getCellInfo(cached=True)
        return

    def test_getDBList_cached(self) :
        DBList=self.CellInfo.DBServers
        DBList.sort()
        self.assertEqual(self.allDBHostnames, DBList)
        return


    def test_getFSServers_cached(self) :
        FSList=self.CellInfo.FileServers
        self.assertEqual(self.numFSs, len(FSList))
        return
        
    def test_PTDBVersion_cached(self):
        DBVersion=self.CellInfo.PTDBVersion
        self.assertTrue((DBVersion>self.minUbikDBVersion))
        return


    def test_PTDBSyncSite_cached(self):
        DBSyncSite=self.CellInfo.PTDBSyncSite
        self.assertTrue((DBSyncSite in self.allDBIPs))
        return

    def test_VLDBVersion_cached(self):
        DBVersion=self.CellInfo.VLDBVersion
        self.assertTrue((DBVersion>self.minUbikDBVersion))
        return

    def test_VLDBSyncSite_cached(self):
        DBSyncSite=self.CellInfo.VLDBSyncSite
        self.assertTrue((DBSyncSite in self.allDBIPs))
        return        


if __name__ == '__main__' :
    parseCMDLine()
    
    sys.stderr.write("Testing live methods to fill DB_CACHE\n")
    sys.stderr.write("==============================\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCellServiceSetMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
    sys.stderr.write("Testing  methods accessing DB_CACHE\n")
    sys.stderr.write("================================\n")
    if afs.defaultConfig.DB_CACHE :
        suite = unittest.TestLoader().loadTestsFromTestCase(TestCellServiceCachedMethods)
        unittest.TextTestRunner(verbosity=2).run(suite)
    else :
         sys.stderr.write("Skipped,  because DB_CACHE is disabled.\n")
