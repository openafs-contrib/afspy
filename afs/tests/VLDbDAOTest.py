#!/usr/bin/env python

import unittest,sys
from BaseTest import parseCMDLine, basicTestSetup

import afs
from afs.dao import VLDbDAO

class TestVLDbDAOMethods(unittest.TestCase, basicTestSetup):
    """
    Tests FileServerDAO Methods
    """
    
    def setUp(self):
        """
        setup
        """
        basicTestSetup.setUp(self)
        self.cellname=self.TestCfg.get("general","Cell")
        self.numServ=int(self.TestCfg.get("VLDbDAO","numServ"))
        self.DAO = VLDbDAO.VLDbDAO()
        return
    
    def test_getVolList(self) :
        ServList=self.DAO.getFsServList(_cfg=afs.CONFIG, _user="test")
        self.assertTrue(len(ServList) > self.numServ)
        return
        
if __name__ == '__main__' :
    parseCMDLine()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestVLDbDAOMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
