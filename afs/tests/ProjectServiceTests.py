#!/usr/bin/env python

import unittest

import afs,sys
from afs.service.ProjectService import ProjectService

from BaseTest import parseCMDLine, basicTestSetup

class SetupTest(basicTestSetup) :
    """
    Tests ProjectService Methods
    """
    
    def setUp(self):
        """
        setup ProjectService
        """
        basicTestSetup.setUp(self)
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
        print Prj.id
        return

if __name__ == '__main__' :
    parseCMDLine()
    sys.stderr.write("Testing  methods accessing DB_CACHE\n")
    sys.stderr.write("====================================\n")
    if afs.defaultConfig.DB_CACHE :
        suite = unittest.TestLoader().loadTestsFromTestCase(TestProjectServiceCachedMethods)
        unittest.TextTestRunner(verbosity=2).run(suite)
    else :
        sys.stderr.write("Skipped, because DB_CACHE is disabled.\n")
