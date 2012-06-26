#!/usr/bin/env python

import unittest
from BaseTest import parseCMDLine, basicTestSetup

import afs.dao.OSDVolumeDAO 

class TestOSDVolumeDAOMethods(unittest.TestCase, basicTestSetup):
    """
    Tests OSDVolumeDAO Methods
    """
    
    def setUp(self):
        """
        setup
        """
        basicTestSetup.setUp(self)
        self.FS_nonOSD=self.TestCfg.get("OSDVolumeDAO","FS_nonOSD")
        self.Part_nonOSD=self.TestCfg.get("OSDVolumeDAO","Part_nonOSD")
        self.VolumeID_nonOSD=int(self.TestCfg.get("OSDVolumeDAO","VolID_nonOSD"))
        self.numVols_nonOSD=int(self.TestCfg.get("OSDVolumeDAO","numVols_nonOSD"))
        self.FS_OSD=self.TestCfg.get("OSDVolumeDAO","FS_OSD")
        self.Part_OSD=self.TestCfg.get("OSDVolumeDAO","Part_OSD")
        self.VolumeID_OSD=int(self.TestCfg.get("OSDVolumeDAO","VolID_OSD"))
        self.numVols_OSD=int(self.TestCfg.get("OSDVolumeDAO","numVols_OSD"))
        
        self.DAO = afs.dao.OSDVolumeDAO.OSDVolumeDAO()
        return
    
    def test_get_nonOSD_Volume(self) :
        Volume=self.DAO.getVolume(self.VolumeID_nonOSD,self.FS_nonOSD,self.Part_nonOSD,self.Cell,None)
        self.assertEqual(Volume['vid'],self.VolumeID_nonOSD)
        return

    def test_get_OSD_Volume(self) :
        Volume=self.DAO.getVolume(self.VolumeID_OSD,self.FS_OSD,self.Part_OSD,self.Cell,None)
        self.assertEqual(Volume['vid'],self.VolumeID_OSD)
        return
        
    def test_getVol_nonOSD_GroupList(self) :
        VolGroupList=self.DAO.getVolGroupList(self.VolumeID_nonOSD,self.Cell,None)
        self.assertEqual(len(VolGroupList),self.numVols_nonOSD)
        return

    def test_getVol_OSD_GroupList(self) :
        VolGroupList=self.DAO.getVolGroupList(self.VolumeID_OSD,self.Cell,None)
        self.assertEqual(len(VolGroupList),self.numVols_OSD)
        return

    def test_traverse_OSD(self) :
        histogram_OSD=self.DAO.traverse(self.FS_OSD,self.VolumeID_OSD,self.Cell,None)
        self.assertTrue(1)
        return

if __name__ == '__main__' :
    parseCMDLine()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestOSDVolumeDAOMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
