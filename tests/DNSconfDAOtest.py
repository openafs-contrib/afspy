#!/usr/bin/env python

import unittest
import sys, os, argparse
from ConfigParser import ConfigParser

sys.path.append("..")

from afs.util.AfsConfig import parseDefaultConfig
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
    myParser=argparse.ArgumentParser(parents=[afs.argParser], add_help=False)
    myParser.add_argument("--setup", default="./Test.cfg", help="path to Testconfig")
    parseDefaultConfig(myParser)
    if not os.path.exists(options.setup) :
        sys.stderr.write("Test setup file %s does not exist.\n" % options.setup)
        sys.exit(2)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDNSconfDAO)
    unittest.TextTestRunner(verbosity=2).run(suite)
