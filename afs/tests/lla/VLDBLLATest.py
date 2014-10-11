#!/usr/bin/env python

"""
Unittest for the LLA module VLDBLLA
"""

from ConfigParser import ConfigParser
import datetime
import os
import sys
import time
import unittest

from afs.tests.BaseTest import parse_commandline
import afs.lla.VLDBLLA
import afs.lla.VolServerLLA 
import afs

class EvaluateTestResults(unittest.TestCase) :
    """
    evaluate results
    """

    def eval_vos_addsite(self, res) :
        self.assertEqual(res, True)
        return

    def eval_vos_remsite(self, res) :
        self.assertEqual(res, True)
        return

    def eval_vos_lock(self, res) :
        self.assertEqual(res, True)
        return
    
    def eval_vos_unlock(self, res) :
        self.assertEqual(res, True)
        return

    def eval_get_fileserver_uuid(self, res) :
        self.assertEqual(res, self.fileserver_uuid)
        return

    def eval_get_fileserver_list(self, res) :
        found_uuid = False
        for vol_dict in res :
            if self.fileserver_uuid == vol_dict["uuid"] :
                found_uuid = True 
        self.assertTrue(found_uuid)
        return

    def eval_get_volume_list(self, res) :
        self.assertTrue(len(res) > 0)
        return

    def eval_sync_vldb(self, res) :
        self.assertTrue(res)
        return

    def eval_sync_serv(self, res) :
        self.assertTrue(res)
        return

class TestVLDBLLAMethods(EvaluateTestResults) :
    """
    Tests VLDBLLA Methods
    """

    @classmethod
    def setUpClass(self) :
        """
        setup test environment
        called automagically
        """
        self.lla = afs.lla.VLDBLLA.VLDBLLA()
        self.vols_lla = afs.lla.VolServerLLA.VolServerLLA()
        self.test_config = ConfigParser()
        self.test_config.read(afs.CONFIG.setup)
        self.tmp_volume = afs.model.Volume.Volume()
        self.tmp_volume.name = self.test_config.get("VLDBLLA", "TmpVolName")
        self.tmp_volume.servername = self.test_config.get("VLDBLLA", "FS")
        self.tmp_volume.partition = self.test_config.get("VLDBLLA","Part")
        self.fileserver_name = self.test_config.get("VLDBLLA", "FS")
        self.fileserver_uuid = self.test_config.get("VLDBLLA", "FS_UUID")
        return

    def test_vos_addsite_remsite(self) :
        if not afs.CONFIG.enable_modifying_tests :
            raise unittest.SkipTest("modifying tests disabled.")
        self.vols_lla.create(self.tmp_volume)
        res = self.lla.addsite(self.tmp_volume)
        self.eval_vos_addsite(res) 
        res = self.lla.remsite(self.tmp_volume)
        self.eval_vos_remsite(res) 
        self.vols_lla.remove(self.tmp_volume)
        return

    def test_vos_lock_unlock(self) :
        self.vols_lla.create(self.tmp_volume)
        res = self.lla.lock(self.tmp_volume)
        self.eval_vos_lock(res)
        res = self.lla.unlock(self.tmp_volume)
        self.eval_vos_unlock(res)
        self.vols_lla.remove(self.tmp_volume)
        return

    def test_get_fileserver_uuid(self) :
        res = self.lla.get_fileserver_uuid(self.fileserver_name)
        self.eval_get_fileserver_uuid(res)
        return

    def test_get_fileserver_list(self) :
        res = self.lla.get_fileserver_list()
        self.eval_get_fileserver_list(res)
        return

    def test_get_volume_list(self) :
        res = self.lla.get_volume_list()
        self.eval_get_volume_list(res)
        return

    def test_sync_vldb(self) :
        res = self.lla.sync_vldb(self.fileserver_name)
        self.eval_sync_vldb(res)
        return

    def test_sync_serv(self) :
        res = self.lla.sync_serv(self.fileserver_name)
        self.eval_sync_serv(res)
        return

class TestVLDBLLAMethods_async(EvaluateTestResults):
    """
    Tests VLDBLLA Methods
    """

    @classmethod
    def setUpClass(self) :
        """
        setup test environment
        called automagically
        """
        self.lla = afs.lla.VLDBLLA.VLDBLLA()
        self.vols_lla = afs.lla.VolServerLLA.VolServerLLA()
        self.test_config = ConfigParser()
        self.test_config.read(afs.CONFIG.setup)
        self.tmp_volume = afs.model.Volume.Volume()
        self.tmp_volume.name = self.test_config.get("VLDBLLA", "TmpVolName")
        self.tmp_volume.servername = self.test_config.get("VLDBLLA", "FS")
        self.tmp_volume.partition = self.test_config.get("VLDBLLA","Part")
        self.fileserver_name = self.test_config.get("VLDBLLA", "FS")
        self.fileserver_uuid = self.test_config.get("VLDBLLA", "FS_UUID")
        return

    def test_vos_addsite_remsite(self) :
        if not afs.CONFIG.enable_modifying_tests :
            raise unittest.SkipTest("modifying tests disabled.")
        self.vols_lla.create(self.tmp_volume)
        sp_ident = self.lla.addsite(self.tmp_volume, async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.assertTrue(res != None)
        self.eval_vos_addsite(res)

        sp_ident = self.lla.remsite(self.tmp_volume, async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.assertTrue(res != None)
        self.eval_vos_remsite(res)
        self.vols_lla.remove(self.tmp_volume)
        return

    def test_vos_lock_unlock(self) :
        self.vols_lla.create(self.tmp_volume)

        sp_ident = self.lla.lock(self.tmp_volume, async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_vos_lock(res)

        sp_ident = self.lla.unlock(self.tmp_volume, async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_vos_unlock(res)
        self.vols_lla.remove(self.tmp_volume)
        return

    def test_get_fileserver_uuid(self):
        sp_ident = self.lla.get_fileserver_uuid(self.fileserver_name, async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_get_fileserver_uuid(res)
        return

    def test_get_fileserver_list(self) :
        sp_ident = self.lla.get_fileserver_list(async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_get_fileserver_list(res)
        return

    def test_get_volume_list(self) :
        sp_ident = self.lla.get_volume_list(async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_get_volume_list(res)
        return

    def test_sync_vldb(self) :
        sp_ident = self.lla.sync_vldb(self.fileserver_name, async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_sync_vldb(res)
        return

    def test_sync_serv(self) :
        sp_ident = self.lla.sync_serv(self.fileserver_name, async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_sync_vldb(res)
        return

if __name__ == '__main__' :
    parse_commandline()
    sys.stderr.write("\n===\n=== testing direct fork ===\n===\n\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestVLDBLLAMethods)
    unittest.TextTestRunner(verbosity = 2).run(suite)
    sys.stderr.write("\n===\n=== testing detached execution ===\n===\n\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestVLDBLLAMethods_async)
    unittest.TextTestRunner(verbosity = 2).run(suite)
