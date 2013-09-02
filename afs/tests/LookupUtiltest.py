#!/usr/bin/env python

import unittest
import logging
from BaseTest import parseCMDLine, basicTestSetup
import afs



class TestLookupUtilMethods(unittest.TestCase, basicTestSetup):
    """
    Tests LookupUtil Methods
    """
    
    def setUp(self):
        """
        setup
        """
        basicTestSetup.setUp(self)

        self.HostAlias=self.TestCfg.get("LookupUtil","HostAlias")
        self.primaryHostName=self.TestCfg.get("LookupUtil","primaryHostName")
        self.IPAddr=self.TestCfg.get("LookupUtil","IPAddr")
        self.FsUUID=self.TestCfg.get("LookupUtil","FsUUID")
        return

    def test_Lookup_HostAlias(self) :
        DNSInfo=afs.LookupUtil[afs.CONFIG.cell].getDNSInfo(self.HostAlias)
        self.assertEqual(self.primaryHostName,DNSInfo["names"][0])
        return

    def test_Lookup_UUID(self) :
        uuid=afs.LookupUtil[afs.CONFIG.cell].getFSUUID(self.HostAlias)
        self.assertEqual(self.FsUUID,uuid)
        return

    def test_Lookup_HostnameByFSUUID(self) :
        afs.LookupUtil[afs.CONFIG.cell].Logger.setLevel(logging.DEBUG)
        hostname=afs.LookupUtil[afs.CONFIG.cell].getHostnameByFSUUID(self.FsUUID)
        afs.LookupUtil[afs.CONFIG.cell].Logger.setLevel(logging.WARN)
        self.assertEqual(self.primaryHostName,hostname)
        return



if __name__ == '__main__' :
    parseCMDLine()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLookupUtilMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
