#!/usr/bin/env python

"""
Unittest for the LLA module VolumeLLA
"""

from ConfigParser import ConfigParser
import sys
import unittest

from afs.tests.BaseTest import parse_commandline
import afs.lla.VolServerLLA 
import afs

class EvaluateTestResults(unittest.TestCase) :
    """
    evaluate results
    """

    def eval_examine(self, res) :
        self.assertEqual(res.vid, self.volume.vid) 
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
        self.num_volumes = int(self.test_config.get("VolServerLLA", "numVols"))
        return

    def test_vos_examine(self) :
        res = self.lla.examine(self.volume)
        self.eval_examine(res) 
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
        self.volume = afs.model.Volume.Volume()
        self.volume.vid = int(self.test_config.get("VolServerLLA", "VolID"))
        self.num_volumes = int(self.test_config.get("VolServerLLA", "numVols"))
        return

    def test_vos_examine(self) :
        sp_ident = self.lla.examine(self.volume, async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_examine(res) 
        return
    
if __name__ == '__main__' :
    parse_commandline()
    sys.stderr.write("\n===\n=== testing direct fork ===\n===\n\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestVolServerLLAMethods)
    unittest.TextTestRunner(verbosity = 2).run(suite)
    sys.stderr.write("\n===\n=== testing detached execution ===\n===\n\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestVolServerLLAMethods_async)
    unittest.TextTestRunner(verbosity = 2).run(suite)
