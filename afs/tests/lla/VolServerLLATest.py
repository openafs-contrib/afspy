#!/usr/bin/env python

"""
Unittest for the LLA module VolumeLLA
"""

from ConfigParser import ConfigParser
import datetime
import os
import sys
import time
import unittest

from afs.tests.BaseTest import parse_commandline
import afs.lla.VolServerLLA 
import afs

class EvaluateTestResults(unittest.TestCase) :
    """
    evaluate results
    """

    def eval_vos_examine(self, res) :
        self.assertEqual(res.vid, self.volume.vid) 
        self.assertEqual(res.servername, self.volume.servername) 
        self.assertEqual(res.partition, self.volume.partition) 
        return

    def eval_vos_move(self, res) :
        self.assertEqual(res, True)
        return

    def eval_vos_release(self, res, res_ro, before_date) :
        self.assertEqual(res, True)
        self.assertTrue(res_ro.creation_date >= before_date)
        return

    def eval_vos_set_blockquota(self, res) :
        self.assertEqual(res, True)
        return

    def eval_vos_dump(self, res) :
        self.assertEqual(res, True)
        return

    def eval_vos_restore(self, res) :
        self.assertEqual(res, self.tmp_volume)
        return

    def eval_vos_convert(self, res) :
        self.assertEqual(res, True)
        return

    def eval_vos_create(self, res) :
        self.assertEqual(res, True)
        return

    def eval_vos_remove(self, res) :
        self.assertEqual(res, True)
        return


class TestVolServerLLAMethods(EvaluateTestResults) :
    """
    Tests VolumeLLA Methods
    """

    @classmethod
    def setUpClass(self) :
        """
        setup test environment
        called automagically
        """
        self.lla = afs.lla.VolServerLLA.VolServerLLA()
        self.test_config = ConfigParser()
        self.test_config.read(afs.CONFIG.setup)
        self.fileserver = self.test_config.get("VolServerLLA", "FS")
        self.part = self.test_config.get("VolServerLLA", "Part")
        self.volume = afs.model.Volume.Volume()
        self.volume.vid = int(self.test_config.get("VolServerLLA", "VolID"))
        self.volume.servername = self.test_config.get("VolServerLLA", "FS")
        self.volume.partition = self.test_config.get("VolServerLLA", "Part")
        self.ro_volume = afs.model.Volume.Volume()
        self.ro_volume.vid = int(self.test_config.get("VolServerLLA", "ROVolID"))
        self.ro_volume.servername = self.test_config.get("VolServerLLA", "FS")
        self.ro_volume.partition = self.test_config.get("VolServerLLA", "Part")
        self.dump_file = self.test_config.get("VolServerLLA", "DumpFile")
        self.tmp_volume = afs.model.Volume.Volume()
        self.tmp_volume.name = self.test_config.get("VolServerLLA", "TmpVolName")
        self.tmp_volume.servername = self.volume.servername
        self.tmp_volume.partition = self.volume.partition
        return

    def test_vos_examine(self) :
        res = self.lla.examine(self.volume)
        self.eval_vos_examine(res) 
        return
   
    def test_vos_dump_restore_remove(self) :
        if not afs.CONFIG.enable_modifying_tests :
            raise unittest.SkipTest("modifying tests disabled.")
        res = self.lla.dump(self.volume, self.dump_file)
        self.eval_vos_dump(res)
        res = self.lla.restore(self.tmp_volume, self.dump_file)
        self.eval_vos_restore(res)
        os.unlink(self.dump_file)
        res = self.lla.remove(self.tmp_volume)
        self.eval_vos_remove(res)
        return

    def test_vos_create_remove(self) :
        if not afs.CONFIG.enable_modifying_tests :
            raise unittest.SkipTest("modifying tests disabled.")
        res = self.lla.create(self.tmp_volume)
        self.eval_vos_create(res)
        res = self.lla.remove(self.tmp_volume)
        self.eval_vos_remove(res)
        return

    def test_vos_release(self) :
        if not afs.CONFIG.enable_modifying_tests :
            raise unittest.SkipTest("modifying tests disabled.")
        before_date = datetime.datetime.now()
        # before_date has a higher resolution than creation_date of the ro.
        # thus we need to wait to make sure before_Dat is smaller.
        time.sleep(1)
        res = self.lla.release(self.volume)
        res_ro = self.lla.examine(self.ro_volume)
        self.eval_vos_release(res, res_ro, before_date)
        return

