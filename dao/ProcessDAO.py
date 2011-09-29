import re,string,os,sys
import afs.dao.bin

from afs.model.FileServer import FileServer
from afs.model.Partition import Partition
from afs.util import afsutil


class ProcessDAO() :
    """
    Direct Access Object for a Process (BNode)
    """
    generalRestartRegEX=re.compile("Server (\S+) restarts (?:at)?(.*)")
    binaryRestartRegEX=re.compile("Server (\S+) restarts for new binaries (?:at)?(.*)")

    def __init__(self) :
        return
    
    def getRestartTimes(self, servername):
        CmdList=[afs.dao.bin.BOSBIN,"getrestart","-server", "%s"  % servername]
        rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=0,lethal=1)
        if rc :
            return rc,output,outerr
        if len(output) != 2 :
            return 1, output, outerr
        generalRestart=generalRestartRegEX.match(output[0]).groups()[1]
        binaryRestart=binaryRestartRegEX.match(output[1]).groups()[1]
        return generalRestart, binaryRestart
