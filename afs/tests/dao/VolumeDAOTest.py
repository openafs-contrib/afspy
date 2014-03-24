#!/usr/bin/env python

"""
Unittest for the DAO module VolumeDAO
"""
import unittest
from afs.tests.BaseTest import parse_commandline, BasicTestSetup
import afs.dao.VolumeDAO 
import afs

class TestVolumeDAOMethods(unittest.TestCase, BasicTestSetup):
    """
    Tests VolumeDAO Methods
    """
    
    def setUp(self):
        """
        setup
        """
        self.dao = afs.dao.VolumeDAO.VolumeDAO()
        BasicTestSetup.__init__(self, self.dao, ignore_classes = \
            [afs.dao.BaseDAO.BaseDAO])
        self.fileserver = self.test_config.get("VolumeDAO", "FS")
        self.part = self.test_config.get("VolumeDAO", "Part")
        self.volume = afs.model.Volume.Volume()
        self.volume.vid = int(self.test_config.get("VolumeDAO", "VolID"))
        self.num_volumes = int(self.test_config.get("VolumeDAO", "numVols"))
        return
    
    def test_pull_volumes(self) :
        """
        test filling in a Volume object
        """
        volumes = self.dao.pull_volumes(self.volume, _cfg = afs.CONFIG)
        self.assertEqual(volumes[0].vid, self.volume.vid)
        return

if __name__ == '__main__' :
    parse_commandline()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestVolumeDAOMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
