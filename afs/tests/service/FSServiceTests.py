#!/usr/bin/env python

import unittest, sys
from BaseTest import parse_commandline, BasicTestSetup

from afs.service.FsService import FsService
import afs

class SetupTest(BasicTestSetup) :
    """
    setup TestFs config
    """
    
    def setUp(self):
        """
        setup VolService
        """
        BasicTestSetup.__init__(self)
        self.FsName=self.test_config.get("FsService", "FS")
        self.FsPartitions=self.test_config.get("FsService", "Partitions").split(",")
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
    parse_commandline()
    sys.stderr.write("Testing live methods to fill DB_CACHE\n")
    sys.stderr.write("==============================\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFsServiceSetMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
    sys.stderr.write("Testing  methods accessing DB_CACHE\n")
    sys.stderr.write("================================\n")
    if afs.CONFIG.DB_CACHE :
        suite = unittest.TestLoader().loadTestsFromTestCase(TestFsServiceCachedMethods)
        unittest.TextTestRunner(verbosity=2).run(suite)
    else :
         sys.stderr.write("Skipped,  because DB_CACHE is disabled.\n")
