#!/usr/bin/env python

import unittest
from BaseTest import parseCMDLine, basicTestSetup

from afs.service import AuthService
import afs


class TestAuthServiceMethods(unittest.TestCase, basicTestSetup):
    """
    Tests AuthService Methods
    """
    
    def setUp(self):
        """
        setup
        """
        basicTestSetup.setUp(self)
        self.AuthService = AuthService.AuthService()
        return
    
    def test_getTokenFromPAG(self) :
        afs.defaultConfig.CRED_TYPE="pag"
        token=self.AuthService.getToken()
        self.assertEqual(self.Cell, token.CELL_NAME)
        return

    def test_get_artificialToken(self) :
        token=self.AuthService.get_artificial_Token(123,"openafs.org")
        self.assertEqual("openafs.org",token.CELL_NAME)
        self.assertEqual(123,token.AFS_ID)
        return
        
    def test_getTokenFromPassword(self):
        afs.defaultConfig.CRED_TYPE="krb5_password"
        token=self.AuthService.getToken()
        self.assertEqual(self.Cell, token.CELL_NAME)
        return
    
    def test_getTokenFromKeytab(self):
        afs.defaultConfig.CRED_TYPE="krb5_keytab:/home/hanke/private/keytab"
        token=self.AuthService.getToken()
        self.assertEqual(self.Cell, token.CELL_NAME)
        return
    
if __name__ == '__main__' :
    parseCMDLine()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAuthServiceMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
