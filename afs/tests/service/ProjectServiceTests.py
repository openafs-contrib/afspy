#!/usr/bin/env python

import sys
import time
import unittest
from ConfigParser import ConfigParser

from afs.service.ProjectService import ProjectService
from afs.tests.BaseTest import parse_commandline
import afs

class TestProjectServiceCachedMethods(unittest.TestCase):
    """
    Tests ProjectService getter Methods
    """
    @classmethod
    def setUpClass(self):
        """
        setup ProjectService
        """
        sys.stderr.write("\nsetUpClass\n")
        self.PrjMng = ProjectService()
        self.test_config = ConfigParser()
        self.test_config.read(afs.CONFIG.setup)
        self.ProjectName = self.test_config.get("ProjectService", "ProjectName")
        self.ProjectDescription = self.test_config.get("ProjectService", "ProjectDescription")
        self.ProjectServerPart = tuple(self.test_config.get("ProjectService", "ServerPart").split(","))
        sys.stderr.write("ProjectName: %s\n" % self.ProjectName)
        if self.PrjMng.get_project_by_name(self.ProjectName) != None :
            sys.stderr.write("Test-project of name already exists!\n")
            sys.stderr.write("cleanup the mess yourself.\n")
            sys.exit(1)
        self.Prj = self.PrjMng.create_project(self.ProjectName, self.ProjectDescription)
        return    

    @classmethod
    def tearDownClass(self) :
        """
        cleanup
        """
        sys.stderr.write("\ntearDownClass\n")
        #self.PrjMng.delete_project(self.Prj)
        return

    def test_get_project_by_name(self) :
        Prj = self.PrjMng.get_project_by_name(self.ProjectName)
        #sys.stderr.write("\nPrj=%s\n" % Prj)
        self.assertTrue( type(Prj) != type(None) )

    def test_add_remove_server_partitions(self) :
        Prj = self.PrjMng.add_server_partition(self.Prj, self.ProjectServerPart, "RW") 
        rw_serverparts, ro_serverparts = self.PrjMng.get_server_partitions(Prj)
        self.assertEqual(rw_serverparts, [self.ProjectServerPart])
        Prj = self.PrjMng.remove_server_partition(self.Prj, self.ProjectServerPart, "RW") 
        rw_serverparts, ro_serverparts = self.PrjMng.get_server_partitions(Prj)
        self.assertEqual(rw_serverparts, [])

    def test_set_remove_parent(self) :
        parent_project = self.PrjMng.create_project("parent_of_%s" % self.ProjectName, "test-parent")
        #sys.stderr.write("\nparent.db_id=%s\n" % parent_project.db_id)
        Prj = self.PrjMng.set_parent(self.Prj, parent_project)
        #sys.stderr.write("\nparent_db_id=%s\n" % Prj.parent_db_id)
        other_parent = self.PrjMng.get_parent(self.Prj)
        self.assertEqual(parent_project.db_id, other_parent.db_id)
        self.PrjMng.remove_parent(Prj) 
        other_parent = self.PrjMng.get_parent(self.Prj)
        self.assertEqual(other_parent, None)

    def test_add_remove_location(self) :
        Prj = self.PrjMng.add_location(self.Prj, self.ProjectName, "RW")   
        self.assertEqual(Prj.rw_locations, [self.ProjectName])
        Prj = self.PrjMng.remove_location(Prj, self.ProjectName, "RW")
        self.assertEqual(Prj.rw_locations, [])

    def test_set_owner(self) :
        Prj = self.PrjMng.set_owner(self.Prj, self.ProjectName)   
        other_prj = self.PrjMng.get_project_by_name(self.Prj.name)
        self.assertEqual(other_prj.owner, self.ProjectName) 

if __name__ == '__main__' :
    parse_commandline()
    sys.stderr.write("Testing methods accessing DB_CACHE\n")
    sys.stderr.write("====================================\n")
    PrjMng = ProjectService()
    if afs.CONFIG.DB_CACHE :
        suite = unittest.TestLoader().loadTestsFromTestCase(TestProjectServiceCachedMethods)
        unittest.TextTestRunner(verbosity=2).run(suite)
    else :
        sys.stderr.write("Skipped, because DB_CACHE is disabled.\n")
