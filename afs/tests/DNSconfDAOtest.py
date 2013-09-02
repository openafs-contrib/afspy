#!/usr/bin/env python
"""
unit test for retrieving AFS-cell configuration from DNS
"""

import unittest
from afs.tests.BaseTest import parse_commandline, BasicTestSetup
from afs.dao import DNSconfDAO
import afs

class TestDNSconfDAO(unittest.TestCase, BasicTestSetup) :
    """
    Tests DNSconfDAO Methods
    """

    def setUp(self):
        """
        setup
        """
        BasicTestSetup.__init__(self)
        self.dao = DNSconfDAO.DNSconfDAO()
        return

    def test_get_db_serverlist(self):
        """
        test the retrieval of all afs database servers from DNS
        for a given cell.
        """
        db_serverlist = self.dao.get_db_serverlist( _user = "test", \
            _cfg = afs.CONFIG)
        db_serverlist.sort()
        self.assertEqual(db_serverlist, self.all_dbservers)
        return

if __name__ == '__main__' :
    parse_commandline()
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestDNSconfDAO)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
