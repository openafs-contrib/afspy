#!/usr/bin/env python

import unittest
from BaseTest import parseCMDLine, basicTestSetup

from afs.service import AuthService
import afs


global Krb5Principal,Krb5Keytab
Krb5Principal=""
Krb5Keytab=""

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
        Krb5Keytab=self.TestCfg.get("AuthService", "Krb5Keytab")
        Krb5Principal=self.TestCfg.get("AuthService", "Krb5Principal")
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
        
    @unittest.skipIf(len(Krb5Principal) == 0, "no Krb5 Principal given.")
    def test_getTokenFromPassword(self):
        afs.defaultConfig.CRED_TYPE="krb5_password"
        afs.defaultConfig.KRB5_PRINC=Krb5Principal
        token=self.AuthService.getToken()
        self.assertEqual(self.Cell, token.CELL_NAME)
        return
    
    @unittest.skipIf(len(Krb5Keytab) == 0, "no Krb5 Keytab given.")
    def test_getTokenFromKeytab(self):
        afs.defaultConfig.CRED_TYPE="krb5_keytab:%s" % self.Keytab
        token=self.AuthService.getToken()
        self.assertEqual(self.Cell, token.CELL_NAME)
        return
    
if __name__ == '__main__' :
    parseCMDLine()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAuthServiceMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
