import re,string,os,sys
import afs.dao.bin
from afs.exceptions.CMError import CMError
from afs.dao.BaseDAO import BaseDAO

class CacheManagerDAO(BaseDAO):
    """
    cmdebug and friends
    """
    
    def __init__(self) :
        BaseDAO.__init__(self)
        return
    
    def getWSCell(self):
        """
        Returns the name of the cell to which a machine belongs
        """
        CmdList=[afs.dao.bin.FSBIN , "wscell"]
        rc,output,outerr=self.execute(CmdList)
        if rc :
            raise CMError
        # parse "This workstation belongs to cell 'beolink.org'"
        cellname=output[0].split()[5].replace("'", "")
        return cellname
        
    def flushall(self):
        """
        Force the AFS Cache Manager to discard all data
        """
        CmdList=[afs.dao.bin.FSBIN , "flushall"]
        rc,output,outerr=self.execute(CmdList)
        if rc :
            raise CMError
        return
    
    def flushvolume(self, path):
        """
        Forces the Cache Manager to discard cached data from a volume
        """
        CmdList=[afs.dao.bin.FSBIN , "flushvolume", "%s" % path]
        rc,output,outerr=self.execute(CmdList)
        if rc :
            raise CMError
        return
    
    def flushmount(self, path):
        """
        Forces the Cache Manager to discard a mount point
        """
        CmdList=[afs.dao.bin.FSBIN , "flushmount", "-path", "%s"%path]
        rc,output,outerr=self.execute(CmdList)
        if rc :
            raise CMError
        return
        
    def flush(self, path):
        """
        Forces the Cache Manager to discard a cached file or directory
        """
        CmdList=[afs.dao.bin.FSBIN , "flush", "-path", "%s" % path]
        rc,output,outerr=self.execute(CmdList)
        if rc :
            raise CMError
        return
    
    def getCellAliases(self):
        """
        list defined Cell aliases
        """
        CmdList=[afs.dao.bin.FSBIN , "listaliases"]
        rc,output,outerr=self.execute(CmdList)
        if rc :
            raise CMError
        return output
        
    def newCellAlias(self, alias, cellname):
        """
        set a new Cell alias
        """
        CmdList=[afs.dao.bin.FSBIN , "newaliases", "-alias" "%s"  % alias,"-name" % cellname]
        rc,output,outerr=self.execute(CmdList)
        if rc :
            raise CMError
        return
