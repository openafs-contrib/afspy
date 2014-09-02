#!/usr/bin/env python

from ConfigParser import ConfigParser
import sys
import unittest

from afs.tests.BaseTest import parse_commandline
from afs.service.VolumeService import VolumeService
from afs.model.Volume import Volume
from afs.model.Historic import historic_Volume
from afs.util.DBManager import DBManager
import afs

class EvaluateTestResults(unittest.TestCase) :

    def eval_get_volume_by_name(self, res) :
        #sys.stderr.write("\n\n===================\n%s\n============================\n" % res)
        self.assertEqual(len(res), 1)
        self.assertTrue(isinstance(res[0], Volume))
        self.assertEqual(res[0].vid, self.VolID)
        self.assertEqual(res[0].servername, self.FSName)
        self.assertEqual(res[0].partition, self.Part)
        return

    def eval_get_volume_group_by_name(self, res) :
        #sys.stderr.write("\n\n===================\n%s\n============================\n" % res)
        self.assertTrue(isinstance(res["RW"], Volume))
        self.assertEqual(len(res["RO"]), 2)
        self.assertEqual(res["BK"], None)
        return

class TestVolServiceMethods(EvaluateTestResults) :
    """
    Test VolService setter- and live- Methods
    """

    @classmethod 
    def setUp(self):
        """
        setup VolService
        """
        self.test_config = ConfigParser()
        self.test_config.read(afs.CONFIG.setup)
        self.volMng = VolumeService()
        self.VolID = int(self.test_config.get("VolService", "VolID"))
        self.VolName = self.test_config.get("VolService", "VolName")
        self.minCopy = int(self.test_config.get("VolService", "minCopy"))
        self.Owner = self.test_config.get("VolService", "Owner")
        self.FS = self.test_config.get("VolService", "FS")
        self.FSName = self.test_config.get("VolService", "FSName")
        self.Part = self.test_config.get("VolService", "Part")
        return    

    def test_get_volume_by_name(self) :
        res = self.volMng.get_volume(self.VolName, cached=False)
        self.eval_get_volume_by_name(res)
        return    

    def test_get_volume_group_by_name(self) :
        res = self.volMng.get_volume_group(self.VolName, cached=False)
        self.eval_get_volume_group_by_name(res)
        return    
    
class TestVolServiceMethods_async(EvaluateTestResults) :
    """
    Test VolService setter- and live- Methods
    """

    @classmethod 
    def setUp(self):
        """
        setup VolService
        """
        self.test_config = ConfigParser()
        self.test_config.read(afs.CONFIG.setup)
        self.volMng = VolumeService()
        self.VolID = int(self.test_config.get("VolService", "VolID"))
        self.VolName = self.test_config.get("VolService", "VolName")
        self.minCopy = int(self.test_config.get("VolService", "minCopy"))
        self.Owner = self.test_config.get("VolService", "Owner")
        self.FS = self.test_config.get("VolService", "FS")
        self.FSName = self.test_config.get("VolService", "FSName")
        self.Part = self.test_config.get("VolService", "Part")
        return    

    def test_get_volume_by_name(self) :
        task_ident = self.volMng.get_volume(self.VolName, cached=False, async=True)
        self.volMng.wait_for_task(task_ident) 
        res = self.volMng.get_task_result(task_ident)
        self.eval_get_volume_by_name(res)
        return    

    def test_get_volume_group_by_name(self) :
        task_ident = self.volMng.get_volume_group(self.VolName, cached=False, async=True)
        self.volMng.wait_for_task(task_ident) 
        res = self.volMng.get_task_result(task_ident)
        self.eval_get_volume_group_by_name(res)
        return    
    
class TestVolServiceMethods_cached(EvaluateTestResults) :
    """
    Tests VolService getter Methods
    """

    @classmethod 
    def setUp(self):
        """
        setup VolService
        """
        self.test_config = ConfigParser()
        self.test_config.read(afs.CONFIG.setup)
        self.volMng = VolumeService()
        self.VolID = int(self.test_config.get("VolService", "VolID"))
        self.VolName = self.test_config.get("VolService", "VolName")
        self.minCopy = int(self.test_config.get("VolService", "minCopy"))
        self.Owner = self.test_config.get("VolService", "Owner")
        self.FS = self.test_config.get("VolService", "FS")
        self.FSName = self.test_config.get("VolService", "FSName")
        self.Part = self.test_config.get("VolService", "Part")
        return    

    def test_get_volume_by_name(self) :
        res = self.volMng.get_volume(self.VolName, cached=True)
        self.eval_get_volume_by_name(res)
        return    

    def test_get_volume_group_by_name(self) :
        res = self.volMng.get_volume_group(self.VolName, cached=True)
        self.eval_get_volume_group_by_name(res)
        return    
    
