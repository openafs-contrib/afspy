import string, types
from afs.dao.BaseDAO import BaseDAO,execwrapper
import BNodeDAO_parse as PM
from afs.exceptions.BNodeError import BNodeError


class BNodeDAO(BaseDAO) :
    """
    Direct Access Object for a Process (BNode)
    """

    def __init__(self) :
        BaseDAO.__init__(self)
        return

    @execwrapper    
    def getRestartTimes(self, servername, _cfg=None):
        """
        return dict telling the restart times
        """
        CmdList=[_cfg.binaries["bos"],"getrestart","-server", "%s"  % servername]
        return CmdList,PM.getRestartTimes

    @execwrapper    
    def setRestartTimes(self, servername, time, restarttype, _cfg=None) :
        if restarttype == "general" :
            option = "-general"
        elif restarttype == "binary" :
            option = "-newbinary"
        else :
             raise BNodeError( "invalid restarttype=%s" % restarttype, '')
             return 1, "invalid restarttype=%s" % restarttype
        CmdList=[_cfg.binaries["bos"],"setrestart","-server", "%s"  % servername, "-time",  "%s" % time,  "%s" % option ]
        return CmdList,PM.setRestartTimes

    @execwrapper    
    def addUser(self, servername, userlist, _cfg=None) :
        if type(userlist) == types.ListType :
            usernames = string.join(userlist)
        else :
            usernames = userlist
        CmdList=[_cfg.binaries["bos"],"adduser","-server", "%s"  % servername, "-user",  "%s" % usernames ]
        return CmdList,PM.addUser
    
    @execwrapper    
    def removeUser(self, servername, userlist, _cfg=None) :
        if type(userlist) == types.ListType :
            usernames = string.join(userlist)
        else :
            usernames = userlist
        CmdList=[_cfg.binaries["bos"],"removeuser","-server", "%s"  % servername, "-user",  "%s" % usernames ]
        return CmdList,PM.removeUser
    
    @execwrapper    
    def getUserList(self, servername, _cfg=None) :
        CmdList=[_cfg.binaries["bos"],"listuser","-server", "%s"  % servername ]
        return CmdList,PM.getUserList
    
    @execwrapper    
    def getFileDate(self, servername, filelist, destdir="", _cfg=None) :
        if type(filelist) == types.ListType :
            filenames = string.join(filelist)
        else :
            filenames = filelist
        CmdList=[_cfg.binaries["bos"],"getdate","-server", "%s"  % servername, "-files", "%s" % filenames ]
        if destdir != "" :
            CmdList += ["-dir", "%s" % destdir]
        return CmdList,PM.getFileDate
    
    @execwrapper    
    def cmd(self, servername, cmd, _cfg=None) :
        CmdList=[_cfg.binaries["bos"],"cmd","-server", "%s"  % servername ]
        return CmdList,PM.cmd
    
    @execwrapper    
    def getLog(self, servername, logfile,_cfg=None) :
        CmdList=[_cfg.binaries["bos"],"getlog","-server", "%s"  % servername ]
        return CmdList,PM.getLog
    
    @execwrapper    
    def prune(self, type, servername, _cfg=None) :
        CmdList=[_cfg.binaries["bos"],"prune","-server", "%s"  % servername ]
        return CmdList,PM.pruneLog

    @execwrapper    
    def runRestart(self, process, servername, _cfg=None) :
        CmdList=[_cfg.binaries["bos"],"restart","-server", "%s"  % servername ]
        return CmdList,PM.runRestart
    
    @execwrapper    
    def runStart(self, process, servername, _cfg=None) :
        CmdList=[_cfg.binaries["bos"],"start","-server", "%s"  % servername ]
        return CmdList,PM.runStart
    
    @execwrapper    
    def runShutdown(self, process, servername, _cfg=None) :
        CmdList=[_cfg.binaries["bos"],"shutdown","-server", "%s"  % servername ]
        return CmdList,PM.runShutdown
    
    @execwrapper    
    def runStartup(self, process, servername, _cfg=None) :
        CmdList=[_cfg.binaries["bos"],"startup","-server", "%s"  % servername ]
        return CmdList,PM.runStartup
    
    @execwrapper    
    def runStop(self, process, servername, _cfg=None) :
        CmdList=[_cfg.binaries["bos"],"stop","-server", "%s"  % servername ]
        return CmdList,PM.runStop

    @execwrapper    
    def salvage(self, vid, part, servername, _cfg=None) :
        CmdList=[_cfg.binaries["bos"],"salvageXXX","-server", "%s"  % servername ]
        return CmdList,PM.salvage
    
    @execwrapper    
    def status(self, process, servername, _cfg=None) :
        CmdList=[_cfg.binaries["bos"],"status","-server", "%s"  % servername ,"-long"]
        return CmdList,PM.status

    @execwrapper    
    def getDBServList(self,servername, _cfg=None) :
        """
        get list of all database-servers known to a given AFS-server
        """
        CmdList=[_cfg.binaries["bos"],"listhosts","-server", "%s"  % servername, "-cell" , "%s" % _cfg.CELL_NAME]
        return CmdList,PM.getDBServList
