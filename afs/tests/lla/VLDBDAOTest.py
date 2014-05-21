#!/usr/bin/env python

import unittest,sys
from BaseTest import parse_commandline, BasicTestSetup

import afs
from afs.lla import VLDBLLA

class TestVLDbLLAMethods(unittest.TestCase, BasicTestSetup):
    """
    Tests FileServerLLA Methods
    """
    
    def setUp(self):
        """
        setup
        """
        BasicTestSetup.__init__(self)
        self.cellname=self.test_config.get("general","Cell")
        self.numServ=int(self.test_config.get("VLDbLLA","numServ"))
        self.LLA = VLDBLLA.VLDBLLA()
        return
    
    def test_getVolList(self) :
        ServList=self.LLA.getFsServList(_cfg=afs.CONFIG, _user="test")
        self.assertTrue(len(ServList) > self.numServ)
        return
        
if __name__ == '__main__' :
    parse_commandline()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestVLDbLLAMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