class TestVolServiceMethods_cached_async(EvaluateTestResults) :
    """
    Tests VolService getter Methods
    """

    @classmethod 
    def setUp(self):
        """
        setup VolService
        """
        self.test_config = ConfigParser()
        self.test_config.read(afs.CONFIG.setup)
        self.volMng = VolumeService()
        self.VolID = int(self.test_config.get("VolService", "VolID"))
        self.VolName = self.test_config.get("VolService", "VolName")
        self.minCopy = int(self.test_config.get("VolService", "minCopy"))
        self.Owner = self.test_config.get("VolService", "Owner")
        self.FS = self.test_config.get("VolService", "FS")
        self.FSName = self.test_config.get("VolService", "FSName")
        self.Part = self.test_config.get("VolService", "Part")
        return    

    def test_get_volume_by_name(self) :
        task_ident = self.volMng.get_volume(self.VolName, cached=True, async=True)
        self.volMng.wait_for_task(task_ident) 
        res = self.volMng.get_task_result(task_ident)
        self.eval_get_volume_by_name(res)
        return    

    def test_get_volume_group_by_name(self) :
        task_ident = self.volMng.get_volume_group(self.VolName, cached=True, async=True)
        self.volMng.wait_for_task(task_ident) 
        res = self.volMng.get_task_result(task_ident)
        self.eval_get_volume_group_by_name(res)
        return    
    
class TestVolServiceMethods_historic(EvaluateTestResults) :

    @classmethod 
    def setUp(self):
        """
        setup VolService
        """
        self.test_config = ConfigParser()
        self.test_config.read(afs.CONFIG.setup)
        self.volMng = VolumeService()
        self.VolID = int(self.test_config.get("VolService", "VolID"))
        self.VolName = self.test_config.get("VolService", "VolName")
        self.minCopy = int(self.test_config.get("VolService", "minCopy"))
        self.Owner = self.test_config.get("VolService", "Owner")
        self.FS = self.test_config.get("VolService", "FS")
        self.FSName = self.test_config.get("VolService", "FSName")
        self.Part = self.test_config.get("VolService", "Part")
        return    

    def test_get_archived_volumes_by_name(self) :
        archived_rw_objs = self.volMng.get_archived( historic_Volume,  name=self.VolName )
        self.assertEqual(len(archived_rw_objs), 1)
        archived_ro_objs = self.volMng.get_archived( historic_Volume,  name="%s.readonly" % self.VolName )
        self.assertEqual(len(archived_ro_objs), 2)
        return    

if __name__ == '__main__' :
    parse_commandline()
    sys.stderr.write("Vacuum history tables\n")
    sys.stderr.write("==============================\n")
    afs.CONFIG.DB_HISTORY_NUM_PER_DAY = 0
    afs.CONFIG.DB_HISTORY_NUM_DAYS = 0
    DBMng = DBManager()
    DBMng.vacuum_history(historic_Volume, 0)
    sys.stderr.write("Testing live methods to fill DB_CACHE\n")
    sys.stderr.write("==============================\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestVolServiceMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
    sys.stderr.write("Testing methods accessing DB_CACHE\n")
    sys.stderr.write("================================\n")
    if afs.CONFIG.DB_CACHE :
        suite = unittest.TestLoader().loadTestsFromTestCase(TestVolServiceMethods_cached)
        unittest.TextTestRunner(verbosity=2).run(suite)
    else :
        sys.stderr.write("Skipped, because DB_CACHE is disabled.\n")

    sys.stderr.write("Testing live methods in async mode\n")
    sys.stderr.write("==================================\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestVolServiceMethods_async)
    unittest.TextTestRunner(verbosity=2).run(suite)

    sys.stderr.write("Testing methods accessing DB_CACHE in async mode\n")
    sys.stderr.write("===============================================\n")
    if afs.CONFIG.DB_CACHE :
        suite = unittest.TestLoader().loadTestsFromTestCase(TestVolServiceMethods_cached_async)
        unittest.TextTestRunner(verbosity=2).run(suite)
    else :
        sys.stderr.write("Skipped, because DB_CACHE is disabled.\n")

    sys.stderr.write("Testing history in DB_CACHE \n")
    sys.stderr.write("============================\n")
    if afs.CONFIG.DB_CACHE and afs.CONFIG.DB_HISTORY :
        suite = unittest.TestLoader().loadTestsFromTestCase(TestVolServiceMethods_historic)
        unittest.TextTestRunner(verbosity=2).run(suite)
    else :
        sys.stderr.write("Skipped, because DB_CACHE is disabled.\n")
