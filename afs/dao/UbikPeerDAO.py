import re,string,os,sys
import afs.dao.bin

class UbikPeerDAO():
    
    """
    udebug and friends
    """
    
    def __init__(self):
        pass
    
    def getSyncSite(self, servername, port):
        SyncSite=""
        return SyncSite
        
    def getAllPeers(self, servername, port):
        """
        In an ubik-database, there are sites which can get master
        and sites which cannot Clones, return those 
        types separately
        """
        PeerList=[]
        CloneList=[]
        return PeerList, CloneList
        
    def getDBVersion(self):
        DBVersion=-1
        return DBVersion
    
