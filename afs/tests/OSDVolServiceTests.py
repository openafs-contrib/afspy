#!/usr/bin/env python

import unittest

import afs,sys
from afs.service.OSDVolService import OSDVolService

from BaseTest import parseCMDLine, basicTestSetup

class SetupTest(basicTestSetup) :
    """
    Tests OSDVolService Methods
    """
    
    def setUp(self):
        """
        setup OSDVolService
        """
        basicTestSetup.setUp(self)
        self.volMng = OSDVolService()
        self.VolID=int(self.TestCfg.get("OSDVolService", "VolID"))
        self.FS=self.TestCfg.get("OSDVolService", "FS")
        self.FSName=self.TestCfg.get("OSDVolService", "FSName")
        self.Part=self.TestCfg.get("OSDVolService", "Part")
        return    

class TestOSDVolServiceCachedMethods(unittest.TestCase, SetupTest):
    """
    Tests OSDVolService getter Methods
    """
    def setUp(self):
        return SetupTest.setUp(self) 

    def test_getStorageUsage(self) :
        storUDict = self.volMng.getStorageUsage(self.FS,self.VolID)
        print storUDict["totals"]
        storUDict2 = self.volMng.getStorageUsage(self.FS,self.VolID,storUDict)
        print storUDict2["totals"]
        return
    
    def test_getOsdVolAttr(self):
        vol=self.volMng.getVolume(self.VolID,self.FS,self.Part)
        self.assertTrue(type(vol)!=type(None))
        return

if __name__ == '__main__' :
    parseCMDLine()
    sys.stderr.write("Testing  methods accessing DB_CACHE\n")
    sys.stderr.write("================================\n")
    if afs.defaultConfig.DB_CACHE :
        suite = unittest.TestLoader().loadTestsFromTestCase(TestOSDVolServiceCachedMethods)
        unittest.TextTestRunner(verbosity=2).run(suite)
    else :
        sys.stderr.write("Skipped,  because DB_CACHE is disabled.\n")
