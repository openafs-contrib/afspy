#!/usr/bin/env python

import unittest,sys
from BaseTest import parse_commandline, BasicTestSetup

import afs
from afs.dao import VLDBDAO

class TestVLDbDAOMethods(unittest.TestCase, BasicTestSetup):
    """
    Tests FileServerDAO Methods
    """
    
    def setUp(self):
        """
        setup
        """
        BasicTestSetup.__init__(self)
        self.cellname=self.test_config.get("general","Cell")
        self.numServ=int(self.test_config.get("VLDbDAO","numServ"))
        self.DAO = VLDBDAO.VLDBDAO()
        return
    
    def test_getVolList(self) :
        ServList=self.DAO.getFsServList(_cfg=afs.CONFIG, _user="test")
        self.assertTrue(len(ServList) > self.numServ)
        return
        
if __name__ == '__main__' :
    parse_commandline()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestVLDbDAOMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
