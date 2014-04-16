#!/usr/bin/env python

"""
unit-test module for the BosServerDAO
"""

from ConfigParser import ConfigParser
import sys
import unittest
from afs.tests.BaseTest import parse_commandline
import afs.dao.BosServerDAO
import afs.model.BosServer
import afs.model.Volume
import afs.model.BNode

class TestBosServerDAOMethods(unittest.TestCase):
    """
    Tests BosServerPeerDAO Methods
    """

    @classmethod  
    def setUp(self):
        """
        setup test environment
        called automagically
        """
        self.dao = afs.dao.BosServerDAO.BosServerDAO()
        self.test_config = ConfigParser()
        self.test_config.read(afs.CONFIG.setup)
        self.bos_server = afs.model.BosServer.BosServer()
        self.bos_server.servername =  self.test_config.get("BosServerDAO","server")
        self.bos_server.newbinary_restart_time = self.test_config.get("BosServerDAO","newbinary_restart_time")
        self.bos_server.general_restart_time = self.test_config.get("BosServerDAO","general_restart_time")
        self.logfile = self.test_config.get("BosServerDAO","logfile")
        self.volume_name = self.test_config.get("BosServerDAO","vol_name")
        self.volume_partition = self.test_config.get("BosServerDAO","vol_part")
        self.test_superuser = self.test_config.get("BosServerDAO","superuser")
        self.test_db_server = self.test_config.get("BosServerDAO","db_server")
        self.test_db_server_clone = self.test_config.get("BosServerDAO","db_server_clone")
        return
  
    def test_user_management(self) :
        if not afs.CONFIG.modifying :
            raise unittest.SkipTest("modifying tests disabled.")
        self.dao.pull_userlist(self.bos_server) 
        if self.test_superuser in self.bos_server.superusers :
            raise RuntimeError("Superuser %s already in userlist." % self.test_superuser)
        self.dao.add_user(self.bos_server,[self.test_superuser, ])
        if not self.test_superuser in self.bos_server.superusers :
            self.fail("did not add %s to superuserlist." % self.test_superuser)
        self.dao.remove_user(self.bos_server,[self.test_superuser, ])
        if self.test_superuser in self.bos_server.superusers :
            self.fail("did not remove %s from superuserlist." % self.test_superuser)
        return

    def test_pull_db_servers(self) :
        self.dao.pull_db_servers(self.bos_server)
        found_clone = False
        found_srv = False
        for srv in self.bos_server.db_servers :
            if srv["hostname"] == self.test_db_server_clone and srv["isClone"] == 1 :
                found_clone = True
            if srv["hostname"] == self.test_db_server and srv["isClone"] == 0 :
                found_srv = True
        if not found_clone :
            self.fail("Did not find clone in dbserver list")    
        if not found_srv :
            self.fail("Did not find server in dbserver list")    
        return

    def test_push_bos_server(self) :
        """
        XXX just test for error 
        """
        if not afs.CONFIG.modifying :
            raise unittest.SkipTest("modifying tests disabled.")
        self.dao.push_bos_server(self.bos_server)
        return

    def test_get_log(self) :
        """
        test reading a logfile
        """ 
        res = self.dao.get_log(self.bos_server, self.logfile)
        self.assertTrue(len(res) > 0)
        return

    def test_pull_bnodes(self) :
        """
        test pulling in bnodes
        """ 
        res = self.dao.pull_bnodes(self.bos_server)
        self.assertTrue(len(self.bos_server.bnodes) > 0)
        return
     
    def test_pull_restart_times(self) :
        """
        test retrieving restart times into object
        """ 
        obj = self.dao.pull_restart_times(self.bos_server)
        self.assertEqual(self.bos_server.newbinary_restart_time, obj.newbinary_restart_time)
        self.assertEqual(self.bos_server.general_restart_time, obj.general_restart_time)
        return

    def test_push_restart_times(self) :
        """
        test pushing time into object
        """
        if not afs.CONFIG.modifying :
            raise unittest.SkipTest("modifying tests disabled.")
        obj = self.dao.push_restart_times(self.bos_server)
        self.assertEqual(self.bos_server.newbinary_restart_time, obj.newbinary_restart_time)
        self.assertEqual(self.bos_server.general_restart_time, obj.general_restart_time)
        return 
   
    def test_restart(self) :
        """
        test restarting 
        """
        if not afs.CONFIG.interrupting :
            raise unittest.SkipTest("interrupting tests disabled.")
        self.dao.restart(self.bos_server,restart_bosserver=False)
        return

    def test_execute_shell(self) :
	"""
        test executing a shell command
        """
        result = self.dao.execute_shell(self.bos_server,"/bin/ls")
        self.assertEqual(result,True)
        return

    def test_get_filedate(self) :
        """
        test getting the date of a file
        """
        result = self.dao.get_filedate(self.bos_server,[ "fileserver"])
        self.assertTrue(result.has_key("current"))
        return

    def test_prune_log(self) :
        """
        test pruning a log
        """
        if not afs.CONFIG.destructive :
            raise unittest.SkipTest("destructive tests disabled.")
        result = self.dao.prune_log(self.bos_server,"core") 
        return

    def test_salvage_volume(self) :
        """
        salvage a volume
        """
        if not afs.CONFIG.modifying :
            raise unittest.SkipTest("modifying tests disabled.")
        vol = afs.model.Volume.Volume()
        vol.name = self.volume_name
        vol.partition = self.volume_partition
        result = self.dao.salvage_volume(self.bos_server,vol)
        return
   
    def test_shutdown_startup(self) :
        """
        test shutting down and starting up
        """
        if not afs.CONFIG.interrupting :
            raise unittest.SkipTest("interrupting tests disabled.")
        result_1 = self.dao.shutdown(self.bos_server)
        result_2 = self.dao.startup(self.bos_server)
        return

    def test_start_stop_bnode(self) :
        """
        test starting and stopping a bnode
        """ 
        if not afs.CONFIG.interrupting :
            raise unittest.SkipTest("interrupting tests disabled.")
        bnode=afs.model.BNode.BNode(instance_name="fs")
        result_1 = self.dao.stop_bnodes(self.bos_server,[bnode])
        result_2 = self.dao.start_bnodes(self.bos_server,[bnode])
        return
        

if __name__ == '__main__' :
    # disable DBCACHE stuff, since we are dealing with DAO only
    parse_commandline()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBosServerDAOMethods)
    unittest.TextTestRunner(verbosity = 2).run(suite)
