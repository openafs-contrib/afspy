import re,string,os,sys
import afs.dao.bin

from afs.util import afsutil
from afs.exceptions.ProcError import ProcError

def restartT2Minutes(Time):
    """
    converts a restart time from the human readable output to
    minutes after midnight.
    -1 means never
    """
    if Time == "never" : return -1
    Minutes=0
    tokens=Time.split()
    if tokens[1] == "pm" :
       Minutes = 12*60
    hours, min=tokens[0].split(":")
    Minutes += int(hours)*60 + min
    return Minutes

def minutes2restartT(Minutes) :
    """
    converts an int meaning Minutes after midnight into a 
    restartTime string  understood by the bos command
    """
    if Minutes == -1 :
        return "never"
    Pod="am"
    if Minutes > 12*60 :
        Pod="pm"
        Minutes -= 12*60
    Time = "%d:%02d %s" % (Minutes/60, Minutes%60,Pod)
    return Time

class ProcessDAO() :
    """
    Direct Access Object for a Process (BNode)
    """
    generalRestartRegEX=re.compile("Server (\S+) restarts (?:at)?(.*)")
    binaryRestartRegEX=re.compile("Server (\S+) restarts for new binaries (?:at)?(.*)")
    DBServerRegEx=re.compile("Host (\d+) is (\S+)")

    def __init__(self) :
        return
    
    def getRestartTimes(self, servername, cellname, token):
        CmdList=[afs.dao.bin.BOSBIN,"getrestart","-server", "%s"  % servername]
        rc,output,outerr=afs.dao.bin.execute(CmdList)
        if rc :
            raise ProcError( outerr, output)
        
        if len(output) != 2 :
            raise ProcError( outerr, output)
        
        st = []
        st[generalRestart]=self.generalRestartRegEX.match(output[0]).groups()[1].strip()
        st[binaryRestart]=self.binaryRestartRegEX.match(output[1]).groups()[1].strip()
        
        return st

    def setRestartTimes(self, servername, time, restarttype, cellname, token):
        if restarttype == "general" :
            option = "-general"
        elif restarttype == "binary" :
            option = "-newbinary"
        else :
             raise ProcError( "invalid restarttype=%s" % restarttype, '')
             return 1, "invalid restarttype=%s" % restarttype
        CmdList=[afs.dao.bin.BOSBIN,"setrestart","-server", "%s"  % servername, "-time",  "%s" % time,  "%s" % option ]
        rc,output,outerr=afs.dao.bin.execute(CmdList)
        
        return 

    def addUser(self, user, servername, cellname):
        pass
    
    def removeUser(self, user, servername, cellname):
        pass
    
    def getUserList(self, servername, cellname):
        pass
    
    def getFileDate(self,file, servername, cellname):
        pass
    
    def cmd(self, cmd, servername, cellname):
        pass
    
    def getLog(self, log, servername, cellname):
        pass
    
    def pruneLog(self, type, servername, cellname):
        pass

    def runRestart(self, process, servername, cellname):
        pass
    
    def runStart(self, process, servername, cellname):
        pass
    
    def runShutdown(self, process, servername, cellname):
        pass
    
    def runStartup(self, process, servername, cellname):
        pass
    
    def runStop(self, process, servername, cellname):
        pass

    def salvage(self, vid, part, servername, cellname, **kwargs):
        pass
    
    def status(self, process, servername, cellname, **kwargs):
        pass

    def getDBServList(self,servername, cellname ):
        """
        get list of all database-servers known to a given AFS-server
        """
        CmdList=[afs.dao.bin.BOSBIN,"listhosts","-server", "%s"  % servername, "-cell" , "%s" % cellname]
        rc,output,outerr=afs.dao.bin.execute(CmdList)
        if rc :
            raise ProcError( outerr, output)
            
        DBServers=[]
        for line in output :
            mObj=self.DBServerRegEx.match(line)
            if mObj :
                server = {}
                host=mObj.groups()[1].strip()
                if host[0] == "[" and host[len(host)-1] == "]" :
                    server['hostname']=host[1:-1]
                    server['isClone'] = 1
                else :
                    server['hostname']=host
                    server['isClone'] = 0
                DBServers.append(server)
        return DBServers
