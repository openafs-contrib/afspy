#!/usr/bin/env python

import unittest
import sys
from afs.tests.BaseTest import parse_commandline, BasicTestSetup

import afs

from afs.service import CellService

class SetupTest(BasicTestSetup) :
    """
    setup TestFs config
    """
    
    def setUp(self):
        """
        setup
        """
        self.CellService = CellService.CellService()
        BasicTestSetup.__init__(self, self.CellService, ignore_classes=[afs.service.BaseService.BaseService])
        self.numFSs=int(self.test_config.get("CellService", "numFSs"))
        self.allDBIPs=self.test_config.get("CellService", "allDBIPs").split(",")
        self.allDBIPs.sort()
        self.allDBHostnames=self.test_config.get("CellService", "allDBHostnames").split(",")
        self.allDBHostnames.sort()
        self.minUbikDBVersion=self.test_config.get("CellService", "minUbikDBVersion")
        self.FS=self.test_config.get("CellService", "FS")
        self.FsUUID=self.test_config.get("CellService", "FsUUID")
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
        self.CellInfo = self.CellService.get_cell_info(cached=False)
        return
    
    def test_Cellinfo_DBList_live(self) :
        DBList=self.CellInfo.db_servers
        DBList.sort()
        self.assertEqual(self.allDBHostnames, DBList)
        return

    def test_getFSServers_live(self) :
        FSList=self.CellInfo.file_servers
        self.assertEqual(self.numFSs, len(FSList))
        return

    def test_PTDBVersion_live(self):
        DBVersion = self.CellInfo.ptdb_version
        self.assertTrue((DBVersion>self.minUbikDBVersion))
        return

    def test_PTDBSyncSite_live(self):
        DBSyncSite=self.CellInfo.ptdb_sync_site
        self.assertTrue((DBSyncSite in self.allDBIPs))
        return
        
    def test_VLDBVersion_live(self):
        DBVersion=self.CellInfo.vldb_version
        self.assertTrue((DBVersion>self.minUbikDBVersion))
        return

    def test_VLDBSyncSite_live(self):
        DBSyncSite=self.CellInfo.vldb_sync_site
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
        self.CellInfo = self.CellService.get_cell_info(cached=True)
        return

    def test_getDBList_cached(self) :
        DBList=self.CellInfo.db_servers
        DBList.sort()
        self.assertEqual(self.allDBHostnames, DBList)
        return


    def test_getFSServers_cached(self) :
        FSList=self.CellInfo.file_servers
        self.assertEqual(self.numFSs, len(FSList))
        return
        
    def test_PTDBVersion_cached(self):
        DBVersion=self.CellInfo.ptdb_version
        self.assertTrue((DBVersion>self.minUbikDBVersion))
        return


    def test_PTDBSyncSite_cached(self):
        DBSyncSite=self.CellInfo.ptdb_sync_site
        self.assertTrue((DBSyncSite in self.allDBIPs))
        return

    def test_VLDBVersion_cached(self):
        DBVersion=self.CellInfo.vldb_version
        self.assertTrue((DBVersion>self.minUbikDBVersion))
        return

    def test_VLDBSyncSite_cached(self):
        DBSyncSite=self.CellInfo.vldb_sync_site
        self.assertTrue((DBSyncSite in self.allDBIPs))
        return        


if __name__ == '__main__' :
    parse_commandline()
    
    sys.stderr.write("Testing live methods to fill DB_CACHE\n")
    sys.stderr.write("==============================\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCellServiceSetMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
    sys.stderr.write("Testing  methods accessing DB_CACHE\n")
    sys.stderr.write("================================\n")
    if afs.CONFIG.DB_CACHE :
        suite = unittest.TestLoader().loadTestsFromTestCase(TestCellServiceCachedMethods)
        unittest.TextTestRunner(verbosity=2).run(suite)
    else :
         sys.stderr.write("Skipped,  because DB_CACHE is disabled.\n")
