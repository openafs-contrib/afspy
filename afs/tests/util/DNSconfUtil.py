#!/usr/bin/env python
"""
unit test for retrieving AFS-cell configuration from DNS
"""

import unittest
from afs.tests.BaseTest import parse_commandline, BasicTestSetup
import afs.lo.DNSconfUtil, afs.lo.BaseUtil
import afs

class TestDNSconf(unittest.TestCase, BasicTestSetup) :
    """
    Tests DNSconfDAO Methods
    """

    def setUp(self):
        """
        setup
        """
        self.lo = afs.lo.DNSconfUtil.DNSconfUtil()
        BasicTestSetup.__init__(self, self.lo, ignore_classes = [afs.util.Executor.Executor, afs.lo.BaseUtil.BaseUtil])
        return

    def test_get_db_serverlist(self):
        """
        test the retrieval of all afs database servers from DNS
        for a given cell.
        """
        db_serverlist = self.lo.get_db_serverlist(None, _cfg = afs.CONFIG)
        db_serverlist.sort()
        self.assertEqual(db_serverlist, self.all_dbservers)
        return

if __name__ == '__main__' :
    parse_commandline()
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestDNSconf)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
