#!/usr/bin/env python

from ConfigParser import ConfigParser
import sys
import unittest

from afs.tests.BaseTest import parse_commandline
from afs.lla import FileServerLLA
import afs

class EvaluateTestResults(unittest.TestCase) :
    """
    evaluate results
    """

    def eval_get_volume_list(self, res) :
        # this is somewhat silly, but what can you do ?
        # maybe check structure of result ?
        self.assertTrue(len(res) < 100)
        return

    def eval_get_volume_id_list(self, res) :
        # this is somewhat silly, but what can you do ?
        # maybe check structure of result ?
        self.assertTrue(len(res) < 100)
        return

    def eval_get_partitions(self, res) :
        for p in res :
           if not p.name in self.allParts :
                self.assertEqual(p, "Not in Test.cfg")
        return

class TestFileServerLLAMethods(EvaluateTestResults):
    """
    Tests FileServerLLA Methods
    """
    
    @classmethod
    def setUp(self):
        """
        setup
        """
        self.lla = afs.lla.FileServerLLA.FileServerLLA()
        self.test_config = ConfigParser()
        self.test_config.read(afs.CONFIG.setup)
        self.FS = afs.model.FileServer.FileServer()
        self.FS.servernames = [self.test_config.get("FileServerLLA","FS"), ]
        self.Part = self.test_config.get("FileServerLLA","Part")
        self.allParts = self.test_config.get("FileServerLLA","allParts")
        return
    
    def test_get_volume_list(self) :
        res = self.lla.get_volume_list(self.FS, part=self.Part)
        self.eval_get_volume_list(res)
        return
        
    def test_get_volume_id_list(self) :
        res = self.lla.get_volume_id_list(self.FS, part=self.Part)
        self.eval_get_volume_id_list(res)
        return

    def test_get_partitions(self) :
        res = self.lla.get_partitions(self.FS)
        self.eval_get_volume_list(res)
        return

class TestFileServerLLAMethods_async(EvaluateTestResults):
    """
    Tests FileServerLLA Methods
    """
    
    @classmethod
    def setUp(self):
        """
        setup
        """
        self.lla = afs.lla.FileServerLLA.FileServerLLA()
        self.test_config = ConfigParser()
        self.test_config.read(afs.CONFIG.setup)
        self.FS = afs.model.FileServer.FileServer()
        self.FS.servernames = [self.test_config.get("FileServerLLA","FS"), ]
        self.Part = self.test_config.get("FileServerLLA","Part")
        self.allParts = self.test_config.get("FileServerLLA","allParts")
        return
    
    def test_get_volume_list(self) :
        sp_ident = self.lla.get_volume_list(self.FS, part=self.Part, async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_get_volume_list(res)
        return
        
    def test_get_volume_id_list(self) :
        sp_ident = self.lla.get_volume_id_list(self.FS, part=self.Part, async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_get_volume_id_list(res)
        return

    def test_get_partitions(self) :
        sp_ident = self.lla.get_partitions(self.FS, async=True)
        self.lla.wait_for_subprocess(sp_ident)
        res = self.lla.get_subprocess_result(sp_ident)
        self.eval_get_partitions(res)
        return
    
if __name__ == '__main__' :
    parse_commandline()
    sys.stderr.write("\n===\n=== testing direct fork ===\n===\n\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFileServerLLAMethods)
    unittest.TextTestRunner(verbosity = 2).run(suite)
    sys.stderr.write("\n===\n=== testing detached execution ===\n===\n\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFileServerLLAMethods_async)
    unittest.TextTestRunner(verbosity = 2).run(suite)
