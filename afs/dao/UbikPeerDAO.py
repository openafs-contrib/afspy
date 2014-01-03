"""
Low-level implementation for methods
dealing with a ubik database server.
"""
from afs.dao.BaseDAO import BaseDAO
from afs.util.Executor import exec_wrapper
import afs.dao.UbikPeerDAOParse as PM


class UbikPeerDAO(BaseDAO):
    
    """
    udebug 
    """
    
    def __init__(self) :
        BaseDAO.__init__(self)
        return
    
    @exec_wrapper 
    def get_long_info(self, name_or_ip, port, _cfg=None) : 
        """
        return dict containing all info from a udebug -long
        """
        command_list = [_cfg.binaries["udebug"], "-server", "%s"  % \
                        name_or_ip, "-port", "%s" % port, "-long"]
        return command_list, PM.get_long_info
 
    @exec_wrapper 
    def get_short_info(self, name_or_ip, port, _cfg=None) :
        """
        return dict containing all info from a simple udebug
        """   
        command_list = [_cfg.binaries["udebug"], "-server", "%s"  % \
                        name_or_ip, "-port", "%s" % port, "-long"]
        return command_list, PM.get_short_info

