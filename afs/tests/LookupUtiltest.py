#!/usr/bin/env python

import unittest
import logging
from BaseTest import parseCMDLine, basicTestSetup

from afs.util import afsutil


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
        self.LookupUtil = afsutil.LookupUtil()
        self.LookupUtil.Logger.setLevel(logging.DEBUG)
        return

    def test_Lookup(self) :
        DNSInfo=self.LookupUtil.getDNSInfo(self.HostAlias)
        self.assertEqual(self.primaryHostName,DNSInfo[0][0])
        return


if __name__ == '__main__' :
    parseCMDLine()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLookupUtilMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
