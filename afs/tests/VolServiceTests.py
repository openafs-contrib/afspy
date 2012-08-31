#!/usr/bin/env python

import unittest,sys

import afs
from afs.service.VolService import VolService

from BaseTest import parseCMDLine, basicTestSetup

class SetupTest(basicTestSetup) :
    """
    Tests VolService Methods
    """
    
    def setUp(self):
        """
        setup VolService
        """
        basicTestSetup.setUp(self)
        self.volMng = VolService()
        self.VolID=int(self.TestCfg.get("VolService", "VolID"))
        self.VolName=self.TestCfg.get("VolService", "VolName")
        self.minCopy=int(self.TestCfg.get("VolService", "minCopy"))
        self.Owner=self.TestCfg.get("VolService", "Owner")
        self.FS=self.TestCfg.get("VolService", "FS")
        self.FSName=self.TestCfg.get("VolService", "FSName")
        self.Part=self.TestCfg.get("VolService", "Part")
        return    

class TestVolServiceSetMethods(unittest.TestCase, SetupTest):
    """
    Test VolService setter- and live- Methods
    """

    def setUp(self):
        return SetupTest.setUp(self) 

    def test_setExtendedVolumeAttributes(self):
        if not afs.defaultConfig.DB_CACHE :
            self.assertEqual(None, None)
            return
        volExtAttrDict={
                        "mincopy" : self.minCopy, 
                        "owner" : self.Owner, 
                        }
        thisExtVolAttr=self.volMng.setExtVolAttr(self.VolID, volExtAttrDict)
        self.assertEqual(thisExtVolAttr.mincopy, self.minCopy)
        self.assertEqual(thisExtVolAttr.owner, self.Owner)
        return
    
    def test_getVolbyName_live(self) :
        vol = self.volMng.getVolume(self.VolName, self.FS, self.Part, cached=False)
        self.assertEqual(vol.vid, self.VolID)
        self.assertEqual(vol.servername, self.FSName)
        self.assertEqual(vol.part, self.Part)
        return    
    


class TestVolServiceCachedMethods(unittest.TestCase, SetupTest):
    """
    Tests VolService getter Methods
    """
    def setUp(self):
        return SetupTest.setUp(self) 

    def test_getVolbyName_cached(self) :
        vol = self.volMng.getVolume(self.VolName, self.FS, self.Part, cached=True)
        self.assertEqual(vol.vid, self.VolID)
        self.assertEqual(vol.servername, self.FSName)
        self.assertEqual(vol.part, self.Part)
        return
    
    def test_getExtendedVolumeAttributes(self):
        volExt=self.volMng.getExtVolAttr(self.VolID)
        
        self.assertEqual(volExt.mincopy, self.minCopy)
        self.assertEqual(volExt.owner, self.Owner)
        return

if __name__ == '__main__' :
    parseCMDLine()
    sys.stderr.write("Testing live methods to fill DB_CACHE\n")
    sys.stderr.write("==============================\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestVolServiceSetMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
    sys.stderr.write("Testing  methods accessing DB_CACHE\n")
    sys.stderr.write("================================\n")
    if afs.defaultConfig.DB_CACHE :
        suite = unittest.TestLoader().loadTestsFromTestCase(TestVolServiceCachedMethods)
        unittest.TextTestRunner(verbosity=2).run(suite)
    else :
        sys.stderr.write("Skipped,  because DB_CACHE is disabled.\n")
