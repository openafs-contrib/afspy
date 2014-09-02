#!/usr/bin/env python

from ConfigParser import ConfigParser
import sys
import unittest

from afs.tests.BaseTest import parse_commandline
from afs.service.FSService import FSService
import afs

class EvaluateTestResults(unittest.TestCase) :
    
    def eval_get_fileserver(self, res) :
        self.assertEqual(self.general_restart_time, res.general_restart_time)
        self.assertEqual(self.newbinary_restart_time, res.newbinary_restart_time)
        return

    def eval_partition_list(self, res) :
        return


class TestFSServiceSetMethods_async(unittest.TestCase):
    """             
    Tests FSService Methods
    """         
                    
    @classmethod    
    def setUpClass(self):
        """         
        setup FSService
        """     
        self.FSService = FSService()
        self.test_config = ConfigParser()
        self.test_config.read(afs.CONFIG.setup)
        self.FsName = self.test_config.get("FSService", "FS")
        self.FsUUID = self.test_config.get("FSService", "FSUUID")
        self.FsPartitions = self.test_config.get("FSService", "Partitions").split(",")
        self.FsPartitions.sort()
        self.fileserver=self.FSService.get_fileserver(self.FsName, async=True, cached=False)
        
    def test_partition_list(self) :
        parts = []
        for p in self.fileserver.parts :
            parts.append(p.name)
        parts.sort()
        self.assertEqual(self.FsPartitions, parts)
        return

    def test_uuid(self) :
        self.assertEqual(self.FsUUID, self.fileserver.uuid)
        return
        
    def test_get_volumes(self) :
        task_ident = self.FSService.get_volumes(self.fileserver, async=True, cached=False)
        self.FSService.wait_for_task(task_ident)
        volumes = self.FSService.get_task_result(task_ident)    
        sys.stderr.write("num_vols=%s\n" % len(volumes,))
        return

class TestFSServiceSetMethods(unittest.TestCase):
    """
    Tests FSService Methods
    """

    @classmethod
    def setUpClass(self):
        """
        setup FSService
        """ 
        self.FSService = FSService()
        self.test_config = ConfigParser()
        self.test_config.read(afs.CONFIG.setup)
        self.FsName = self.test_config.get("FSService", "FS")
        self.FsUUID = self.test_config.get("FSService", "FSUUID")
        self.FsPartitions = self.test_config.get("FSService", "Partitions").split(",")
        self.FsPartitions.sort()
        self.fileserver=self.FSService.get_fileserver(self.FsName, async=False, cached=False)

    def test_partition_list(self) :
        parts = []
        for p in self.fileserver.parts :
            parts.append(p.name)
        parts.sort()
        self.assertEqual(self.FsPartitions, parts)
        return

    def test_uuid(self) :
        self.assertEqual(self.FsUUID, self.fileserver.uuid)
        return

    def test_get_volumes(self) :
        volumes = self.FSService.get_volumes(self.fileserver, part="a", async=False, cached=False) 
        sys.stderr.write("num_vols=%s\n" % len(volumes,))
        return


class TestFSServiceCachedMethods(unittest.TestCase):
    """
    Tests FsService Methods from cache
    """
    
    @classmethod
    def setUpClass(self):
        """
        setup FsService
        """ 
        self.FSService = FSService()
        self.test_config = ConfigParser()
        self.test_config.read(afs.CONFIG.setup)
        self.FsName = self.test_config.get("FSService", "FS")
        self.FsUUID = self.test_config.get("FSService", "FSUUID")
        self.FsPartitions = self.test_config.get("FSService", "Partitions").split(",")
        self.FsPartitions.sort()
        self.fileserver=self.FSService.get_fileserver(self.FsName, async=False, cached=True)

    @classmethod
    def tearDownClass(self) :
        """
        remove history from DB
        """
        sys.stderr.write("removing historic classes")
        #self.FSService.DBManager.vaccuum_cache()
        return

    def test_partitionlist(self) :
        parts = []
        for p in self.fileserver.parts :
            parts.append(p.name)
        parts.sort()
        self.assertEqual(self.FsPartitions, parts)
        return

    def test_uuid(self) :
        self.assertEqual(self.FsUUID, self.fileserver.uuid)
        return

    def test_get_volumes(self) :
        volumes = self.FSService.get_volumes(self.fileserver, part="a", async=False, cached=True) 
        sys.stderr.write("num_vols=%s\n" % len(volumes,))
        return

if __name__ == '__main__' :
    parse_commandline()

    sys.stderr.write("Testing async methods to fill DB_CACHE\n")
    sys.stderr.write("==============================\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFSServiceSetMethods_async)
    unittest.TextTestRunner(verbosity=2).run(suite)
    sys.stderr.write("Testing live methods to fill DB_CACHE\n")
    sys.stderr.write("==============================\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFSServiceSetMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
    sys.stderr.write("Testing sync methods accessing DB_CACHE\n")
    sys.stderr.write("================================\n")
    if afs.CONFIG.DB_CACHE :
        suite = unittest.TestLoader().loadTestsFromTestCase(TestFSServiceCachedMethods)
        unittest.TextTestRunner(verbosity=2).run(suite)
    else :
         sys.stderr.write("Skipped,  because DB_CACHE is disabled.\n")
