import re,string,os,sys
import afs.dao.bin
from afs.exceptions.UbikError import UbikError

class UbikPeerDAO():
    
    """
    udebug 
    """
    
    def __init__(self):
        pass
    
    SyncRX=re.compile("Sync host (.*) was set (\d+) secs ago")
    SyncRX2=re.compile("I am sync site until (\d+) secs from now \(at (.*)\) \((\d+) servers\)")
    thisHostAddrRX=re.compile("Host's addresses are: (.*)")
    syncDBVerRX=re.compile("Sync site's db version is (.*)")
    localDBVerRX=re.compile("Local db version is (.*)")
    PeerRX=re.compile("Server \((\S+)\): \(db (\S+)\)(\W+is only a clone!)?")
    DBStateRX=re.compile("Recovery state (\S+)")
    Vote1stLine=re.compile("last vote rcvd (\d+) secs ago \(at (.*)\),")
    Vote2ndLine=re.compile("last beacon sent (\d+) secs ago \((.*)\), last vote was (\S+)")
    
    
    def getSyncSite(self, servername, port):
        """
        return one IP of the SyncSite
        """
        return self.exec_and_parse(servername, port)["SyncSite"]
        
    def getAllPeers(self, servername, port):
        """
        In an ubik-database, there are sites which can get master
        and sites which cannot Clones, return those 
        types separately
        """
        return self.exec_and_parse(servername, port)["Peers"]
        
    def getDBVersion(self, servername, port):
        return self.exec_and_parse(servername, port)["syncDBVersion"]
    
    def getDBState(self, servername, port):
        """
        return "Recoverystate". 
        raise an error if not run on SyncSite..
        """
        d=self.exec_and_parse(servername, port)
        if d["DBState"] == "" :
            raise UbikError("%s: not  SyncSite" % servername)
        return d["DBState"]
    
    def exec_and_parse(self, servername, port):
        """
        Parsing is always the same, so do it here.
        """
        CmdList=[afs.dao.bin.UDEBUGBIN,"-server", "%s"  % servername, "-port", "%s" % port,  "-long"]
        rc,output,outerr=afs.dao.bin.execute(CmdList)
        if rc :
            raise ubikError(rc)
        d= { "SyncSite" : "", 
            "DBState" : "", 
            "syncDBVersion" :-1, 
            "localDBVersion" :-1, 
            "Peers" :{}, 
            "thisHostIPs" : [], 
        }
        line_no=-1
        while line_no < len(output)-1  :
            line_no += 1
            #sys.stderr.write("line_no = %s\n" % line_no)
            line=output[line_no]
            M=self.thisHostAddrRX.match(line) 
            if M :
                d["thisHostIPs"]=M.groups()[0].split()
                continue
            M=self.SyncRX.match(line) 
            if M :
                d["SyncSite"]=M.groups()[0]
                continue
            M=self.SyncRX2.match(line) 
            if M :
                d["SyncSite"]=d["thisHostIPs"][0]
            M=self.syncDBVerRX.match(line)
            if M :
                d["syncDBVersion"] = M.groups()[0]
                continue 
            M=self.localDBVerRX.match(line)
            if M :
                d["localDBVersion"] = M.groups()[0]
                continue
            # we make DBState a string, not boolean, because 
            # there are more states than OK/NOTOK, even 
            # if we don't uswe them yet.
            M=self.DBStateRX.match(line)
            if M :
                if M.groups()[0] == "1f":
                    d["DBState"]="OK"
                else :
                    d["DBState"]="NOTOK"
                continue
            M=self.PeerRX.match(line)
            if M :
                IP, DbVer, isClone=M.groups()
                peerDict={"lastVoteRcvd" : -1,  "lastVote" : "NA",  "lastBeaconSend" : -1,  "DBVersion": DbVer}
                if isClone :
                    peerDict["isClone"] = True
                else:
                    peerDict["isClone"] = False
                line_no+=1
                line=output[line_no]
                peerDict["lastVoteRcvd"]=self.Vote1stLine.match(line).groups()[0]
                line_no+=1
                line=output[line_no]
                peerDict["lastBeaconSend"]=self.Vote2ndLine.match(line).groups()[0]
                peerDict["lastVote"]=self.Vote2ndLine.match(line).groups()[2]
                d["Peers"][IP]= peerDict
                continue
        return d
