#!/usr/bin/env python

import unittest, sys
from BaseTest import parseCMDLine, basicTestSetup

sys.path.append("..")
from afs.service.FsService import FsService
import afs

class SetupTest(basicTestSetup) :
    """
    setup TestFs config
    """
    
    def setUp(self):
        """
        setup VolService
        """
        basicTestSetup.setUp(self)
        self.FsName=self.TestCfg.get("FsService", "FS")
        self.FsPartitions=self.TestCfg.get("FsService", "Partitions").split(",")
        self.FsPartitions.sort()
        self.FsMng = FsService()
        return    


class TestFsServiceSetMethods(unittest.TestCase, SetupTest):
    """
    Tests FsService Methods
    """
    
    def setUp(self):
        """
        setup token and FsService
        """
        SetupTest.setUp(self)
        return

    def test_setRestartTimes(self):
        restartTime = self.FsMng.setRestartTimes(self.FsName,"never","general")
        self.assertEqual(None,restartTime)
        restartTime = self.FsMng.setRestartTimes(self.FsName,"never","binary")
        self.assertEqual(None,restartTime)
        return
        
    def test_getRestartTimes(self):
        TimesDict = self.FsMng.getRestartTimes(self.FsName)
        self.assertEqual("never",TimesDict["general"])
        self.assertEqual("5:00 am",TimesDict["binary"])
        return
        
    def test_getServerObj(self) :
        server=self.FsMng.getFileServer(self.FsName, cached=False)
        parts=[]
        for p in server.parts :
            parts.append(server. parts[p]["name"])
        parts.sort()
        self.assertEqual(self.FsPartitions, parts)
        return

class TestFsServiceCachedMethods(unittest.TestCase, SetupTest):
    """
    Tests FsService Methods
    """
    
    def setUp(self):
        """
        setup token and FsService
        """
        SetupTest.setUp(self)
        return

    def test_getServerObj(self) :
        server=self.FsMng.getFileServer(self.FsName, cached=True)
        parts= server.parts.keys()
        parts.sort()
        self.assertEqual(self.FsPartitions, parts)
        return



if __name__ == '__main__' :
    parseCMDLine()
    sys.stderr.write("Testing live methods to fill DB_CACHE\n")
    sys.stderr.write("==============================\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFsServiceSetMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
    sys.stderr.write("Testing  methods accessing DB_CACHE\n")
    sys.stderr.write("================================\n")
    if afs.defaultConfig.DB_CACHE :
        suite = unittest.TestLoader().loadTestsFromTestCase(TestFsServiceCachedMethods)
        unittest.TextTestRunner(verbosity=2).run(suite)
    else :
         sys.stderr.write("Skipped,  because DB_CACHE is disabled.\n")
