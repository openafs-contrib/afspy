#!/usr/bin/env python

import unittest
import sys, os
from ConfigParser import ConfigParser

sys.path.append("..")

from afs.util.AfsConfig import setupDefaultConfig
from afs.util.options import define, options
from afs.service.FsService import FsService
import afs
import afs.dao.bin

class TestFsServiceMethods(unittest.TestCase):
    """
    Tests FsService Methods
    """
    
    def setUp(self):
        """
        setup token and FsService
        """
        self.TestCfg=ConfigParser()
        self.TestCfg.read(options.setup)
        self.Cell=self.TestCfg.get("general", "Cell")
        afs.defaultConfig.AFSCell=self.Cell
        self.User=self.TestCfg.get("general", "User")
        self.Pass=self.TestCfg.get("general", "Pass")
        self.FsMng = FsService()
        self.FsName=self.TestCfg.get("FsService", "FS")
        self.FsPartitions=self.TestCfg.get("FsService", "Partitions").split(",")
        self.FsPartitions.sort()
        if afs.defaultConfig.DB_CACHE :
            from sqlalchemy.orm import sessionmaker
            self.DbSession= sessionmaker(bind=afs.defaultConfig.DB_ENGINE)
        return

    def test_getRestartTimes(self):
        TimesDict = self.FsMng.getRestartTimes(self.FsName)
        self.assertEqual("never",TimesDict["general"])
        self.assertEqual("5:00 am",TimesDict["binary"])
        return

    def test_setRestartTimes(self):
        restartTime = self.FsMng.setRestartTimes(self.FsName,"never","general")
        self.assertEqual(None,restartTime)
        restartTime = self.FsMng.setRestartTimes(self.FsName,"never","binary")
        self.assertEqual(None,restartTime)
        return
        
    def test_getServerObj(self) :
        server=self.FsMng.getFileServer(self.FsName)
        parts=[]
        for p in server.parts :
            parts.append(server. parts[p]["name"])
        parts.sort()
        self.assertEqual(self.FsPartitions, parts)
        return

if __name__ == '__main__' :
    define("setup", default="./Test.cfg", help="path to Testconfig")
    setupDefaultConfig()
    if not os.path.exists(options.setup) :
        sys.stderr.write("Test setup file %s does not exist.\n" % options.setup)
        sys.exit(2)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFsServiceMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
