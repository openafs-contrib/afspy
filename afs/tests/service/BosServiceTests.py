#!/usr/bin/env python

from ConfigParser import ConfigParser
import sys
import time
import unittest

from afs.service.BosService import BosService
from afs.tests.BaseTest import parse_commandline
import afs

class EvaluateTestResults(unittest.TestCase) :
    
    def eval_get_bosserver(self, res) :
        self.assertEqual(self.bos_server.restart_times["general"], res.restart_times["general"])
        self.assertEqual(self.bos_server.restart_times["newbinary"], res.restart_times["newbinary"])
        self.assertEqual(self.server_name, res.servernames[0])
        for bnode in self.bos_server.bnodes :
            self.assertEqual(bnode.status, "running")
            self.assertIn(bnode.instance_name, self.bnodes)
        return
    
    def eval_bosserver_shutdown(self) :
        for bnode in self.bos_server.bnodes :
            self.assertTrue(bnode.status in ["disabled", "stopped"] )
        return

    def eval_bosserver_startup(self) :
        for bnode in self.bos_server.bnodes :
            self.assertEqual(bnode.status, "running")
        return

    def eval_restart_times(self, expected, time_type) :
        self.assertEqual(self.bos_server.restart_times[time_type], expected)
        return 

    def eval_set_superusers(self, expected) :
        self.assertEqual(self.bos_server.superusers, expected)
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
        self.bnodes = self.test_config.get("BosService", "bnodes").split(",")
        self.newbinary_restart_time = self.test_config.get("BosService","newbinary_restart_time")
        self.general_restart_time = self.test_config.get("BosService","general_restart_time")
        self.superuser_list = self.test_config.get("BosService","superuser_list").split(",")
        return    

    def test_get_bosserver(self) :
        self.eval_get_bosserver(self.bos_server)
        return

    def test_shutdown_startup(self) :
        if not afs.CONFIG.enable_interrupting_tests :
            raise unittest.SkipTest("enable_interrupting_tests tests disabled.")
        self.bos_server = self.service.shutdown(self.bos_server)
        time.sleep(2)
        self.eval_bosserver_shutdown()
        self.bos_server = self.service.startup(self.bos_server)
        self.eval_bosserver_startup()
        return

    def test_restart_times(self) :
        if not afs.CONFIG.enable_modifying_tests :
            raise unittest.SkipTest("modifying tests disabled.")
        for time_type  in ["general", "newbinary"] :
            saved_restart_time = self.bos_server.restart_times[time_type]
            if self.newbinary_restart_time != "4:00 am" :
                self.bos_server.restart_times[time_type] = "4:00 am"
                expected = "4:00 am"
            else :
                self.bos_server.restart_times[time_type] = "5:00 am"
                expected = "5:00 am"
            self.service.set_restart_times(self.bos_server)
            self.bos_server = self.service.get_bos_server(self.server_name, cached=False)
            self.eval_restart_times(expected, time_type)
            # set it back
            self.bos_server.restart_times[time_type] = saved_restart_time
            self.service.set_restart_times(self.bos_server)
            self.eval_restart_times(saved_restart_time, time_type)
        return

    def test_setuser(self) :
        saved_superuser_list = self.bos_server.superusers
        self.bos_server.superusers = self.superuser_list
        self.service.set_superusers(self.bos_server)
        self.bos_server = self.service.get_bos_server(self.server_name, cached=False)
        self.eval_set_superusers(self.superuser_list)
        # set it back
        self.bos_server.superusers = saved_superuser_list
        self.service.set_superusers(self.bos_server)
        self.bos_server = self.service.get_bos_server(self.server_name, cached=False)
        self.eval_set_superusers(saved_superuser_list)
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
        self.bnodes = self.test_config.get("BosService", "bnodes").split(",")
        self.newbinary_restart_time = self.test_config.get("BosService","newbinary_restart_time")
        self.general_restart_time = self.test_config.get("BosService","general_restart_time")
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
