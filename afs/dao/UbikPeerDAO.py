from UbikPeerDAOError import UbikPeerDAOError
from afs.dao.BaseDAO import BaseDAO
from afs.util.Executor import exec_wrapper
import UbikPeerDAOParse as PM


class UbikPeerDAO(BaseDAO):
    
    """
    udebug 
    """
    
    def __init__(self) :
        BaseDAO.__init__(self)
        return
    
    @exec_wrapper 
    def getLongInfo(self,name_or_ip,port,_cfg=None) : 
        """
        return dict containing all info from a udebug -long
        """
        CmdList=[_cfg.binaries["udebug"],"-server", "%s"  % name_or_ip, "-port", "%s" % port,  "-long"]
        return CmdList,PM.parse_getLongInfo
 
    @exec_wrapper 
    def getShortInfo(self,name_or_ip,port,_cfg=None) :
        """
        return dict containing all info from a simple udebug
        """   
        CmdList=[_cfg.binaries["udebug"],"-server", "%s"  % name_or_ip, "-port", "%s" % port,  "-long"]
        rc,output,outerr=self.execute(CmdList) 
        if rc :
            raise UbikPeerDAOError(rc)
        return CmdList,PM.parse_getShortInfo

