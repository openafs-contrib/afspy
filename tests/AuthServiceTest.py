#!/usr/bin/env python

import unittest
import sys, os
from ConfigParser import ConfigParser

sys.path.append("..")

from afs.util.AfsConfig import  setupDefaultConfig
from afs.util.options import define, options
from afs.service import AuthService
import afs

class TestAuthServiceMethods(unittest.TestCase):
    """
    Tests VolService Methods
    """
    
    def setUp(self):
        """
        setup
        """
        self.AuthService = AuthService.AuthService()
        self.TestCfg=ConfigParser()
        self.TestCfg.read(options.setup)
        self.Cell=self.TestCfg.get("general", "Cell").lower()
        self.User=self.TestCfg.get("general", "User")
        self.Pass=self.TestCfg.get("general", "Pass")
        return
    
    def test_getTokenFromPAG(self) :
        afs.defaultConfig.CRED_TYPE="pag"
        token=self.AuthService.getToken()
        self.assertEqual(self.Cell, token._CELL_NAME)
        return

    def test_get_artificialToken(self) :
        token=self.AuthService.get_artificial_Token(123,"openafs.org")
        self.assertEqual("openafs.org",token._CELL_NAME)
        self.assertEqual(123,token._AFS_ID)
        return
        
    def test_getTokenFromPassword(self):
        afs.defaultConfig.CRED_TYPE="krb5_password"
        token=self.AuthService.getToken()
        self.assertEqual(self.Cell, token._CELL_NAME)
        return
    
    def test_getTokenFromKeytab(self):
        afs.defaultConfig.CRED_TYPE="krb5_keytab:/home/hanke/private/keytab"
        token=self.AuthService.getToken()
        self.assertEqual(self.Cell, token._CELL_NAME)
        return
    
if __name__ == '__main__' :
    define("setup", default="./Test.cfg", help="path to Testconfig")
    setupDefaultConfig()
    if not os.path.exists(options.setup) :
        sys.stderr.write("Test setup file %s does not exist.\n" % options.setup)
        sys.exit(2)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAuthServiceMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
