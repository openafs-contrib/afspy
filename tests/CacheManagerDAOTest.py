#!/usr/bin/env python

import unittest
import sys, os
from ConfigParser import ConfigParser

sys.path.append("..")

from afs.util.AfsConfig import AfsConfig, setupDefaultConfig
from afs.util.options import define, options
from afs.dao import CacheManagerDAO 
import afs

class TestCacheManagerDAOMethods(unittest.TestCase):
    """
    Tests CacheManagerDAO Methods
    """
    
    def setUp(self):
        """
        setup
        """
        self.DAO = CacheManagerDAO.CacheManagerDAO()
        self.TestCfg=ConfigParser()
        self.TestCfg.read(options.setup)
        self.Cell=self.TestCfg.get("general", "Cell").lower()
        self.User=self.TestCfg.get("general", "User")
        self.Pass=self.TestCfg.get("general", "Pass")
        return
    
    def test_getWSCell(self) :
        cellname=self.DAO.getWSCell()
        self.assertEqual(self.Cell, cellname)
        return
        
    def test_getCellAliases(self) :
        Aliases=self.DAO.getCellAliases()
        print Aliases
        return
    
if __name__ == '__main__' :
    define("setup", default="./Test.cfg", help="path to Testconfig")
    setupDefaultConfig()
    if not os.path.exists(options.setup) :
        sys.stderr.write("Test setup file %s does not exist.\n" % options.setup)
        sys.exit(2)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCacheManagerDAOMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
