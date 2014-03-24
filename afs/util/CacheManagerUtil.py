"""
common cache-manager operations
"""
from afs.util.Executor import exec_wrapper
import ParseCacheManagerUtil as PM
from BaseUtil import BaseUtil

class CacheManagerUtil(BaseUtil) :
        
    @exec_wrapper 
    def flush_all(self, _cfg=None):
        """
        Force the AFS Cache Manager to discard all data
        """
        CmdList=[_cfg.binaries["fs"] , "flushall"]
        return CmdList,PM.parse_flushall
    
    @exec_wrapper 
    def flush_volume(self, path, _cfg=None):
        """
        Forces the Cache Manager to discard cached data from a volume
        """
        CmdList=[_cfg.binaries["fs"] , "flushvolume", "%s" % path]
        return CmdList,PM.parse_flushvolume
    
    @exec_wrapper 
    def flush_mount(self, path, _cfg=None):
        """
        Forces the Cache Manager to discard a mount point
        """
        CmdList=[_cfg.binaries["fs"] , "flushmount", "-path", "%s"%path]
        return CmdList, PM.parse_flushmount
        
    @exec_wrapper 
    def flush(self, path, _cfg=None):
        """
        Forces the Cache Manager to discard a cached file or directory
        """
        CmdList=[_cfg.binaries["fs"] , "flush", "-path", "%s" % path]
        return CmdList, PM.parse_flush

    @exec_wrapper 
    def get_ws_cell(self, cache_manager, _cfg=None):
        """
        Returns the name of the cell to which a machine belongs
        """
        CmdList=[_cfg.binaries["fs"] , "wscell"]
        return CmdList, PM.pull_ws_cell
    
    @exec_wrapper 
    def get_cell_aliases(self, cache_manager, _cfg=None):
        """
        list defined Cell aliases
        """
        CmdList=[_cfg.binaries["fs"] , "listaliases"]
        return CmdList, PM.pull_cell_aliases
        
    @exec_wrapper 
    def new_cell_alias(self, cache_manager, alias, _cfg=None):
        """
        set a new Cell alias
        """
        CmdList=[_cfg.binaries["fs"] , "newaliases", "-alias" "%s"  % alias,"-name" % _cfg.cell]
        return CmdList,PM.pull_cell_alias
