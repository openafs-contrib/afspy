#!/usr/bin/env python

import unittest
from BaseTest import parseCMDLine, basicTestSetup

from afs.dao import CacheManagerDAO 
import afs

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
        cellname=self.DAO.getWSCell( _cfg=afs.CONFIG,_user="test")
        self.assertEqual(self.Cell,cellname)
        return
        
    def test_getCellAliases(self) :
        Aliases=self.DAO.getCellAliases(_cfg=afs.CONFIG,_user="test")
        print Aliases
        return
    
if __name__ == '__main__' :
    parseCMDLine()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCacheManagerDAOMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
