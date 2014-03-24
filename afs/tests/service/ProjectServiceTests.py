#!/usr/bin/env python

import unittest

import afs,sys
from afs.service.ProjectService import ProjectService

from BaseTest import parse_commandline, BasicTestSetup

class SetupTest(BasicTestSetup) :
    """
    Tests ProjectService Methods
    """
    
    def setUp(self):
        """
        setup ProjectService
        """
        BasicTestSetup.setUp(self)
        self.PrjMng = ProjectService()
        self.ProjectName=self.TestCfg.get("ProjectService", "ProjectName")
        self.ProjectID=self.TestCfg.get("ProjectService", "ProjectID")
        self.ProjectIDs=self.TestCfg.get("ProjectService", "ProjectIDs")
        return    

class TestProjectServiceCachedMethods(unittest.TestCase, SetupTest):
    """
    Tests ProjectService getter Methods
    """
    def setUp(self):
        return SetupTest.setUp(self) 

    def test_getProjectByName(self) :
        Prj = self.PrjMng.getProjectByName(self.ProjectName)
        self.assertTrue( type(Prj) != type(None) )

if __name__ == '__main__' :
    parse_commandline()
    sys.stderr.write("Testing  methods accessing DB_CACHE\n")
    sys.stderr.write("====================================\n")
    if afs.CONFIG.DB_CACHE :
        suite = unittest.TestLoader().loadTestsFromTestCase(TestProjectServiceCachedMethods)
        unittest.TextTestRunner(verbosity=2).run(suite)
    else :
        sys.stderr.write("Skipped, because DB_CACHE is disabled.\n")
