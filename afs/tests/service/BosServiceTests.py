#!/usr/bin/env python

import unittest, sys
from afs.tests.BaseTest import parse_commandline, BasicTestSetup

from afs.service.BosService import BosService
import afs

class SetupTest(BasicTestSetup) :
    """
    setup TestBs config
    """
    
    def setUp(self):
        """
        setup VolService
        """
        self.service = BosService()
        BasicTestSetup.__init__(self, self.service, ignore_classes=[afs.service.BaseService.BaseService])
        self.server_name=self.test_config.get("BosService", "server")
        self.BNodes=self.test_config.get("BosService", "BNodes").split(",")
        self.newbinary_restart_time = self.test_config.get("BosServerDAO","newbinary_restart_time")
        self.general_restart_time = self.test_config.get("BosServerDAO","general_restart_time")
        return    


class TestBosServiceSetMethods(unittest.TestCase, SetupTest):
    """
    Tests BosService Methods
    """
    
    def setUp(self):
        """
        setup BosService
        """
        SetupTest.setUp(self)
        return

    def test_push_bos_server(self):
        """
        push bos-server config to AFS-cell
        """
        return

    def test_pull_bos_server(self):
        """
        pull bos-server config to AFS-cell
        """
        obj = self.service.pull_bos_server(self.server_name, cached=False)
        self.assertEqual(self.general_restart_time, obj.general_restart_time)
        self.assertEqual(self.newbinary_restart_time, obj.newbinary_restart_time)
        return
        
class TestBosServiceCachedMethods(unittest.TestCase, SetupTest):
    """
    Tests BosService Methods
    """
    
    def setUp(self):
        """
        setup token and BosService
        """
        SetupTest.setUp(self)
        return

    def test_pull_bos_server(self) :
        """
        pull bos-server config to AFS-cell
        """
        obj = self.service.pull_bos_server(self.server_name, cached = True)
        return

    def test_push_bos_server(self):
        """
        push bos-server config to AFS-cell
        """
        return
        


if __name__ == '__main__' :
    parse_commandline()
    sys.stderr.write("Testing live methods to fill DB_CACHE\n")
    sys.stderr.write("==============================\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBosServiceSetMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
    sys.stderr.write("Testing  methods accessing DB_CACHE\n")
    sys.stderr.write("================================\n")
    if afs.CONFIG.DB_CACHE :
        suite = unittest.TestLoader().loadTestsFromTestCase(TestBosServiceCachedMethods)
        unittest.TextTestRunner(verbosity=2).run(suite)
    else :
         sys.stderr.write("Skipped,  because DB_CACHE is disabled.\n")
