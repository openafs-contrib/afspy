#!/usr/bin/env python

import unittest
import sys, os
from ConfigParser import ConfigParser

sys.path.append("..")

from afs.util.AfsConfig import AfsConfig, setupDefaultConfig
from afs.util.options import define, options
from afs.service.VolService import VolService
import afs

class TestVolServiceMethods(unittest.TestCase):
    """
    Tests VolService Methods
    """
    
    def setUp(self):
        """
        setup token and VolService
        """
        self.TestCfg=ConfigParser()
        self.TestCfg.read(options.setup)
        self.Cell=self.TestCfg.get("general", "Cell")
        afs.defaultConfig.AFSCell=self.Cell
        self.User=self.TestCfg.get("general", "User")
        self.Pass=self.TestCfg.get("general", "Pass")
        self.volMng = VolService()
        self.VolID=int(self.TestCfg.get("VolService", "VolID"))
        self.VolName=self.TestCfg.get("VolService", "VolName")
        self.FS=self.TestCfg.get("VolService", "FS")
        self.FSName=self.TestCfg.get("VolService", "FSName")
        self.Part=self.TestCfg.get("VolService", "Part")
        if afs.defaultConfig.DB_CACHE :
            from sqlalchemy.orm import sessionmaker
            self.DbSession= sessionmaker(bind=afs.defaultConfig.DB_ENGINE)
        return
    
    def test_getVolbyName_live(self) :
        vol = self.volMng.getVolume(self.VolName, self.FS, self.Part, cached=False)
        self.assertEqual(vol.vid, self.VolID)
        self.assertEqual(vol.servername, self.FSName)
        self.assertEqual(vol.part, self.Part)
        return

    def test_getVolbyName_cached(self) :
        vol = self.volMng.getVolume(self.VolName, self.FS, self.Part, cached=True)
        self.assertEqual(vol.vid, self.VolID)
        self.assertEqual(vol.servername, self.FSName)
        self.assertEqual(vol.part, self.Part)
        return

if __name__ == '__main__' :
    define("setup", default="./Test.cfg", help="path to Testconfig")
    setupDefaultConfig()
    if not os.path.exists(options.setup) :
        sys.stderr.write("Test setup file %s does not exist.\n" % options.setup)
        sys.exit(2)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestVolServiceMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
