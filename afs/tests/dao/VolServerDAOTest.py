#!/usr/bin/env python

"""
Unittest for the DAO module VolumeDAO
"""

from ConfigParser import ConfigParser
import sys
import unittest

from afs.tests.BaseTest import parse_commandline
import afs.dao.VolServerDAO 
import afs

class TestVolServerDAOMethods(unittest.TestCase):
    """
    Tests VolumeDAO Methods
    """

    @classmethod
    def setUpClass(self) :
        """
        setup test environment
        called automagically
        """
        self.dao = afs.dao.VolServerDAO.VolServerDAO()
        self.test_config = ConfigParser()
        self.test_config.read(afs.CONFIG.setup)
        self.fileserver = self.test_config.get("VolServerDAO", "FS")
        self.part = self.test_config.get("VolServerDAO", "Part")
        self.volume = afs.model.Volume.Volume()
        self.volume.vid = int(self.test_config.get("VolServerDAO", "VolID"))
        self.num_volumes = int(self.test_config.get("VolServerDAO", "numVols"))
        return
    
    def test_pull_volumes(self) :
        """
        test filling in a Volume object
        """
        volumes = self.dao.pull_volumes(self.volume, _cfg = afs.CONFIG)
        self.assertEqual(volumes[0].vid, self.volume.vid)
        return

class TestVolServerDAOMethods_async(unittest.TestCase):
    """
    Tests VolServerDAO Methods
    """

    @classmethod
    def setUpClass(self) :
        """
        setup test environment
        called automagically
        """
        self.dao = afs.dao.VolServerDAO.VolServerDAO()
        self.test_config = ConfigParser()
        self.test_config.read(afs.CONFIG.setup)
        self.fileserver = self.test_config.get("VolServerDAO", "FS")
        self.part = self.test_config.get("VolServerDAO", "Part")
        self.volume = afs.model.Volume.Volume()
        self.volume.vid = int(self.test_config.get("VolServerDAO", "VolID"))
        self.num_volumes = int(self.test_config.get("VolServerDAO", "numVols"))
        return
    
    def test_pull_volumes(self) :
        """
        test filling in a Volume object
        """
        sp_ident = self.dao.pull_volumes(self.volume, _cfg = afs.CONFIG, async = True)
        self.dao.wait_for_subprocess(sp_ident)
        volumes = self.dao.get_subprocess_result(sp_ident)
        self.assertEqual(volumes[0].vid, self.volume.vid)
        return

if __name__ == '__main__' :
    parse_commandline()
    sys.stderr.write("\n===\n=== testing direct fork ===\n===\n\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestVolServerDAOMethods)
    unittest.TextTestRunner(verbosity = 2).run(suite)
    sys.stderr.write("\n===\n=== testing detached execution ===\n===\n\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestVolServerDAOMethods_async)
    unittest.TextTestRunner(verbosity = 2).run(suite)
