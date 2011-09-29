#!/usr/bin/env python

import unittest
import sys
from ConfigParser import ConfigParser

sys.path.append("..")

from afs.model.AfsConfig import AfsConfig
from afs.service.VolService import VolService
from afs.model.Token import Token
from TestConfig import TestConfig


class TestVolServiceMethods(unittest.TestCase):
    """
    Tests VolService Methods
    """
        
    def setUp(self):
        """
        setup token and VolService
        """
        self.TestCfg=ConfigParser()
        self.TestCfg.read("tests.cfg")
        self.Cell=self.TestCfg.get("general", "Cell")
        self.User=self.TestCfg.get("general", "User")
        self.Pass=self.TestCfg.get("general", "Pass")
        token = Token(self.User, self.Pass, self.Cell)
        self.volMng = VolService(token)
        self.VolID=self.TestCfg.get("VolService", "VolID")
        self.VolName=self.TestCfg.get("VolService", "VolName")
        self.FS=self.TestCfg.get("VolService", "FS")
        self.Part=self.TestCfg.get("VolService", "Part")
        return
    
    def test_getVolbyName(self) :
        vol = self.volMng.getVolByName(self.VolName)
        self.assertEqual(vol.vid, self.VolID)
        self.assertEqual(vol.serv, self.FS)
        self.assertEqual(vol.part, self.Part)
        return
        
    def test_getVolbyID(self) :
        vol = self.volMng.getVolByID(self.VolID)
        self.assertEqual(vol.name, self.VolName)
        self.assertEqual(vol.serv, self.FS)
        self.assertEqual(vol.part, self.Part)
        return
    


if __name__ == '__main__' :
    suite = unittest.TestLoader().loadTestsFromTestCase(TestVolServiceMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
