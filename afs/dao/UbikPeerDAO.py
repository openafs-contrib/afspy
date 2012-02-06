import re,string,os,sys
import afs.dao.bin

class UbikPeerDAO():
    
    """
    udebug and friends
    """
    
    def __init__(self):
        pass
    
    SyncRX=re.compile("Sync host (.*) was set (\d+) secs ago")
    SyncRX2=re.compile("I am sync site until (\d+) secs from now \(at (.*)\) \((\d+) servers\)")
    thisHostAddrRX=re.compile("Host's addresses are: (.*)")
    DBVerRX=re.compile("Sync site's db version is (.*)")

    def getSyncSite(self, servername, port):
        """
        return one IP of the SyncSite
        """
        SyncSite=""
        CmdList=[afs.dao.bin.UDEBUGBIN,"-server", "%s"  % servername, "-port", "%s" % port]
        rc,output,outerr=afs.dao.bin.execute(CmdList)
        if rc :
            raise ubikError(rc)
        for line in output :
            M=self.thisHostAddrRX.match(line) 
            if M :
                thisHostIPs=M.groups()[0].split()
            M=self.SyncRX.match(line) 
            if M :
                SyncSite=M.groups()[0]
                break
            M=self.SyncRX2.match(line) 
            if M :
                SyncSite=thisHostIPs[0]
                break
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
        
    def getDBVersion(self, servername, port):
        DBVersion=-1
        CmdList=[afs.dao.bin.UDEBUGBIN,"-server", "%s"  % servername, "-port", "%s" % port]
        rc,output,outerr=afs.dao.bin.execute(CmdList)
        if rc :
            raise ubikError(rc)
        for line in output :
            M=self.DBVerRX.match(line) 
            if M :
                DBVersion=M.groups()[0]
        return DBVersion
    
