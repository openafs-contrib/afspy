#!/usr/bin/env python

import unittest,logging
from BaseTest import parseCMDLine, basicTestSetup

from afs.dao import OSDFileServerDAO 
import afs

class TestOSDFileServerDAOMethods(unittest.TestCase, basicTestSetup):
    """
    Tests OSDFileServerDAO Methods
    """
    
    def setUp(self):
        """
        setup
        """
        basicTestSetup.setUp(self)
        self.FS=self.TestCfg.get("OSDFileServerDAO","FS")
        self.Part=self.TestCfg.get("OSDFileServerDAO","Part")
        self.allParts=self.TestCfg.get("OSDFileServerDAO","allParts")
        
        self.DAO = OSDFileServerDAO.OSDFileServerDAO()
        return
    
    def test_getVolList(self) :
        VolList=self.DAO.getVolList(self.FS,self.Part,_cfg=afs.CONFIG,_user="test")
        # this is somewhat silly, but what can you do ?
        # maybe check structure of result ?
        self.assertTrue(len(VolList)> 100)
        return
        
    def test_getIdVolList(self) :
        self.DAO.Logger.setLevel(logging.DEBUG)
        IdVolList=self.DAO.getIdVolList(self.FS,self.Part,_cfg=afs.CONFIG,_user="test")
        self.DAO.Logger.setLevel(logging.WARN)
        # this is somewhat silly, but what can you do ?
        # maybe check structure of result ?
        self.assertTrue(len(IdVolList)> 100)
        return

    def test_getPartList(self,) :
        PartList=self.DAO.getPartList(self.FS,_cfg=afs.CONFIG,_user="test")
        for p in PartList :
           if not p["name"] in self.allParts :
                self.assertEqual(p,"Not in Test.cfg")
        return
    
if __name__ == '__main__' :
    parseCMDLine()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestOSDFileServerDAOMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
