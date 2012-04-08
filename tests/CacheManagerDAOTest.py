#!/usr/bin/env python

import unittest
import sys
from BaseTest import parseCMDLine, basicTestSetup

sys.path.append("..")
from afs.dao import CacheManagerDAO 

class TestCacheManagerDAOMethods(unittest.TestCase, basicTestSetup):
    """
    Tests CacheManagerDAO Methods
    """
    
    def setUp(self):
        """
        setup
        """
        basicTestSetup.setUp(self)
        self.DAO = CacheManagerDAO.CacheManagerDAO()
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
    parseCMDLine()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCacheManagerDAOMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
