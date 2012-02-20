import re,string,os,sys
import afs.dao.bin
from afs.dao.BaseDAO import BaseDAO

class OsdDbDAO(BaseDAO):
    
    """
    stuff to do with the osddb
    """

    def __init__(self) :
        BaseDAO.__init__(self)
        return
        
    def getStatistics(self,srv, cellname,token):
        """
        get RPC-statistics of OsdDb-Server
        """
        CmdList=[afs.dao.bin.OSDBIN, "osddbstatistics","-server","%s" % srv,"-cell",  "%s" % cellname ]
        rc,output,outerr=self.execute(CmdList)
        if rc:
            raise OsdDbError("Error", outerr)
        
        statDict={}
        
        return statDict
