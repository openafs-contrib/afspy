import string, types
from afs.dao.BaseDAO import BaseDAO, exec_wrapper
import ParseBNodeDAO as PM
from afs.exceptions.BNodeError import BNodeError


class BNodeDAO(BaseDAO) :
    """
    Direct Access Object for a Process (BNode)
    """

    def __init__(self) :
        BaseDAO.__init__(self)
        return

    @exec_wrapper    
    def getRestartTimes(self, servername, _cfg=None):
        """
        return dict telling the restart times
        """
        CmdList=[_cfg.binaries["bos"],"getrestart","-server", "%s"  % servername]
        return CmdList,PM.getRestartTimes

    @exec_wrapper    
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

    @exec_wrapper    
    def addUser(self, servername, userlist, _cfg=None) :
        if type(userlist) == types.ListType :
            usernames = string.join(userlist)
        else :
            usernames = userlist
        CmdList=[_cfg.binaries["bos"],"adduser","-server", "%s"  % servername, "-user",  "%s" % usernames ]
        return CmdList,PM.addUser
    
    @exec_wrapper    
    def removeUser(self, servername, userlist, _cfg=None) :
        if type(userlist) == types.ListType :
            usernames = string.join(userlist)
        else :
            usernames = userlist
        CmdList=[_cfg.binaries["bos"],"removeuser","-server", "%s"  % servername, "-user",  "%s" % usernames ]
        return CmdList,PM.removeUser
    
    @exec_wrapper    
    def getUserList(self, servername, _cfg=None) :
        CmdList=[_cfg.binaries["bos"],"listuser","-server", "%s"  % servername ]
        return CmdList,PM.getUserList
    
    @exec_wrapper    
    def getFileDate(self, servername, filelist, destdir="", _cfg=None) :
        if type(filelist) == types.ListType :
            filenames = string.join(filelist)
        else :
            filenames = filelist
        CmdList=[_cfg.binaries["bos"],"getdate","-server", "%s"  % servername, "-files", "%s" % filenames ]
        if destdir != "" :
            CmdList += ["-dir", "%s" % destdir]
        return CmdList,PM.getFileDate
    
    @exec_wrapper    
    def cmd(self, servername, cmd, _cfg=None) :
        CmdList=[_cfg.binaries["bos"],"cmd","-server", "%s"  % servername ]
        return CmdList,PM.cmd
    
    @exec_wrapper    
    def getLog(self, servername, logfile,_cfg=None) :
        CmdList=[_cfg.binaries["bos"],"getlog","-server", "%s"  % servername ]
        return CmdList,PM.getLog
    
    @exec_wrapper    
    def prune(self, type, servername, _cfg=None) :
        CmdList=[_cfg.binaries["bos"],"prune","-server", "%s"  % servername ]
        return CmdList,PM.pruneLog

    @exec_wrapper    
    def runRestart(self, process, servername, _cfg=None) :
        CmdList=[_cfg.binaries["bos"],"restart","-server", "%s"  % servername ]
        return CmdList,PM.runRestart
    
    @exec_wrapper    
    def runStart(self, process, servername, _cfg=None) :
        CmdList=[_cfg.binaries["bos"],"start","-server", "%s"  % servername ]
        return CmdList,PM.runStart
    
    @exec_wrapper    
    def runShutdown(self, process, servername, _cfg=None) :
        CmdList=[_cfg.binaries["bos"],"shutdown","-server", "%s"  % servername ]
        return CmdList,PM.runShutdown
    
    @exec_wrapper    
    def runStartup(self, process, servername, _cfg=None) :
        CmdList=[_cfg.binaries["bos"],"startup","-server", "%s"  % servername ]
        return CmdList,PM.runStartup
    
    @exec_wrapper    
    def runStop(self, process, servername, _cfg=None) :
        CmdList=[_cfg.binaries["bos"],"stop","-server", "%s"  % servername ]
        return CmdList,PM.runStop

    @exec_wrapper    
    def salvage(self, vid, part, servername, _cfg=None) :
        CmdList=[_cfg.binaries["bos"],"salvageXXX","-server", "%s"  % servername ]
        return CmdList,PM.salvage
    
    @exec_wrapper    
    def status(self, process, servername, _cfg=None) :
        CmdList=[_cfg.binaries["bos"],"status","-server", "%s"  % servername ,"-long"]
        return CmdList,PM.status

    @exec_wrapper    
    def getDBServList(self,servername, _cfg=None) :
        """
        get list of all database-servers known to a given AFS-server
        """
        CmdList=[_cfg.binaries["bos"],"listhosts","-server", "%s"  % servername, "-cell" , "%s" % _cfg.cell]
        return CmdList,PM.getDBServList
