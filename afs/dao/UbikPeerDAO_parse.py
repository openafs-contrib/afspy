from afs.exceptions.UbikError import UbikError
import re

SyncRX=re.compile("Sync host (.*) was set (\d+) secs ago")
SyncRX2=re.compile("I am sync site until (\d+) secs from now \(at (.*)\) \((\d+) servers\)")
LocalCloneRX=re.compile("I am a clone and never can become sync site")
NotSyncRX=re.compile("I am not sync site")
thisHostAddrRX=re.compile("Host's addresses are: (.*)")
syncDBVerRX=re.compile("Sync site's db version is (.*)")
localDBVerRX=re.compile("Local db version is (.*)")
PeerRX=re.compile("Server \((\S+)\): \(db (\S+)\)(\W+is only a clone!)?")
DBStateRX=re.compile("Recovery state (\S+)")
Vote1stLine=re.compile("last vote rcvd (\d+) secs ago \(at (.*)\),")
Vote2ndLine=re.compile("last beacon sent (\d+) secs ago \((.*)\), last vote was (\S+)")
HostTimeRX=re.compile("Host's (.*) time is (.*)")
LocalTimeRX=re.compile("Local time is (.*) \(time differential (\d+) secs\)")
LastYesVoteRX=re.compile("Last yes vote for (.*) was (.*) secs ago \(sync site\);")
    
def parse_getShortInfo(rc, output, outerr, parseParamList, Logger) :
    """
    parse output of udebug
    """
    resDict={}
    idx=0 
    # "Host's addresses are: 130.183.14.14"
    resDict["HostAddrs"] = output[idx].split(":")[1].strip()
    idx += 1
    # "Host's 130.183.14.14 time is Thu Sep 27 08:19:51 2012"
    resDict["HostTime"] = output[idx].split("time is")[1].strip()
    idx += 1
    # "Local time is Thu Sep 27 08:19:51 2012 (time differential 0 secs)"
    splits = output[idx].split("time is")[1].split("(")
    resDict["localTime"] = splits[0]
    resDict["TimeDiff"] = int(splits[1].split()[2])
    idx += 1
    # "Last yes vote for 14.14.183.130 was 6 secs ago (sync site);"
    resDict["lastYesVoteTime"] = int(output[idx].split()[6])
    idx += 1
    # "Last vote started 6 secs ago (at Thu Sep 27 08:19:45 2012)"
    resDict["lastVoteStart"] = int(output[idx].split()[3])
    idx += 1
    # "Local db version is 1348069670.41454"
    resDict["localDBVersion"] = output[idx].split()[4]
    idx += 1
    # now we need to distinguish between sync site and others
    if "I am sync site" in output[idx] :
        # "I am sync site until 54 secs from now (at Thu Sep 27 08:20:45 2012) (3 servers)"
        resDict["isSyncSite"] = True
        resDict["isClone"] = False
        # XXX this can fail
        resDict["SyncSite"] = resDict["HostAddrs"]
        idx += 1
        # "Recovery state 1f"
        if output[idx].split()[2] == "1f" :
            resDict["DBState"] = "OK"
        else :
            resDict["DBState"] = "NOTOK"
        idx += 1
        # "I am currently managing write trans 1348069670.115422006"
        if "I am currently managing" in output[idx] : idx += 1 
        # "Sync site's db version is 1348069670.41445"
        resDict["SyncSiteDBVersion"] = output[idx].split()[5]
    else :
        if "I am not sync site" == output[idx] :
            resDict["isClone"] = False
        elif "I am a clone and never can become sync site" :
            resDict["isClone"] = True
        else :
            raise UbikError("Cannot get Sync/clone info from %s" % output[idx])
        # "I am not sync site"
        resDict["isSyncSite"] = False
        idx += 1
        # "Lowest host 130.183.9.5 was set 5 secs ago"
        resDict["lowestHost"] = output[idx].split()[2]
        idx += 1
        # "Sync host 130.183.14.14 was set 5 secs ago"
        resDict["SyncSite"] = output[idx].split()[2]
        idx += 1
        # "Sync site's db version is 1348069670.41454"
        resDict["SyncSiteDBVersion"] = output[idx].split()[5]
        idx += 1
        # "0 locked pages, 0 of them for write"
        # XXX ignore the rest
    return resDict
        

def parse_getLongInfo( rc, output, outerr, parseParamList,Logger) :
    """
    Parsing is always the same, so do it here.
    """
    d= { "SyncSite" : "", 
        "DBState" : "", 
        "syncDBVersion" :-1, 
        "localDBVersion" :-1, 
        "Peers" :{}, 
        "thisHostIPs" : [], 
    }
    line_no=-1
    thisPeerDict={"lastVoteRcvd" : -1,  "lastVote" : "NA",  "lastBeaconSend" : -1,  "DBVersion": -1, "isClone" : None}
    while line_no < len(output)-1  :
        line_no += 1
        line=output[line_no]
        M=thisHostAddrRX.match(line) 
        if M :
            d["thisHostIPs"]=M.groups()[0].split()
            continue
        M=SyncRX.match(line) 
        if M :
            d["SyncSite"]=M.groups()[0]
            continue
        M=SyncRX2.match(line) 
        if M :
            d["SyncSite"]=d["thisHostIPs"][0]
            thisPeerDict["isClone"] = True
        M=LocalCloneRX.match(line)
        if M :
            thisPeerDict["isClone"] = False
        M=NotSyncRX.match(line) 
        if M :
            thisPeerDict["isClone"] = False
        M=syncDBVerRX.match(line)
        if M :
            d["syncDBVersion"] = M.groups()[0]
            continue 
        M=localDBVerRX.match(line)
        if M :
            d["localDBVersion"] = M.groups()[0]
            continue
        # we make DBState a string, not boolean, because 
        # there are more states than OK/NOTOK, even 
        # if we don't uswe them yet.
        M=DBStateRX.match(line)
        if M :
            if M.groups()[0] == "1f":
                d["DBState"]="OK"
            else :
                d["DBState"]="NOTOK"
            continue
        M=PeerRX.match(line)
        if M :
            IP, DbVer, isClone=M.groups()
            peerDict={"lastVoteRcvd" : -1,  "lastVote" : "NA",  "lastBeaconSend" : -1,  "DBVersion": DbVer, "isClone" : None}
            if isClone != None :
                peerDict["isClone"] = True
            else:
                peerDict["isClone"] = False
            line_no+=1
            line=output[line_no]
            peerDict["lastVoteRcvd"]=Vote1stLine.match(line).groups()[0]
            line_no+=1
            line=output[line_no]
            peerDict["lastBeaconSend"]=Vote2ndLine.match(line).groups()[0]
            peerDict["lastVote"]=Vote2ndLine.match(line).groups()[2]
            d["Peers"][IP]= peerDict
            Logger.debug("%s: %s" % (IP,peerDict))
            continue
        M=HostTimeRX.match(line)
        if M :
            Host,Time=M.groups()
            Logger.debug("Got host=%s time=%s" % (Host,Time) )
            continue
        M=LocalTimeRX.match(line)
        if M :
            localTime,diffTime=M.groups()
            Logger.debug("Got localtime=%s differential=%s" % (localTime,diffTime) )
            continue

        M=LastYesVoteRX.match(line)
        if M :
            Host,ago=M.groups()
            continue

        #raise UbikError("Error Parsing line: %s" % output[line_no])
    d["Peers"][d["thisHostIPs"][0]]=thisPeerDict
    return d
