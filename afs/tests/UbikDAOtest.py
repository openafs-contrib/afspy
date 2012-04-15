#!/usr/bin/env python

import unittest
from BaseTest import parseCMDLine, basicTestSetup

from afs.dao import UbikPeerDAO 


class TestUbikDAOMethods(unittest.TestCase, basicTestSetup):
    """
    Tests UbikPeerDAO Methods
    """
    
    def setUp(self):
        """
        setup
        """
        basicTestSetup.setUp(self)

        self.SyncSite=self.TestCfg.get("UbikDAO","SyncSite")
        self.DBPort=self.TestCfg.get("UbikDAO","DBPort")
        self.DBState=self.TestCfg.get("UbikDAO","DBState")
        self.allHosts=self.TestCfg.get("UbikDAO","allDBs").split(",")
        self.allHosts.sort()
        self.not_SyncSite=""
        # get a non-Sync DB Host
        if len(self.allHosts) == 1 :
            raise unittest.SkipTest("Only one DB-Server defined")
        for srv in self.allHosts :
            if self.SyncSite != srv :
                self.not_SyncSite=srv
                break
                
        self.DAO = UbikPeerDAO.UbikPeerDAO()
        return

    def do_test_getSyncSite(self, servername):
        SyncSite=self.DAO.getSyncSite(servername, self.DBPort)
        self.assertTrue( (SyncSite in self.allHosts), msg="SyncSite '%s' not in allDBs : %s" % (SyncSite, self.allHosts))
        return

    def test_getSyncSite_syncSite(self) :
        self.do_test_getSyncSite(self.SyncSite)
        return

    def test_getSyncSite_not_syncSite(self):
        self.do_test_getSyncSite(self.not_SyncSite)
        return

    def do_test_getAllPeers(self, servername):
        Peers=self.DAO.getAllPeers(servername, self.DBPort)
        allPeers=Peers.keys()
        allPeers.sort()
        self.allHosts.remove(servername)
        self.assertEqual(allPeers, self.allHosts)
        return 
        
    def test_getAllPeers_syncSite(self) :
        self.do_test_getAllPeers(self.SyncSite)
        return

    def test_getAllPeers_not_syncSite(self):
        if len(self.allHosts) == 1 :
            raise unittest.SkipTest("Only one DB-Server defined")
        for srv in self.allHosts :
            if self.SyncSite != srv :
                servername=srv
                break
        self.do_test_getAllPeers(servername)
        return
 
    def do_test_getDBVersion(self, servername) :
        DBVersion=self.DAO.getDBVersion(self.SyncSite, self.DBPort)
        self.assertTrue((DBVersion>self.minUbikDBVersion))
        return
    
    def test_getDBVersion_syncSite(self)  :
        self.do_test_getDBVersion(self.SyncSite)
        return

    def test_getDBVersion_not_syncSite(self)  :
        self.do_test_getDBVersion(self.not_SyncSite)
        return

    def do_test_getDBState(self, servername) :
        DBState=self.DAO.getDBState(servername, self.DBPort)
        self.assertEqual(DBState, self.DBState)
        return
    
    def test_getDBState_syncSite(self):
        self.do_test_getDBState(self.SyncSite)
        return
    
    @unittest.expectedFailure
    def test_getDBState_not_syncSite(self):
        self.do_test_getDBState(self.not_SyncSite)
        return
        
    def do_test_voting(self, servername):
        d=self.DAO.exec_and_parse(servername, self.DBPort)
        for p in d["Peers"] :
            self.assertTrue((d["Peers"][p]["lastVote"] in ["yes","no"]), "Peer '%s' reports lastVote '%s', which is neither 'yes' nor 'no'" % (p,d["Peers"][p]["lastVote"]  ))
        return

    def test_voting_syncSite(self):
        self.do_test_voting(self.SyncSite)
        return

    def test_voting_not_SyncSite(self):
        self.do_test_voting(self.not_SyncSite)
        return

    def do_test_lastBeaconSend(self, servername): 
        d=self.DAO.exec_and_parse(servername, self.DBPort)
        for p in d["Peers"] :
            self.assertTrue((float(d["Peers"][p]["lastBeaconSend"]) >= 0), "last Beacon Sendtime '%s' is not a non-negative float"  %d["Peers"][p]["lastBeaconSend"] )
        return
    
    def test_lastBeaconSend_SyncSite(self) :
        self.do_test_lastBeaconSend(self.SyncSite)
        return
    
    def test_lastBeaconSend_not_SyncSite(self) :
        self.do_test_lastBeaconSend(self.not_SyncSite)
        return


if __name__ == '__main__' :
    parseCMDLine()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUbikDAOMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
