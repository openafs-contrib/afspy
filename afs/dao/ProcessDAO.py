import re,string,os,sys
import afs.dao.bin

from afs.util import afsutil


class ProcessDAO() :
    """
    Direct Access Object for a Process (BNode)
    """
    generalRestartRegEX=re.compile("Server (\S+) restarts (?:at)?(.*)")
    binaryRestartRegEX=re.compile("Server (\S+) restarts for new binaries (?:at)?(.*)")

    def __init__(self) :
        return
    
    def getRestartTimes(self, servername, cellname):
        CmdList=[afs.dao.bin.BOSBIN,"getrestart","-server", "%s"  % servername]
        rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=0)
        if rc :
            return rc,output,outerr
        if len(output) != 2 :
            return 1, output, outerr
        generalRestart=generalRestartRegEX.match(output[0]).groups()[1]
        binaryRestart=binaryRestartRegEX.match(output[1]).groups()[1]
        return generalRestart, binaryRestart

    def setRestart(self, time, restarttype, servername, cellname):
        if restarttype == "general" :
            option = "-general"
        elif restarttype == "binary" :
            option = "-newbinary"
        else :
             return False
        CmdList=[afs.dao.bin.BOSBIN,"setrestart","-server", "%s"  % servername, "-time",  "%s" % time,  "%s" % option ]
        rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=0)
        if rc :
            raise Error

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

