#!/usr/bin/env python

from ConfigParser import ConfigParser
import sys
import unittest

from afs.service.BosService import BosService
from afs.tests.BaseTest import parse_commandline
import afs

class EvaluateTestResults(unittest.TestCase) :
    
    def eval_get_bosserver(self, res) :
        self.assertEqual(self.general_restart_time, res.general_restart_time)
        self.assertEqual(self.newbinary_restart_time, res.newbinary_restart_time)
        self.assertEqual(self.server_name, res.servernames[0])
        return

class TestBosServiceMethods(EvaluateTestResults) :
    """
    Tests BosService Methods
    """
    
    @classmethod
    def setUp(self):
        """
        setup VolService
        """
        self.test_config = ConfigParser()
        self.test_config.read(afs.CONFIG.setup)
        self.service = BosService()
        self.server_name = self.test_config.get("BosService", "server")
        self.bos_server = self.service.get_bos_server(self.server_name, cached=False)
        self.BNodes = self.test_config.get("BosService", "BNodes").split(",")
        self.newbinary_restart_time = self.test_config.get("BosServerLLA","newbinary_restart_time")
        self.general_restart_time = self.test_config.get("BosServerLLA","general_restart_time")
        return    

    def test_get_bosserver(self) :
        self.eval_get_bosserver(self.bos_server)
        return 

class TestBosServiceMethods_cached(EvaluateTestResults) :
    """
    Tests BosService Methods
    """

    @classmethod
    def setUp(self):
        self.test_config = ConfigParser()
        self.test_config.read(afs.CONFIG.setup)
        self.service = BosService()
        self.server_name = self.test_config.get("BosService", "server")
        self.bos_server = self.service.get_bos_server(self.server_name, cached=True)
        self.BNodes = self.test_config.get("BosService", "BNodes").split(",")
        self.newbinary_restart_time = self.test_config.get("BosServerLLA","newbinary_restart_time")
        self.general_restart_time = self.test_config.get("BosServerLLA","general_restart_time")
        return    

    def test_get_bosserver(self) :
        self.eval_get_bosserver(self.bos_server)
        return 

if __name__ == '__main__' :
    parse_commandline()
    sys.stderr.write("Testing live methods to fill DB_CACHE\n")
    sys.stderr.write("==============================\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBosServiceMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
    sys.stderr.write("Testing  methods accessing DB_CACHE\n")
    sys.stderr.write("================================\n")
    if afs.CONFIG.DB_CACHE :
        suite = unittest.TestLoader().loadTestsFromTestCase(TestBosServiceMethods_cached)
        unittest.TextTestRunner(verbosity=2).run(suite)
    else :
         sys.stderr.write("Skipped,  because DB_CACHE is disabled.\n")
