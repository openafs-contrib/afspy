#!/usr/bin/env python

import unittest
from BaseTest import parseCMDLine, basicTestSetup
from afs.dao import DNSconfDAO
import afs

class TestDNSconfDAO(unittest.TestCase,basicTestSetup):
    """
    Tests DNSconfDAO Methods
    """

    def setUp(self):
        """
        setup
        """
        basicTestSetup.setUp(self)

        self.DAO = DNSconfDAO.DNSconfDAO()
        self.Cell=self.TestCfg.get("general","Cell")
        self.allDBServs=self.TestCfg.get("general","allDBServs").split(",")
        self.allDBServs.sort()
        return

    def test_getDBServList(self):
        DBServList=self.DAO.getDBServList(self.Cell, _cfg=afs.defaultConfig, _user="test")
        DBServList.sort()
        self.assertEqual(DBServList, self.allDBServs)
        return

if __name__ == '__main__' :
    parseCMDLine()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDNSconfDAO)
    unittest.TextTestRunner(verbosity=2).run(suite)
