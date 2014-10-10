#!/usr/bin/env python

"""
unit-test module for the BosServerLLA
"""

from ConfigParser import ConfigParser
import sys
import unittest
from afs.tests.BaseTest import parse_commandline
import afs.lla.BosServerLLA
import afs.model.BosServer
import afs.model.Volume
import afs.model.BNode

class EvaluateTestResults(unittest.TestCase) :

    def eval_get_db_servers(self, res) :
        found_clone = False
        found_srv = False
        for srv in self.bos_server.db_servers :
            if srv["hostname"] == self.test_db_server_clone and srv["isClone"] == 1 :
                found_clone = True
            if srv["hostname"] == self.test_db_server and srv["isClone"] == 0 :
                found_srv = True
        if not found_clone and self.test_db_server_clone != "" :
            self.fail("Did not find clone in dbserver list")    
        if not found_srv :
            self.fail("Did not find server in dbserver list")    
        return 

    def eval_get_user_list(self, res, should_include=None, should_not_include=None) :
        if should_include != None :
            self.assertIn(should_include, self.bos_server.superusers)
        if should_not_include != None :
            self.assertNotIn(should_not_include, self.bos_server.superusers)
        # XXX check for basic user_list, needs to be defined in Test.cfg
        return

    def eval_get_bnodes(self, res) :
        self.assertTrue(len(res.bnodes) > 0)
        return

    def eval_get_restart_times(self, res) :
        self.assertEqual(self.bos_server.newbinary_restart_time, res.newbinary_restart_time)
        self.assertEqual(self.bos_server.general_restart_time, res.general_restart_time)
        return

    def eval_restart(self, res) :
        return

    def eval_execute_shell(self, res) :
        return


class TestBosServerLLAMethods(EvaluateTestResults):
    """
    Tests BosServerPeerLLA Methods
    """

    @classmethod  
    def setUpClass(self) :
        """
        setup test environment
        called automagically
        """
        self.lla = afs.lla.BosServerLLA.BosServerLLA()
        self.test_config = ConfigParser()
        self.test_config.read(afs.CONFIG.setup)
        self.bos_server = afs.model.BosServer.BosServer()
        self.bos_server.servernames =  [self.test_config.get("BosServerLLA","server"), ]
        self.bos_server.newbinary_restart_time = self.test_config.get("BosServerLLA","newbinary_restart_time")
        self.bos_server.general_restart_time = self.test_config.get("BosServerLLA","general_restart_time")
        self.logfile = self.test_config.get("BosServerLLA","logfile")
        self.volume_name = self.test_config.get("BosServerLLA","vol_name")
        self.volume_partition = self.test_config.get("BosServerLLA","vol_part")
        self.test_superuser = self.test_config.get("BosServerLLA","superuser")
        self.test_db_server = self.test_config.get("BosServerLLA","db_server")
        self.test_db_server_clone = self.test_config.get("BosServerLLA","db_server_clone")
        return
  
    def test_get_user_list(self) :
        if not afs.CONFIG.enable_modifying_tests :
            raise unittest.SkipTest("modifying tests disabled.")
        res = self.lla.get_userlist(self.bos_server) 
        self.eval_get_user_list(res)
        return

    def test_add_remove_user(self) :
        if not afs.CONFIG.enable_modifying_tests :
            raise unittest.SkipTest("modifying tests disabled.")
        res = self.lla.add_user(self.bos_server,[self.test_superuser, ])
        self.eval_get_user_list(res, should_include=self.test_superuser)
        res = self.lla.remove_user(self.bos_server,[self.test_superuser, ])
        self.eval_get_user_list(res, should_not_include=self.test_superuser)
        return

    def test_get_db_servers(self) :
        res = self.lla.get_db_servers(self.bos_server)
        self.eval_get_db_servers(res)
        return 

    def test_get_log(self) :
        """
        test reading a logfile
        """ 
        if not afs.CONFIG.enable_harmless_auth_tests :
            raise unittest.SkipTest("tests requiring authentication disabled.")
        res = self.lla.get_log(self.bos_server, self.logfile)
        self.eval_get_log(res)
        return

    def test_get_bnodes(self) :
        """
        test geting in bnodes
        """ 
        res = self.lla.get_bnodes(self.bos_server)
        self.eval_get_bnodes(res)
        return
     
    def test_get_restart_times(self) :
        """
        test retrieving restart times into object
        """ 
        res = self.lla.get_restart_times(self.bos_server)
        self.eval_get_restart_times(res)
        return 

    def test_push_binary_restart_times(self) :
        """
        test pushing binary-restart-time from object to live-system
        """
        if not afs.CONFIG.enable_modifying_tests :
            raise unittest.SkipTest("modifying tests disabled.")
        obj = self.lla.push_restart_times(self.bos_server)
        res = self.assertEqual(self.bos_server.newbinary_restart_time, obj.newbinary_restart_time)
        self.assertEqual(self.bos_server.general_restart_time, obj.general_restart_time)
        self.eval_push_binary_restart_times(res)
        return

    def test_push_binary_restart_times(self) :
        """
        test pushing general restart time from object to live-system
        """
        if not afs.CONFIG.enable_modifying_tests :
            raise unittest.SkipTest("modifying tests disabled.")
        res = self.lla.push_restart_times(self.bos_server)
        self.eval_push_general_restart_times(res)
        return
   
    def test_restart(self) :
        """
        test restarting 
        """
        if not afs.CONFIG.enable_interrupting_tests :
            raise unittest.SkipTest("enable_interrupting_tests tests disabled.")
        res = self.lla.restart(self.bos_server, restart_bosserver=False)
        self.eval_restart(res)
        return

    def test_execute_shell(self) :
	"""
        test executing a shell command
        """
        if not afs.CONFIG.enable_harmless_auth_tests :
            raise unittest.SkipTest("modifying tests disabled.")
        res = self.lla.execute_shell(self.bos_server,"/bin/ls")
        self.assertEqual(rest, True)
        self.eval_execute_shell(res)
        return

    def test_get_filedate(self) :
        """
        test getting the date of a file
        """
        res = self.lla.get_filedate(self.bos_server, ["fileserver"])
        self.assertTrue(res.has_key("current"))
        self.eval_execute_shell(res)
        return

    def test_prune_log(self) :
        """
        test pruning a log
        """
        if not afs.CONFIG.enable_destructive_tests :
            raise unittest.SkipTest("destructive tests disabled.")
        res = self.lla.prune_log(self.bos_server,"core") 
        self.eval_prune_log(res)
        return

    def test_salvage_volume(self) :
        """
        salvage a volume
        """
        if not afs.CONFIG.enable_modifying_tests :
            raise unittest.SkipTest("modifying tests disabled.")
        vol = afs.model.Volume.Volume()
        vol.name = self.volume_name
        vol.partition = self.volume_partition
        result = self.lla.salvage_volume(self.bos_server,vol)
        self.eval_salvage_volume(res)
        return
   
    def test_shutdown_startup(self) :
        """
        test shutting down and starting up
        """
        if not afs.CONFIG.enable_interrupting_tests :
            raise unittest.SkipTest("enable_interrupting_tests tests disabled.")
        res_shutdown = self.lla.shutdown(self.bos_server)
        res_startup = self.lla.startup(self.bos_server)
        self.eval_shutdown_startup(res_shutdwon, res_startup)
        return

    def test_start_stop_bnode(self) :
        """
        test starting and stopping a bnode
        """ 
        if not afs.CONFIG.enable_interrupting_tests :
            raise unittest.SkipTest("enable_interrupting_tests tests disabled.")
        bnode=afs.model.BNode.BNode(instance_name="fs")
        res_stop = self.lla.stop_bnodes(self.bos_server,[ bnode])
        res_start = self.lla.start_bnodes(self.bos_server, [bnode])
        self.eval_start_stop_bnode(res_stop, res_start)
        return

