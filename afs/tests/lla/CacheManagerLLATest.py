#!/usr/bin/env python

import unittest
from afs.tests.BaseTest import parse_commandline, BasicTestSetup

from afs.lla import CacheManagerLLA 
import afs.model.CacheManager
import afs

class TestCacheManagerLLAMethods(unittest.TestCase, BasicTestSetup):
    """
    Tests CacheManager Methods
    """
    
    def setUp(self):
        """
        setup
        """
        self.lla = CacheManagerLLA.CacheManagerLLA()
        BasicTestSetup.__init__(self, self.lla, ignore_classes = \
            [afs.lla.BaseLLA.BaseLLA])
        self.cell_aliases = {}
        for kv in self.test_config.get("CacheManagerLLA","Aliases").split(",") :
            k,v = kv.split("=") 
            self.cell_aliases[k] = v
        self.cache_manager = afs.model.CacheManager.CacheManager()
        return
    
    def test_get_ws_cell(self) :
        obj = self.lla.get_ws_cell( self.cache_manager)
        self.assertEqual(self.afs_cell,obj.ws_cell)
        return
        
    def test_get_cell_aliases(self) :
        obj = self.lla.get_cell_aliases(self.cache_manager)
        self.assertEqual(self.cell_aliases, obj.cell_aliases)
        return
    
if __name__ == '__main__' :
    parse_commandline()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCacheManagerLLAMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
