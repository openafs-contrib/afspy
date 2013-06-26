from afs.exceptions.UbikError import UbikError
from afs.dao.BaseDAO import BaseDAO, exec_wrapper
from afs.util import afsutil
import ParseUbikPeerDAO as PM


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
            raise UbikError(rc)
        return CmdList,PM.parse_getShortInfo