class TestVolServerLLAMethods_async(EvaluateTestResults):
    """
    Tests VolServerLLA Methods
    """

    @classmethod
    def setUpClass(self) :
        """
        setup test environment
        called automagically
        """
        self.lla = afs.lla.VolServerLLA.VolServerLLA()
        self.test_config = ConfigParser()
        self.test_config.read(afs.CONFIG.setup)
        self.fileserver = self.test_config.get("VolServerLLA", "FS")
        self.part = self.test_config.get("VolServerLLA", "Part")
        self.dump_file = self.test_config.get("VolServerLLA", "DumpFile")
        self.volume = afs.model.Volume.Volume()
        self.volume.vid = int(self.test_config.get("VolServerLLA", "VolID"))
        self.volume.servername = self.test_config.get("VolServerLLA", "FS")
        self.volume.partition = self.test_config.get("VolServerLLA", "Part")
        self.ro_volume = afs.model.Volume.Volume()
        self.ro_volume.vid = int(self.test_config.get("VolServerLLA", "ROVolID"))
        self.ro_volume.servername = self.test_config.get("VolServerLLA", "FS")
        self.ro_volume.partition = self.test_config.get("VolServerLLA", "Part")
        self.tmp_volume = afs.model.Volume.Volume()
        self.tmp_volume.name = self.test_config.get("VolServerLLA", "TmpVolName")
        self.tmp_volume.servername = self.volume.servername
        self.tmp_volume.partition = self.volume.partition
        return

    def test_vos_examine(self) :
        sp_ident = self.lla.examine(self.volume, async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_vos_examine(res) 
        return

    def test_vos_dump_restore_remove(self) :
        if not afs.CONFIG.enable_modifying_tests :
            raise unittest.SkipTest("modifying tests disabled.")
        sp_ident = self.lla.dump(self.volume, self.dump_file, async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_vos_dump(res)
        sp_ident = self.lla.restore(self.tmp_volume, self.dump_file, async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_vos_restore(res)
        os.unlink(self.dump_file)
        sp_ident = self.lla.remove(self.tmp_volume, async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_vos_remove(res)
        return

    def test_vos_create_remove(self) :
        if not afs.CONFIG.enable_modifying_tests :
            raise unittest.SkipTest("modifying tests disabled.")
        sp_ident = self.lla.create(self.tmp_volume, async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_vos_create(res)
        sp_ident = self.lla.remove(self.tmp_volume, async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_vos_remove(res)
        return

    def test_vos_release(self) :
        if not afs.CONFIG.enable_modifying_tests :
            raise unittest.SkipTest("modifying tests disabled.")
        before_date = datetime.datetime.now()
        # before_date has a higher resolution than creation_date of the ro.
        # thus we need to wait to make sure before_Dat is smaller.
        time.sleep(1)
        sp_ident = self.lla.release(self.volume, async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        sp_ident = self.lla.examine(self.ro_volume, async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res_ro = self.lla.get_subprocess_result(sp_ident)
        self.eval_vos_release(res, res_ro, before_date)
        return

if __name__ == '__main__' :
    parse_commandline()
    sys.stderr.write("\n===\n=== testing direct fork ===\n===\n\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestVolServerLLAMethods)
    unittest.TextTestRunner(verbosity = 2).run(suite)
    sys.stderr.write("\n===\n=== testing detached execution ===\n===\n\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestVolServerLLAMethods_async)
    unittest.TextTestRunner(verbosity = 2).run(suite)
