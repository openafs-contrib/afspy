#!/usr/bin/env python

"""
unit-test module for the BosServerLLA
"""

from ConfigParser import ConfigParser
import sys
import time
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
        for srv in res :
            if srv["hostname"] == self.test_db_server_clone and srv["isClone"] == 1 :
                found_clone = True
            if srv["hostname"] == self.test_db_server and srv["isClone"] == 0 :
                found_srv = True
        if not found_clone and self.test_db_server_clone != "" :
            self.fail("Did not find clone in dbserver list")    
        if not found_srv :
            self.fail("Did not find server in dbserver list")    
        return 

    def eval_get_superuser_list(self, res, should_include=None, should_not_include=None) :
        if should_include != None :
            self.assertIn(should_include, res)
        if should_not_include != None :
            self.assertNotIn(should_not_include, res)
        return

    def eval_get_bnodes(self, bnodes) :
        self.assertTrue(len(bnodes) > 0)
        return

    def eval_get_restart_times(self, restart_times) :
        self.assertEqual(self.bos_server_restart_time["general"], restart_times["general"])
        self.assertEqual(self.bos_server_restart_time["newbinary"], restart_times["newbinary"])
        return

    def eval_set_restart_time(self, restart_times, time_type, expected) :
        self.assertEqual(restart_times[time_type], expected)
        return

    def eval_restart(self, res) :
        return

    def eval_stop_bnode(self, res) :
        self.assertEqual(res, True)
        return

    def eval_start_bnode(self, res) :
        self.assertEqual(res, True)
        return

    def eval_startup(self, res) :
        self.assertEqual(res, True)
        return

    def eval_shutdown(self, res) :
        self.assertEqual(res, True)
        return

    def eval_execute_shell(self, res) :
        self.assertEqual(res, True)
        return

    def eval_get_filedate(self, res) :
        now = time.localtime()
        current = time.strptime(res["current"], '%b %d %H:%M:%S %Y')
        self.assertTrue(current < now )
        if res["backup"] != None :
            backup = time.strptime(res["backup"], '%b %d %H:%M:%S %Y')
            self.assertTrue( backup < now )
        if res["old"] != None :
            old = time.strptime(res["old"], '%b %d %H:%M:%S %Y')
            self.assertTrue( old < now )
        return

    def eval_get_log(self, res) :
        self.assertTrue(len(res) > 0)
        return

    def eval_prune_log(self, res) :
        self.assertEqual(res, True)
        return

    def eval_salvage_volume(self, res) :
        self.assertTrue('bos: salvage completed' in res)
        return

    def eval_salvage_partition(self, res) :
        self.assertTrue('bos: salvage completed' in res)
        return

    def eval_salvage_server(self, res) :
        self.assertTrue('bos: salvage completed' in res)
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
        self.bos_server_name =  self.test_config.get("BosServerLLA","server") 
        self.bos_server_restart_time =  { 
            "newbinary" : self.test_config.get("BosServerLLA","newbinary_restart_time"),
            "general" : self.test_config.get("BosServerLLA","general_restart_time") 
        }
        self.logfile = self.test_config.get("BosServerLLA","logfile")
        self.files_to_prune = self.test_config.get("BosServerLLA","files_to_prune")
        self.start_stop_bnode = self.test_config.get("BosServerLLA","start_stop_bnode")
        self.volume_name = self.test_config.get("BosServerLLA","vol_name")
        self.volume_partition = self.test_config.get("BosServerLLA","vol_part")
        self.test_superuser = self.test_config.get("BosServerLLA","superuser")
        self.test_db_server = self.test_config.get("BosServerLLA","db_server")
        self.test_db_server_clone = self.test_config.get("BosServerLLA","db_server_clone")
        return
  
    def test_get_superuser_list(self) :
        if not afs.CONFIG.enable_modifying_tests :
            raise unittest.SkipTest("modifying tests disabled.")
        res = self.lla.get_superuserlist(self.bos_server_name)
        self.eval_get_superuser_list(res)
        return

    def test_add_remove_superuser(self) :
        if not afs.CONFIG.enable_modifying_tests :
            raise unittest.SkipTest("modifying tests disabled.")
        res = self.lla.add_superuser(self.bos_server_name,[self.test_superuser, ])
        superuser_list = self.lla.get_superuserlist(self.bos_server_name)
        self.eval_get_superuser_list(superuser_list, should_include=self.test_superuser)
        self.lla.remove_superuser(self.bos_server_name,[self.test_superuser, ])
        superuser_list = self.lla.get_superuserlist(self.bos_server_name)
        self.eval_get_superuser_list(superuser_list, should_not_include=self.test_superuser)
        return

    def test_get_db_servers(self) :
        res = self.lla.get_db_servers(self.bos_server_name)
        self.eval_get_db_servers(res)
        return 

    def test_get_log(self) :
        """
        test reading a logfile
        """ 
        if not afs.CONFIG.enable_harmless_auth_tests :
            raise unittest.SkipTest("harmless tests requiring authorization disabled.")
        res = self.lla.get_log(self.bos_server_name, self.logfile)
        self.eval_get_log(res)
        return

    def test_get_bnodes(self) :
        """
        test geting in bnodes
        """ 
        res = self.lla.get_bnodes(self.bos_server_name)
        self.eval_get_bnodes(res)
        return
     
    def test_get_restart_times(self) :
        """
        test retrieving restart times into object
        """ 
        res = self.lla.get_restart_times(self.bos_server_name)
        self.eval_get_restart_times(res)
        return 

    def test_set_restart_time(self) :
        """
        test setting general restart time from object to live-system
        """
        saved_restart_time = self.lla.get_restart_times(self.bos_server_name)
        for time_type in ["general", "newbinary" ] :
            if saved_restart_time[time_type] != "4:00 am" :
                time_string = "4:00 am"
            else :
                time_string = "5:00 am"
            res = self.lla.set_restart_time(self.bos_server_name, time_type, time_string)
            new_times = self.lla.get_restart_times(self.bos_server_name)
            self.eval_set_restart_time(new_times, time_type, time_string)
            # set back to old values
            time_string = saved_restart_time[time_type]
            res = self.lla.set_restart_time(self.bos_server_name, time_type, time_string)
            new_times = self.lla.get_restart_times(self.bos_server_name)
            self.eval_set_restart_time(new_times, time_type, time_string)
        return

    def test_restart(self) :
        """
        test restarting 
        """
        if not afs.CONFIG.enable_interrupting_tests :
            raise unittest.SkipTest("interrupting tests disabled.")
        res = self.lla.restart(self.bos_server_name, "-all", restart_bosserver=False)
        self.eval_restart(res)
        return

    def test_execute_shell(self) :
	"""
        test executing a shell command
        """
        if not afs.CONFIG.enable_harmless_auth_tests :
            raise unittest.SkipTest("harmless tests requiring authorization disabled.")
        res = self.lla.execute_shell(self.bos_server_name,"/bin/ls")
        self.eval_execute_shell(res)
        return

    def test_get_filedate(self) :
        """
        test getting the date of a file
        """
        res = self.lla.get_filedate(self.bos_server_name, ["fileserver"])
        self.eval_get_filedate(res)
        return

    def test_prune_log(self) :
        """
        test pruning a log
        """
        if not afs.CONFIG.enable_destructive_tests :
            raise unittest.SkipTest("destructive tests disabled.")
        res = self.lla.prune_log(self.bos_server_name, self.files_to_prune) 
        self.eval_prune_log(res)
        return

    def test_salvage_volume(self) :
        """
        salvage a volume
        """
        if not afs.CONFIG.enable_modifying_tests :
            raise unittest.SkipTest("modifying tests disabled.")
        res = self.lla.salvage(self.bos_server_name, partition=self.volume_partition, volume=self.volume_name)
        self.eval_salvage_volume(res)
        return

    def test_salvage_partition(self) :
        """
        salvage a volume
        """
        if not afs.CONFIG.enable_modifying_tests :
            raise unittest.SkipTest("modifying tests disabled.")
        res = self.lla.salvage(self.bos_server_name, partition=self.volume_partition)
        self.eval_salvage_partition(res)
        return

    def test_salvage_server(self) :
        """
        salvage a volume
        """
        if not afs.CONFIG.enable_modifying_tests :
            raise unittest.SkipTest("modifying tests disabled.")
        res = self.lla.salvage(self.bos_server_name)
        self.eval_salvage_server(res)
        return
   
    def test_shutdown_startup(self) :
        """
        test shutting down and starting up
        """
        if not afs.CONFIG.enable_interrupting_tests :
            raise unittest.SkipTest("enable_interrupting_tests tests disabled.")
        res = self.lla.shutdown(self.bos_server_name)
        self.eval_shutdown(res)
        res = self.lla.startup(self.bos_server_name)
        self.eval_startup(res)
        return

    def test_start_stop_bnode(self) :
        """
        test starting and stopping a bnode
        """ 
        if not afs.CONFIG.enable_interrupting_tests :
            raise unittest.SkipTest("enable_interrupting_tests tests disabled.")
        res = self.lla.start_bnodes(self.bos_server_name, [self.start_stop_bnode])
        self.eval_stop_bnode(res)
        res = self.lla.start_bnodes(self.bos_server_name,[ self.start_stop_bnode])
        self.eval_start_bnode(res)
        return

