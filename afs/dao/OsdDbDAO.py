from afs.dao.BaseDAO import BaseDAO,execwrapper
import OsdDbDAO_parse as PM

class OsdDbDAO(BaseDAO):
    
    """
    stuff to do with the osddb
    """

    def __init__(self) :
        BaseDAO.__init__(self)
        return
     
    @execwrapper   
    def getStatistics(self,srv, _cfg=None):
        """
        get RPC-statistics of OsdDb-Server
        """
        CmdList=[_cfg.binaries["osd"], "osddbstatistics","-server","%s" % srv,"-cell",  "%s" % _cfg.CELL_NAME ]
        return CmdList,PM.getStatistics

