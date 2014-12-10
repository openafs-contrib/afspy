#!/usr/bin/env python

import sys
import unittest
from ConfigParser import ConfigParser
from afs.tests.BaseTest import parse_commandline

import afs

from afs.service import CellService

class TestCellServiceSetMethods(unittest.TestCase):
    """
    Tests CellService Methods
    """
    
    @classmethod
    def setUpClass(self):
        """
        setup CellService
        """
        self.CellService = CellService.CellService()
        self.test_config = ConfigParser()
        self.test_config.read(afs.CONFIG.setup)
        self.numFSs = int(self.test_config.get("CellService", "numFSs"))
        self.allDBIPs = self.test_config.get("CellService", "allDBIPs").split(",")
        self.allDBIPs.sort()
        if "," in self.test_config.get("CellService", "realDBHostnames") :
            self.realDBHostnames = self.test_config.get("CellService", "realDBHostnames").split(",")
            self.realDBHostnames.sort()
        else :
            self.realDBHostnames = [self.test_config.get("CellService", "realDBHostnames")]
        if "," in self.test_config.get("CellService", "cloneDBHostnames") :
            self.cloneDBHostnames = self.test_config.get("CellService", "cloneDBHostnames").split(",")
            self.cloneDBHostnames.sort()
        else :
            self.cloneDBHostnames = [self.test_config.get("CellService","cloneDBHostnames")]
        self.minUbikDBVersion = self.test_config.get("CellService", "minUbikDBVersion")
        self.FS = self.test_config.get("CellService", "FS")
        self.FsUUID = self.test_config.get("CellService", "FsUUID")
        self.CellInfo = self.CellService.get_cell_info(cached=False)
        return
    
    def test_Cellinfo_DBList_live(self) :
        DBList=[]
        CloneList=[]
        for s in self.CellInfo.db_servers :
            if s["isClone"] :
                CloneList.append(s["hostname"])
            else :
                DBList.append(s["hostname"])
        DBList.sort()
        CloneList.sort()
        self.assertEqual(self.realDBHostnames, DBList)
        self.assertEqual(self.cloneDBHostnames, CloneList)
        return

    def test_getFSServers_live(self) :
        FSList=self.CellInfo.file_servers
        self.assertEqual(self.numFSs, len(FSList))
        return

    def test_PTDBVersion_live(self):
        DBVersion = self.CellInfo.ptdb_version
        self.assertTrue((DBVersion > self.minUbikDBVersion))
        return

    def test_PTDBSyncSite_live(self):
        DBSyncSite=self.CellInfo.ptdb_sync_site
        self.assertTrue((DBSyncSite in self.allDBIPs))
        return
        
    def test_VLDBVersion_live(self):
        DBVersion = self.CellInfo.vldb_version
        self.assertTrue((DBVersion > self.minUbikDBVersion))
        return

    def test_VLDBSyncSite_live(self):
        DBSyncSite = self.CellInfo.vldb_sync_site
        self.assertTrue((DBSyncSite in self.allDBIPs))
        return

class TestCellServiceCachedMethods(unittest.TestCase):
    """
    Tests CellService Methods using DB_CACHE
    """

    @classmethod
    def setUpClass(self):
        """
        setup CellService
        """
        self.CellService = CellService.CellService()
        self.test_config = ConfigParser()
        self.test_config.read(afs.CONFIG.setup)
        self.num_fileserver = int(self.test_config.get("CellService", "num_fileserver"))
        self.all_db_ips = self.test_config.get("CellService", "all_db_ips").split(",")
        self.all_db_ips.sort()
        if "," in self.test_config.get("CellService", "realDBHostnames") :
            self.real_db_hostnames = self.test_config.get("CellService", "real_db_hostnames").split(",")
            self.real_db_hostnames.sort()
        else :
            self.realDBHostnames = [self.test_config.get("CellService", "realDBHostnames")]
        if "," in self.test_config.get("CellService", "clone_db_hostnames") :
            self.clone_db_hostnames = self.test_config.get("CellService", "clone_db_hostnames").split(",")
            self.clone_db_hostnames.sort()
        else :
            self.cloneDBHostnames = [self.test_config.get("CellService","cloneDBHostnames")]
        self.min_ubik_db_version = self.test_config.get("CellService", "min_ubik_db_version")
        self.fileserver = self.test_config.get("CellService", "FS")
        self.fileserver_uuid = self.test_config.get("CellService", "FsUUID")
        self.cell_info = self.CellService.get_cell_info(cached=True)
        return

    @classmethod
    def tearDownClass(self) :
        """
        remove history from DB
        """
        sys.stderr.write("removing historic classes")
        self.CellService.DBManager.vaccuum_cache()
        return
         
    def test_getDBList_cached(self) :
        DBList=[]
        CloneList=[]
        for s in self.CellInfo.db_servers :
            if s["isClone"] :
                CloneList.append(s["hostname"])
            else :
                DBList.append(s["hostname"])
        DBList.sort()
        CloneList.sort()
        self.assertEqual(self.realDBHostnames, DBList)
        self.assertEqual(self.cloneDBHostnames, CloneList)
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
