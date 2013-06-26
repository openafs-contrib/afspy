from afs.dao.BaseDAO import BaseDAO, exec_wrapper
import ParseCacheManagerDAO as PM

class CacheManagerDAO(BaseDAO):
    """
    cmdebug and friends
    """
    
    def __init__(self) :
        BaseDAO.__init__(self)
        return

    @exec_wrapper 
    def getWSCell(self, _cfg=None):
        """
        Returns the name of the cell to which a machine belongs
        """
        CmdList=[_cfg.binaries["fs"] , "wscell"]
        return CmdList,PM.parse_getWsCell
        
    @exec_wrapper 
    def flushall(self, _cfg=None):
        """
        Force the AFS Cache Manager to discard all data
        """
        CmdList=[_cfg.binaries["fs"] , "flushall"]
        return CmdList,PM.parse_flushall
    
    @exec_wrapper 
    def flushvolume(self, path, _cfg=None):
        """
        Forces the Cache Manager to discard cached data from a volume
        """
        CmdList=[_cfg.binaries["fs"] , "flushvolume", "%s" % path]
        return CmdList,PM.parse_flushvolume
    
    @exec_wrapper 
    def flushmount(self, path, _cfg=None):
        """
        Forces the Cache Manager to discard a mount point
        """
        CmdList=[_cfg.binaries["fs"] , "flushmount", "-path", "%s"%path]
        return CmdList,PM.parse_flushmount
        
    @exec_wrapper 
    def flush(self, path, _cfg=None):
        """
        Forces the Cache Manager to discard a cached file or directory
        """
        CmdList=[_cfg.binaries["fs"] , "flush", "-path", "%s" % path]
        return CmdList,PM.parse_flush
    
    @exec_wrapper 
    def getCellAliases(self, _cfg=None):
        """
        list defined Cell aliases
        """
        CmdList=[_cfg.binaries["fs"] , "listaliases"]
        return CmdList,PM.parse_getCellAliases
        
    @exec_wrapper 
    def newCellAlias(self, alias, _cfg=None):
        """
        set a new Cell alias
        """
        CmdList=[_cfg.binaries["fs"] , "newaliases", "-alias" "%s"  % alias,"-name" % _cfg.CELL_NAME]
        return CmdList,PM.parse_newCellAlias
