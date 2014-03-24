#!/usr/bin/env python

import unittest
import logging
from BaseTest import parse_commandline, BasicTestSetup
import afs



class TestLookupUtilMethods(unittest.TestCase, BasicTestSetup):
    """
    Tests LookupUtil Methods
    """
    
    def setUp(self):
        """
        setup
        """
        BasicTestSetup.__init__(self)

        self.HostAlias=self.test_config.get("LookupUtil","HostAlias")
        self.primaryHostName=self.test_config.get("LookupUtil","primaryHostName")
        self.IPAddr=self.test_config.get("LookupUtil","IPAddr")
        self.FsUUID=self.test_config.get("LookupUtil","FsUUID")
        return

    def test_Lookup_HostAlias(self) :
        DNSInfo=afs.LOOKUP_UTIL[afs.CONFIG.cell].get_dns_info(self.HostAlias)
        self.assertEqual(self.primaryHostName,DNSInfo["names"][0])
        return

    def test_Lookup_UUID(self) :
        uuid=afs.LOOKUP_UTIL[afs.CONFIG.cell].get_fsuuid(self.HostAlias)
        self.assertEqual(self.FsUUID,uuid)
        return

    def test_Lookup_HostnameByFSUUID(self) :
        hostname=afs.LOOKUP_UTIL[afs.CONFIG.cell].get_hostname_by_fsuuid(self.FsUUID)
        self.assertEqual(self.primaryHostName,hostname)
        return



if __name__ == '__main__' :
    parse_commandline()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLookupUtilMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
