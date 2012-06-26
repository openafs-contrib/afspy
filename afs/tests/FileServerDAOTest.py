#!/usr/bin/env python

import unittest
from BaseTest import parseCMDLine, basicTestSetup

import afs
from afs.dao import FileServerDAO

class TestFileServerDAOMethods(unittest.TestCase, basicTestSetup):
    """
    Tests FileServerDAO Methods
    """
    
    def setUp(self):
        """
        setup
        """
        basicTestSetup.setUp(self)
        self.FS=self.TestCfg.get("FileServerDAO","FS")
        self.Part=self.TestCfg.get("FileServerDAO","Part")
        self.allParts=self.TestCfg.get("FileServerDAO","allParts")
        self.DAO = FileServerDAO.FileServerDAO()
        return
    
    def test_getVolList(self) :
        VolList=self.DAO.getVolList(self.FS,self.Part,self.Cell,None)
        # this is somewhat silly, but what can you do ?
        # maybe check structure of result ?
        self.assertTrue(len(VolList)> 100)
        return
        
    def test_getIdVolList(self) :
        IdVolList=self.DAO.getIdVolList(self.FS,self.Part,self.Cell,None)
        # this is somewhat silly, but what can you do ?
        # maybe check structure of result ?
        self.assertTrue(len(IdVolList)> 100)
        return

    def test_getPartList(self,) :
        PartList=self.DAO.getPartList(self.FS,self.Cell,None)
        for p in PartList :
           if not p["name"] in self.allParts :
                self.assertEqual(p,"Not in Test.cfg")
        return
    
if __name__ == '__main__' :
    parseCMDLine()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFileServerDAOMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
