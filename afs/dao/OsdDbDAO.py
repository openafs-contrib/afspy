import re,string,os,sys
import afs.dao.bin

class OsdDbDAO():
    
    """
    stuff to do with the osddb
    """
    def __init__(self):
        pass
        
    def getStatistics(self,srv, cellname,token):
        """
        get RPC-statistics of OsdDb-Server
        """
        CmdList=[afs.dao.bin.OSDBIN, "osddbstatistics","-server","%s" % srv,"-cell",  "%s" % cellname ]
        rc,output,outerr=afs.dao.bin.execute(CmdList)
        if rc:
            raise OsdDbError("Error", outerr)
        
        statDict={}
        
        return statDict
