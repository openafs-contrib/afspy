from afs.lla.BaseLLA import BaseLLA, exec_wrapper
import RXPeerLLAParse as PM

class RXPeerLLA(BaseLLA):

    """
    rxdebug and friends
    """

    def __init__(self) :
        BaseLLA.__init__(self)
        return
    
    @exec_wrapper    
    def getVersionandBuildDate(self, servername, port,_cfg=None):
        CmdList=[_cfg.binaries["rxdebug"],"-server", "%s"  % servername, "-port", "%s" % port, "-version"]
        return CmdList,PM.parse_getVersionandBuildDate

