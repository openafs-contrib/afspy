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

class TestVolServerLLAMethods(unittest.TestCase):
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
    
    def test_pull_volumes(self) :
        """
        test filling in a Volume object
        """
        volumes = self.lla.pull_volumes(self.volume, _cfg = afs.CONFIG)
        self.assertEqual(volumes[0].vid, self.volume.vid)
        return

class TestVolServerLLAMethods_async(unittest.TestCase):
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
    
    def test_pull_volumes(self) :
        """
        test filling in a Volume object
        """
        sp_ident = self.lla.pull_volumes(self.volume, _cfg = afs.CONFIG, async = True)
        self.lla.wait_for_subprocess(sp_ident)
        volumes = self.lla.get_subprocess_result(sp_ident)
        self.assertEqual(volumes[0].vid, self.volume.vid)
        return

if __name__ == '__main__' :
    parse_commandline()
    sys.stderr.write("\n===\n=== testing direct fork ===\n===\n\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestVolServerLLAMethods)
    unittest.TextTestRunner(verbosity = 2).run(suite)
    sys.stderr.write("\n===\n=== testing detached execution ===\n===\n\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestVolServerLLAMethods_async)
    unittest.TextTestRunner(verbosity = 2).run(suite)
