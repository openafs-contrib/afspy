#!/usr/bin/env python

import unittest
from afs.tests.BaseTest import parse_commandline, BasicTestSetup

from afs.dao import CacheManagerDAO 
import afs.model.CacheManager
import afs

class TestCacheManagerDAOMethods(unittest.TestCase, BasicTestSetup):
    """
    Tests CacheManager Methods
    """
    
    def setUp(self):
        """
        setup
        """
        self.dao = CacheManagerDAO.CacheManagerDAO()
        BasicTestSetup.__init__(self, self.dao, ignore_classes = \
            [afs.dao.BaseDAO.BaseDAO])
        self.cell_aliases = {}
        for kv in self.test_config.get("CacheManagerDAO","Aliases").split(",") :
            k,v = kv.split("=") 
            self.cell_aliases[k] = v
        self.cache_manager = afs.model.CacheManager.CacheManager()
        return
    
    def test_get_ws_cell(self) :
        obj = self.dao.get_ws_cell( self.cache_manager)
        self.assertEqual(self.afs_cell,obj.ws_cell)
        return
        
    def test_get_cell_aliases(self) :
        obj = self.dao.get_cell_aliases(self.cache_manager)
        self.assertEqual(self.cell_aliases, obj.cell_aliases)
        return
    
if __name__ == '__main__' :
    parse_commandline()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCacheManagerDAOMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
