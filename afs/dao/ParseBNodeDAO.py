import re
from afs.exceptions.BNodeError import BNodeError

generalRestartRegEX=re.compile("Server (\S+) restarts (?:at)?(.*)")
binaryRestartRegEX=re.compile("Server (\S+) restarts for new binaries (?:at)?(.*)")
DBServerRegEx=re.compile("Host (\d+) is (\S+)")

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

def getRestartTimes(rc,output,outerr,parseParamList,Logger):
    if rc :
        raise BNodeError( outerr, output)
    
    if len(output) != 2 :
        raise BNodeError( outerr, output)
    
    st = {}
    st["general"]=generalRestartRegEX.match(output[0]).groups()[1].strip()
    st["binary"]=binaryRestartRegEX.match(output[1]).groups()[1].strip()
    return st

def getDBServList(rc,output,outerr,parseParamList,Logger) :
    if rc :
       raise BNodeError(outerr, output)
    DBServers=[]
    for line in output :
        mObj=DBServerRegEx.match(line)
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


def status(rc,output,outerr,parseParamList,Logger):
    if rc :
        raise BNodeError( outerr, output)
    return

def salvage(rc,output,outerr,parseParamList,Logger):
    if rc :
        raise BNodeError( outerr, output)
    return

def runStop(rc,output,outerr,parseParamList,Logger):
    if rc :
        raise BNodeError( outerr, output)
    return

def setRestartTimes(rc,output,outerr,parseParamList,Logger):
    if rc :
        raise BNodeError( outerr, output)
    return

def addUser(rc,output,outerr,parseParamList,Logger):
    if rc :
        raise BNodeError( outerr, output)
    return

def removeUser(rc,output,outerr,parseParamList,Logger):
    if rc :
        raise BNodeError( outerr, output)
    return

def getUserList(rc,output,outerr,parseParamList,Logger):
    if rc :
        raise BNodeError( outerr, output)
    return

def getFileDate(rc,output,outerr,parseParamList,Logger):
    if rc :
        raise BNodeError( outerr, output)
    return

def cmd(rc,output,outerr,parseParamList,Logger):
    if rc :
        raise BNodeError( outerr, output)
    return

def getLog(rc,output,outerr,parseParamList,Logger):
    if rc :
        raise BNodeError( outerr, output)
    return

def pruneLog(rc,output,outerr,parseParamList,Logger):
    if rc :
        raise BNodeError( outerr, output)
    return

def runRestart(rc,output,outerr,parseParamList,Logger):
    if rc :
        raise BNodeError( outerr, output)
    return

def runStart(rc,output,outerr,parseParamList,Logger):
    if rc :
        raise BNodeError( outerr, output)
    return

def runShutdown(rc,output,outerr,parseParamList,Logger):
    if rc :
        raise BNodeError( outerr, output)
    return

def runStartup(rc,output,outerr,parseParamList,Logger):
    if rc :
        raise BNodeError( outerr, output)
    return
