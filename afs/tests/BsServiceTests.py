#!/usr/bin/env python

import unittest, sys
from BaseTest import parseCMDLine, basicTestSetup

from afs.service.BsService import BsService
import afs

class SetupTest(basicTestSetup) :
    """
    setup TestBs config
    """
    
    def setUp(self):
        """
        setup VolService
        """
        basicTestSetup.setUp(self)
        self.BsName=self.TestCfg.get("BsService", "BS")
        self.BNodes=self.TestCfg.get("BsService", "BNodes").split(",")
        self.BsMng = BsService()
        return    


class TestBsServiceSetMethods(unittest.TestCase, SetupTest):
    """
    Tests BsService Methods
    """
    
    def setUp(self):
        """
        setup BsService
        """
        SetupTest.setUp(self)
        return

    def test_setRestartTimes(self):
        restartTime = self.BsMng.setRestartTimes(self.BsName,"never","general")
        self.assertEqual(None,restartTime)
        restartTime = self.BsMng.setRestartTimes(self.BsName,"never","binary")
        self.assertEqual(None,restartTime)
        return
        
    def test_getRestartTimes(self):
        TimesDict = self.BsMng.getRestartTimes(self.BsName)
        self.assertEqual("never",TimesDict["general"])
        self.assertEqual("never",TimesDict["binary"])
        return
        
class TestBsServiceCachedMethods(unittest.TestCase, SetupTest):
    """
    Tests BsService Methods
    """
    
    def setUp(self):
        """
        setup token and BsService
        """
        SetupTest.setUp(self)
        return

    def test_getServerObj(self) :
        server=self.BsMng.getFileServer(self.BsName, cached=True)
        parts= server.parts.keys()
        parts.sort()
        self.assertEqual(self.BsPartitions, parts)
        return



if __name__ == '__main__' :
    parseCMDLine()
    sys.stderr.write("Testing live methods to fill DB_CACHE\n")
    sys.stderr.write("==============================\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBsServiceSetMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
    sys.stderr.write("Testing  methods accessing DB_CACHE\n")
    sys.stderr.write("================================\n")
    if afs.CONFIG.DB_CACHE :
        suite = unittest.TestLoader().loadTestsFromTestCase(TestBsServiceCachedMethods)
        unittest.TextTestRunner(verbosity=2).run(suite)
    else :
         sys.stderr.write("Skipped,  because DB_CACHE is disabled.\n")
