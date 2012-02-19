#!/usr/bin/env python

import unittest
import sys, os
from ConfigParser import ConfigParser

sys.path.append("..")

from afs.util.AfsConfig import AfsConfig, setupDefaultConfig
from afs.util.options import define, options
from afs.dao import DNSconfDAO 
import afs

class TestDNSconfDAO(unittest.TestCase):
    """
    Tests DNSconfDAO Methods
    """
    
    def setUp(self):
        """
        setup
        """
        self.DAO = DNSconfDAO.DNSconfDAO()
        self.TestCfg=ConfigParser()
        self.TestCfg.read(options.setup)
        self.Cell=self.TestCfg.get("general", "Cell").lower()
        self.allDBServs=self.TestCfg.get("general","allDBServs").split(",")
        self.allDBServs.sort()
        return

    def test_getDBServList(self):
        DBServList=self.DAO.getDBServList(self.Cell)
        DBServList.sort()
        self.assertEqual(DBServList, self.allDBServs)
        return 
        
if __name__ == '__main__' :
    define("setup", default="./Test.cfg", help="path to Testconfig")
    setupDefaultConfig()
    if not os.path.exists(options.setup) :
        sys.stderr.write("Test setup file %s does not exist.\n" % options.setup)
        sys.exit(2)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDNSconfDAO)
    unittest.TextTestRunner(verbosity=2).run(suite)
