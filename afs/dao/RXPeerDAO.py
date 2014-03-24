from afs.dao.BaseDAO import BaseDAO
from afs.util.Executor import exec_wrapper
import RXPeerDAOParse as PM

class RXPeerDAO(BaseDAO):

    """
    rxdebug and friends
    """

    def __init__(self) :
        BaseDAO.__init__(self)
        return
    
    @exec_wrapper    
    def getVersionandBuildDate(self, servername, port,_cfg=None):
        CmdList=[_cfg.binaries["rxdebug"],"-server", "%s"  % servername, "-port", "%s" % port, "-version"]
        return CmdList,PM.parse_getVersionandBuildDate

