#!/usr/bin/env python

import unittest
import sys, os
from ConfigParser import ConfigParser

sys.path.append("..")

from afs.util.AfsConfig import AfsConfig, setupDefaultConfig
from afs.util.options import define, options
from afs.dao import UbikPeerDAO 
import afs

class TestUbikDAOMethods(unittest.TestCase):
    """
    Tests UbikPeerDAO Methods
    """
    
    def setUp(self):
        """
        setup
        """
        self.DAO = UbikPeerDAO.UbikPeerDAO()
        self.TestCfg=ConfigParser()
        self.TestCfg.read(options.setup)
        self.Cell=self.TestCfg.get("general", "Cell").lower()
        self.User=self.TestCfg.get("general", "User")
        self.Pass=self.TestCfg.get("general", "Pass")
        self.DB=self.TestCfg.get("UbikDAO","DB")
        self.DBPort=self.TestCfg.get("UbikDAO","DBPort")
        self.allHosts=self.TestCfg.get("UbikDAO","allDBs").split(",")
        return
    
    def test_getSyncSite(self) :
        SyncSite=self.DAO.getSyncSite(self.DB, self.DBPort)
        self.assertTrue( (SyncSite in self.allHosts), msg="SyncSite '%s' not in allDBs : %s" % (SyncSite, self.allHosts))
        return
    
    def test_getDBVersion(self) :
        DBVersion=self.DAO.getDBVersion(self.DB, self.DBPort)
        self.assertTrue((DBVersion>1327495778))
    
if __name__ == '__main__' :
    define("setup", default="./Test.cfg", help="path to Testconfig")
    setupDefaultConfig()
    if not os.path.exists(options.setup) :
        sys.stderr.write("Test setup file %s does not exist.\n" % options.setup)
        sys.exit(2)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUbikDAOMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
