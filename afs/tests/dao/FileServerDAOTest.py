#!/usr/bin/env python

import unittest

import afs
from afs.tests.BaseTest import parse_commandline, BasicTestSetup
from afs.dao import FileServerDAO

class TestFileServerDAOMethods(unittest.TestCase, BasicTestSetup):
    """
    Tests FileServerDAO Methods
    """
    
    def setUp(self):
        """
        setup
        """
        self.dao = afs.dao.FileServerDAO.FileServerDAO()
        BasicTestSetup.__init__(self, self.dao, ignore_classes = [afs.dao.BaseDAO.BaseDAO])
        self.FS=self.test_config.get("FileServerDAO","FS")
        self.Part=self.test_config.get("FileServerDAO","Part")
        self.allParts=self.test_config.get("FileServerDAO","allParts")
        return
    
    def test_getVolList(self) :
        VolList=self.dao.getVolList(self.FS, self.Part, _cfg=afs.CONFIG, _user="test")
        # this is somewhat silly, but what can you do ?
        # maybe check structure of result ?
        self.assertTrue(len(VolList) < 100)
        return
        
    def test_getIdVolList(self) :
        IdVolList=self.dao.getIdVolList(self.FS, self.Part, _cfg=afs.CONFIG, _user="test")
        # this is somewhat silly, but what can you do ?
        # maybe check structure of result ?
        self.assertTrue(len(IdVolList) < 100)
        return

    def test_getPartList(self,) :
        PartList=self.dao.getPartList(self.FS, _cfg=afs.CONFIG, _user="test")
        for p in PartList :
           if not p["name"] in self.allParts :
                self.assertEqual(p,"Not in Test.cfg")
        return
    
if __name__ == '__main__' :
    parse_commandline()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFileServerDAOMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
