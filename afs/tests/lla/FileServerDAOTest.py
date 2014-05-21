#!/usr/bin/env python

import unittest

import afs
from afs.tests.BaseTest import parse_commandline, BasicTestSetup
from afs.lla import FileServerLLA

class TestFileServerLLAMethods(unittest.TestCase, BasicTestSetup):
    """
    Tests FileServerLLA Methods
    """
    
    def setUp(self):
        """
        setup
        """
        self.lla = afs.lla.FileServerLLA.FileServerLLA()
        BasicTestSetup.__init__(self, self.lla, ignore_classes = [afs.lla.BaseLLA.BaseLLA])
        self.FS=self.test_config.get("FileServerLLA","FS")
        self.Part=self.test_config.get("FileServerLLA","Part")
        self.allParts=self.test_config.get("FileServerLLA","allParts")
        return
    
    def test_getVolList(self) :
        VolList=self.lla.getVolList(self.FS, self.Part, _cfg=afs.CONFIG, _user="test")
        # this is somewhat silly, but what can you do ?
        # maybe check structure of result ?
        self.assertTrue(len(VolList) < 100)
        return
        
    def test_getIdVolList(self) :
        IdVolList=self.lla.getIdVolList(self.FS, self.Part, _cfg=afs.CONFIG, _user="test")
        # this is somewhat silly, but what can you do ?
        # maybe check structure of result ?
        self.assertTrue(len(IdVolList) < 100)
        return

    def test_getPartList(self,) :
        PartList=self.lla.getPartList(self.FS, _cfg=afs.CONFIG, _user="test")
        for p in PartList :
           if not p["name"] in self.allParts :
                self.assertEqual(p,"Not in Test.cfg")
        return
    
if __name__ == '__main__' :
    parse_commandline()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFileServerLLAMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
