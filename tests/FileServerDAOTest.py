#!/usr/bin/env python

import unittest
import sys, os
from ConfigParser import ConfigParser

sys.path.append("..")

from afs.util.AfsConfig import AfsConfig, setupDefaultConfig
from afs.util.options import define, options
from afs.dao import FileServerDAO 
import afs

class TestFileServerDAOMethods(unittest.TestCase):
    """
    Tests FileServerDAO Methods
    """
    
    def setUp(self):
        """
        setup
        """
        self.DAO = FileServerDAO.FileServerDAO()
        self.TestCfg=ConfigParser()
        self.TestCfg.read(options.setup)
        self.Cell=self.TestCfg.get("general", "Cell").lower()
        self.User=self.TestCfg.get("general", "User")
        self.Pass=self.TestCfg.get("general", "Pass")
        self.FS=self.TestCfg.get("FileServerDAO","FS")
        self.Part=self.TestCfg.get("FileServerDAO","Part")
        self.allParts=self.TestCfg.get("FileServerDAO","allParts")
        return
    
    def test_getVolList(self) :
        VolList=self.DAO.getVolList(self.FS,self.Part,self.Cell,None)
        for v in VolList :
            if v["vid"] == 1108623471 :
                sys.stderr.write("\nV=%s" % v)
        return
        
    def test_getIdVolList(self) :
        IdVolList=self.DAO.getIdVolList(self.FS,self.Part,self.Cell,None)
        sys.stderr.write("\nIdVolList=%s" % IdVolList)
        return

    def test_getPartList(self,) :
        PartList=self.DAO.getPartList(self.FS,self.Cell,None)
        for p in PartList :
           if not p["part"] in self.allParts :
                self.assertEqual(p["part"],"Not in Test.cfg")
        return
    
if __name__ == '__main__' :
    define("setup", default="./Test.cfg", help="path to Testconfig")
    setupDefaultConfig()
    if not os.path.exists(options.setup) :
        sys.stderr.write("Test setup file %s does not exist.\n" % options.setup)
        sys.exit(2)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFileServerDAOMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
