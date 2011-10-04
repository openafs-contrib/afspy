import re,string,os,sys
import afs.dao.bin

class CacheManagerDAO():
    """
    cmdebug and friends
    """
    
    def __init__(self):
        return
    
    def wscell(self, init):
        """
        Returns the name of the cell to which a machine belongs
        """
        cellname=""
        return cellname
        
    def flushall(self):
        """
        Force the AFS Cache Manager to discard all data
        """
        return
    
    def flushvolume(self):
        """
        Forces the Cache Manager to discard cached data from a volume
        """
        return
    
    def flushmount(self):
        """
        Forces the Cache Manager to discard a mount point
        """
        return
        
    def flush(self, path):
        """
        Forces the Cache Manager to discard a cached file or directory
        """
        return
    
    def listCellAlias(self, path):
        """
        list defined Cell aliases
        """
        return
        
    def newCellAlias(self, path):
        """
        set a new Cell alias
        """
        return
        