class TestBosServerLLAMethods_async(EvaluateTestResults) :

    @classmethod  
    def setUpClass(self) :
        """
        setup test environment
        called automagically.
        """
        self.lla = afs.lla.BosServerLLA.BosServerLLA()
        self.test_config = ConfigParser()
        self.test_config.read(afs.CONFIG.setup)
        self.bos_server_name =  self.test_config.get("BosServerLLA","server") 
        self.bos_server_restart_time =  { 
            "newbinary" : self.test_config.get("BosServerLLA","newbinary_restart_time"),
            "general" : self.test_config.get("BosServerLLA","general_restart_time") 
        }
        self.logfile = self.test_config.get("BosServerLLA","logfile")
        self.files_to_prune = self.test_config.get("BosServerLLA","files_to_prune")
        self.start_stop_bnode = self.test_config.get("BosServerLLA","start_stop_bnode")
        self.volume_name = self.test_config.get("BosServerLLA","vol_name")
        self.volume_partition = self.test_config.get("BosServerLLA","vol_part")
        self.test_superuser = self.test_config.get("BosServerLLA","superuser")
        self.test_db_server = self.test_config.get("BosServerLLA","db_server")
        self.test_db_server_clone = self.test_config.get("BosServerLLA","db_server_clone")
        return

    def test_get_superuser_list(self) :
        if not afs.CONFIG.enable_modifying_tests :
            raise unittest.SkipTest("modifying tests disabled.")
        sp_ident = self.lla.get_superuserlist(self.bos_server_name, async=True) 
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_get_superuser_list(res)
        return

    def test_add_remove_superuser(self) :
        if not afs.CONFIG.enable_modifying_tests :
            raise unittest.SkipTest("modifying tests disabled.")
        sp_ident = self.lla.add_superuser(self.bos_server_name, [self.test_superuser, ], async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.assertTrue(res)
        superuser_list = self.lla.get_superuserlist(self.bos_server_name)
        self.eval_get_superuser_list(superuser_list, should_include=self.test_superuser)
        sp_ident = self.lla.remove_superuser(self.bos_server_name, [self.test_superuser, ], async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.assertTrue(res)
        superuser_list = self.lla.get_superuserlist(self.bos_server_name)
        self.eval_get_superuser_list(superuser_list, should_not_include=self.test_superuser)
        return

    def test_get_db_servers(self) :
        sp_ident = self.lla.get_db_servers(self.bos_server_name, async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_get_db_servers(res)
        return 

    def test_get_log(self) :
        """
        test reading a logfile
        """ 
        if not afs.CONFIG.enable_harmless_auth_tests :
            raise unittest.SkipTest("harmless tests requiring authorization disabled.")
        sp_ident = self.lla.get_log(self.bos_server_name, self.logfile, async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.assertTrue(len(res) > 0)
        return

    def test_get_db_servers(self) :
        sp_ident = self.lla.get_db_servers(self.bos_server_name, async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_get_db_servers(res)
        return

    def test_get_bnodes(self) :
        """
        test geting in bnodes
        """ 
        sp_ident = self.lla.get_bnodes(self.bos_server_name, async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_get_bnodes(res)
        return
     
    def test_get_restart_times(self) :
        """
        test retrieving restart times into object
        """ 
        sp_ident = self.lla.get_restart_times(self.bos_server_name, async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_get_restart_times(res)
        return 

    def test_set_restart_time(self) :
        """
        test setting general restart time from object to live-system
        """
        saved_restart_time = self.lla.get_restart_times(self.bos_server_name)
        for time_type in ["general", "newbinary" ] :
            if saved_restart_time[time_type] != "4:00 am" :
                time_string = "4:00 am"
            else :
                time_string = "5:00 am"
            sp_ident = self.lla.set_restart_time(self.bos_server_name, time_type, time_string, async=True)
            self.lla.wait_for_subprocess(sp_ident)
            res = self.lla.get_subprocess_result(sp_ident)
            self.assertTrue(res != None)
            new_times = self.lla.get_restart_times(self.bos_server_name)
            self.eval_set_restart_time(new_times, time_type, time_string)
            # set back to old values
            time_string = saved_restart_time[time_type]
            sp_ident = self.lla.set_restart_time(self.bos_server_name, time_type, time_string, async=True)
            self.lla.wait_for_subprocess(sp_ident)
            res = self.lla.get_subprocess_result(sp_ident)
            self.assertTrue(res != None)
            new_times = self.lla.get_restart_times(self.bos_server_name)
            self.eval_set_restart_time(new_times, time_type, time_string)
        return

    def test_restart(self) :
        """
        test restarting 
        """
        if not afs.CONFIG.enable_interrupting_tests :
            raise unittest.SkipTest("interrupting tests disabled.")
        sp_ident = self.lla.restart(self.bos_server_name, "-all", restart_bosserver=False, async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_restart(res)
        return

    def test_execute_shell(self) :
	"""
        test executing a shell command
        """
        if not afs.CONFIG.enable_harmless_auth_tests :
            raise unittest.SkipTest("harmless tests requiring authorization disabled.")
        sp_ident = self.lla.execute_shell(self.bos_server_name, "/bin/ls", async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_execute_shell(res)
        return

    def test_get_filedate(self) :
        """
        test getting the date of a file
        """
        sp_ident = self.lla.get_filedate(self.bos_server_name, ["fileserver"], async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_get_filedate(res)
        return

    def test_prune_log(self) :
        """
        test pruning a log
        """
        if not afs.CONFIG.enable_destructive_tests :
            raise unittest.SkipTest("destructive tests disabled.")
        sp_ident = self.lla.prune_log(self.bos_server_name, self.files_to_prune, async=True) 
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
        sp_ident = self.lla.salvage(self.bos_server_name, partition=self.volume_partition, volume=self.volume_name, async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_salvage_volume(res)
        return

    def test_salvage_partition(self) :
        """
        salvage all volumes on a partition
        """
        if not afs.CONFIG.enable_modifying_tests :
            raise unittest.SkipTest("modifying tests disabled.")
        sp_ident = self.lla.salvage(self.bos_server_name, partition=self.volume_partition, async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_salvage_partition(res)
        return

    def test_salvage_server(self) :
        """
        salvage all volumes on this server
        """
        if not afs.CONFIG.enable_modifying_tests :
            raise unittest.SkipTest("modifying tests disabled.")
        sp_ident = self.lla.salvage(self.bos_server_name, async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_salvage_server(res)
        return

    def test_shutdown_startup(self) :
        """
        test shutting down and starting up
        """
        if not afs.CONFIG.enable_interrupting_tests :
            raise unittest.SkipTest("enable_interrupting_tests tests disabled.")
        sp_ident = self.lla.shutdown(self.bos_server_name, async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_shutdown(res)

        sp_ident = self.lla.startup(self.bos_server_name, async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_startup(res)
        return

    def test_start_stop_bnode(self) :
        """
        test starting and stopping a bnode
        """ 
        if not afs.CONFIG.enable_interrupting_tests :
            raise unittest.SkipTest("enable_interrupting_tests tests disabled.")
        sp_ident = self.lla.stop_bnodes(self.bos_server_name,[ self.start_stop_bnode], async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_stop_bnode(res)

        sp_ident = self.lla.start_bnodes(self.bos_server_name, [self.start_stop_bnode], async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_start_bnode(res)
        return

if __name__ == '__main__' :
    # disable DBCACHE stuff, since we are dealing with LLA only
    parse_commandline()
    sys.stderr.write("\n===\n=== testing direct fork ===\n===\n\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBosServerLLAMethods)
    unittest.TextTestRunner(verbosity = 2).run(suite)
    sys.stderr.write("\n===\n=== testing detached execution ===\n===\n\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBosServerLLAMethods_async)
    unittest.TextTestRunner(verbosity = 2).run(suite)
