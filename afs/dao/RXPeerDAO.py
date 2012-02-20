import re,string,os,sys
import afs.dao.bin
from afs.dao.BaseDAO import BaseDAO

class RXPeerDAO(BaseDAO):

    """
    rxdebug and friends
    """

    RXVerRegEx=re.compile("AFS version:  OpenAFS(.*)built (.*)")

    def __init__(self) :
        BaseDAO.__init__(self)
        return
        
    def getVersionandBuildDate(self, servername, port):
        CmdList=[afs.dao.bin.RXDebugBIN,"-server", "%s"  % servername, "-port", "%s" % port, "-version"]
        rc,output,outerr=self.execute(CmdList)
        if rc :
            return ""
        if len(output) != 2 :
            version="Not readable."
            return ""
        else :
            M=RXVerRegEx.match(output[1])
            if not M :
                version=""
                builddate=""
            else :
                version=M.groups()[0].strip()
                builddate=M.groups()[0].strip()
        return version, builddate


    #Number client active 
    # rxdebug -rxstat
    #  23 server connections, 
    # 636 client connections, 
    # 27 peer structs, 
    # 17 call structs, 
    # 13 free call struct
    
    def getRxConnections(self,servername,port):
        pass
    
    # rxdebug 
    # Free packets: 2765, packet reclaims: 2746, calls: 342929664, used FDs: 63
    # not waiting for packets.
    # 0 calls waiting for a thread
    # 118 threads are idle
    def getThreadStatus(self, servername, port):
        pass
