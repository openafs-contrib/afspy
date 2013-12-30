#!/usr/bin/env python

import unittest,sys

import afs
from afs.service.VolService import VolService

from BaseTest import parse_commandline, BasicTestSetup

class SetupTest(BasicTestSetup) :
    """
    Tests VolService Methods
    """
    
    def setUp(self):
        """
        setup VolService
        """
        BasicTestSetup.__init__(self)
        self.volMng = VolService()
        self.VolID=int(self.test_config.get("VolService", "VolID"))
        self.VolName=self.test_config.get("VolService", "VolName")
        self.minCopy=int(self.test_config.get("VolService", "minCopy"))
        self.Owner=self.test_config.get("VolService", "Owner")
        self.FS=self.test_config.get("VolService", "FS")
        self.FSName=self.test_config.get("VolService", "FSName")
        self.Part=self.test_config.get("VolService", "Part")
        return    

class TestVolServiceSetMethods(unittest.TestCase, SetupTest):
    """
    Test VolService setter- and live- Methods
    """

    def setUp(self):
        return SetupTest.setUp(self) 

    def test_getVolbyName_live(self) :
        vol = self.volMng.get_volume(self.VolName, self.FS, self.Part, cached=False)
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
        vol = self.volMng.get_volume(self.VolName, self.FS, self.Part, cached=True)
        self.assertEqual(vol.vid, self.VolID)
        self.assertEqual(vol.servername, self.FSName)
        self.assertEqual(vol.part, self.Part)
        return
    
if __name__ == '__main__' :
    parse_commandline()
    sys.stderr.write("Testing live methods to fill DB_CACHE\n")
    sys.stderr.write("==============================\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestVolServiceSetMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
    sys.stderr.write("Testing  methods accessing DB_CACHE\n")
    sys.stderr.write("================================\n")
    if afs.CONFIG.DB_CACHE :
        suite = unittest.TestLoader().loadTestsFromTestCase(TestVolServiceCachedMethods)
        unittest.TextTestRunner(verbosity=2).run(suite)
    else :
        sys.stderr.write("Skipped,  because DB_CACHE is disabled.\n")