class TestBosServerLLAMethods_async(EvaluateTestResults) :

    @classmethod  
    def setUpClass(self) :
        """
        setup test environment
        called automagically.
        Same as in sync-case, but the attribute self.async
        """
        self.lla = afs.lla.BosServerLLA.BosServerLLA()
        self.test_config = ConfigParser()
        self.test_config.read(afs.CONFIG.setup)
        self.bos_server = afs.model.BosServer.BosServer()
        self.bos_server.servernames =  [self.test_config.get("BosServerLLA","server"), ]
        self.bos_server.newbinary_restart_time = self.test_config.get("BosServerLLA","newbinary_restart_time")
        self.bos_server.general_restart_time = self.test_config.get("BosServerLLA","general_restart_time")
        self.logfile = self.test_config.get("BosServerLLA","logfile")
        self.volume_name = self.test_config.get("BosServerLLA","vol_name")
        self.volume_partition = self.test_config.get("BosServerLLA","vol_part")
        self.test_superuser = self.test_config.get("BosServerLLA","superuser")
        self.test_db_server = self.test_config.get("BosServerLLA","db_server")
        self.test_db_server_clone = self.test_config.get("BosServerLLA","db_server_clone")
        return

    def test_get_user_list(self) :
        if not afs.CONFIG.enable_modifying_tests :
            raise unittest.SkipTest("modifying tests disabled.")
        sp_ident = self.lla.get_userlist(self.bos_server, async=True) 
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_get_user_list(res)
        return

    def test_add_remove_user(self) :
        if not afs.CONFIG.enable_modifying_tests :
            raise unittest.SkipTest("modifying tests disabled.")
        sp_ident = self.lla.add_user(self.bos_server, [self.test_superuser, ], async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_get_user_list(res, should_include=self.test_superuser)
        sp_ident = self.lla.remove_user(self.bos_server, [self.test_superuser, ], async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_get_user_list(res, should_not_include=self.test_superuser)
        return

    def test_get_db_servers(self) :
        sp_ident = self.lla.get_db_servers(self.bos_server, async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_get_db_servers(res)
        return 

    def test_get_log(self) :
        """
        test reading a logfile
        """ 
        if not afs.CONFIG.enable_harmless_auth_tests :
            raise unittest.SkipTest("tests requiring authentication disabled.")
        sp_ident = self.lla.get_log(self.bos_server, self.logfile, async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.assertTrue(len(res) > 0)
        return

    def test_get_db_servers(self) :
        sp_ident = self.lla.get_db_servers(self.bos_server, async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_get_db_servers(res)
        return

    def test_get_bnodes(self) :
        """
        test geting in bnodes
        """ 
        sp_ident = self.lla.get_bnodes(self.bos_server, async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_get_bnodes(res)
        return
     
    def test_get_restart_times(self) :
        """
        test retrieving restart times into object
        """ 
        sp_ident = self.lla.get_restart_times(self.bos_server, async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_get_restart_times(res)
        return 

    def test_set_binary_restart_times(self) :
        """
        test pushing binary-restart-time from object to live-system
        """
        if not afs.CONFIG.enable_modifying_tests :
            raise unittest.SkipTest("modifying tests disabled.")
        sp_ident = self.lla.set_binary_restart_times(self.bos_server, async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_push_binary_restart_times(res)
        return

    def test_set_binary_restart_times(self) :
        """
        test pushing general restart time from object to live-system
        """
        if not afs.CONFIG.enable_modifying_tests :
            raise unittest.SkipTest("modifying tests disabled.")
        sp_ident = self.lla.set_restart_times(self.bos_server, async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_push_general_restart_times(res)
        return
   
    def test_restart(self) :
        """
        test restarting 
        """
        if not afs.CONFIG.enable_interrupting_tests :
            raise unittest.SkipTest("enable_interrupting_tests tests disabled.")
        sp_ident = self.lla.restart(self.bos_server, restart_bosserver=False, async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_restart(res)
        return

    def test_execute_shell(self) :
	"""
        test executing a shell command
        """
        if not afs.CONFIG.enable_harmless_auth_tests :
            raise unittest.SkipTest("modifying tests disabled.")
        sp_ident = self.lla.execute_shell(self.bos_server, "/bin/ls", async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_execute_shell(res)
        return

    def test_get_filedate(self) :
        """
        test getting the date of a file
        """
        sp_ident = self.lla.get_filedate(self.bos_server, ["fileserver"], async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_execute_shell(res)
        return

    def test_prune_log(self) :
        """
        test pruning a log
        """
        if not afs.CONFIG.enable_destructive_tests :
            raise unittest.SkipTest("destructive tests disabled.")
        sp_ident = self.lla.prune_log(self.bos_server, "core", async=True) 
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_prune_log(res)
        return

    def test_salvage_volume(self) :
        """
        salvage a volume
        """
        if not afs.CONFIG.enable_modifying_tests :
            raise unittest.SkipTest("modifying tests disabled.")
        vol = afs.model.Volume.Volume()
        vol.name = self.volume_name
        vol.partition = self.volume_partition
        sp_ident = self.lla.salvage_volume(self.bos_server, vol, async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_salvage_volume(res)
        return
   
    def test_shutdown_startup(self) :
        """
        test shutting down and starting up
        """
        if not afs.CONFIG.enable_interrupting_tests :
            raise unittest.SkipTest("enable_interrupting_tests tests disabled.")
        sp_ident = self.lla.shutdown(self.bos_server, async=True)
        res_shutdwon = self.lla.get_subprocess_result(sp_ident)
        sp_ident = self.lla.startup(self.bos_server, async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res_startup = self.lla.get_subprocess_result(sp_ident)
        self.eval_shutdown_startup(res_shutdwon, res_startup)
        return

    def test_start_stop_bnode(self) :
        """
        test starting and stopping a bnode
        """ 
        if not afs.CONFIG.enable_interrupting_tests :
            raise unittest.SkipTest("enable_interrupting_tests tests disabled.")
        bnode=afs.model.BNode.BNode(instance_name="fs")
        sp_ident = self.lla.stop_bnodes(self.bos_server,[ bnode], async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res_stop = self.lla.get_subprocess_result(sp_ident)
        sp_ident = self.lla.start_bnodes(self.bos_server, [bnode], async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res_start = self.lla.get_subprocess_result(sp_ident, async=True)
        self.eval_start_stop_bnode(res_stop, res_start)

if __name__ == '__main__' :
    # disable DBCACHE stuff, since we are dealing with LLA only
    parse_commandline()
    sys.stderr.write("\n===\n=== testing direct fork ===\n===\n\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBosServerLLAMethods)
    unittest.TextTestRunner(verbosity = 2).run(suite)
    sys.stderr.write("\n===\n=== testing detached execution ===\n===\n\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBosServerLLAMethods_async)
    unittest.TextTestRunner(verbosity = 2).run(suite)
