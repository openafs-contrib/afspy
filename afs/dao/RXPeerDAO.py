import re,string,os,sys
import afs.dao.bin

class RXPeerDAO():

    """
    rxdebug and friends
    """

    RXVerRegEx=re.compile("AFS version:  OpenAFS(.*)built (.*)")

    def __init__(self):
        pass
        
    def getVersionandBuildDate(self, servername, port):
        CmdList=[afs.dao.bin.RXDebugBIN,"-server", "%s"  % servername, "-port", "%s" % port, "-version"]
        rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=0,lethal=1)
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
