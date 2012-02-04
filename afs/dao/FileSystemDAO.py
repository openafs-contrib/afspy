import re,string,os,sys
import afs.dao.bin
from afs.util import afsutil
from afs.exceptions.FSError import FSError

class FileSystemDAO() :
    """
    low level access to the FileSystem
    ATM this requires a cache-manager, since most of 
    it is done through an AFS-path
    """
    def __init__(self) :
        pass
            

    def  makeMountpoint(self, path, target) :
        return
        
    def removeMountpoint(self, path) :
        return
        
    def listMountpoint(self, path):
        """
        Return target volume of a mount point
        """
        mountpoint=""
        return mountpoint
        
    def getCellByPath(self, path):
        """
        Returns the cell to which a file or directory belongs
        """
        cellname=""
        return cellname
        
    def setQuota(self, path):
        """
        Set a volume-quota by path
        """
        return
        
    def listQuota(self, path):
        """
        list a volume quota by path
        """
        quota=-1
        return quota
    
    def returnVolumeByPath(self, path):
        """
        Basically a fs examine
        """
        volume=""
        return volume
        
