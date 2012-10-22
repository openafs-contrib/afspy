import types,string
from afs.dao.BaseDAO import BaseDAO,execwrapper
import FileSystemDAO_parse as PM

class FileSystemDAO(BaseDAO) :
    """
    low level access to the FileSystem
    ATM this requires a cache-manager, since most of 
    it is done through an AFS-path
    """

    def __init__(self) :
        BaseDAO.__init__(self)
        return

    @execwrapper
    def makeMountpoint(self, path, target, _cfg=None) :
        CmdList=[_cfg.binaries["fs"],  "makemount" , "-dir" , "%s" % path, "-vol", "%s" % target, "-cell",  "%s" % _cfg.CELL_NAME ]
        return CmdList,PM.makeMountpoint
        
    @execwrapper
    def removeMountpoint(self, pathlist, _cfg=None) :
        if type(pathlist) == types.ListType :
            pathes = string.join(pathlist)
        else :
            pathes = pathlist
        CmdList=[_cfg.binaries["fs"],  "rmmount" , "-dir" , "%s" % pathes ]
        return CmdList,PM.removeMountpoint
        
    @execwrapper
    def listMountpoint(self, pathlist, _cfg=None):
        """
        Return target volume of a mount point
        """
        if type(pathlist) == types.ListType :
            pathes = string.join(pathlist)
        else :
            pathes = pathlist
        CmdList=[_cfg.binaries["fs"],  "lsmount" , "-dir" , "%s" % pathes ]
        return CmdList,PM.listMountpoint
        
    @execwrapper
    def getCellByPath(self, path, _cfg=None):
        """
        Returns the cell to which a file or directory belongs
        """
        CmdList=[_cfg.binaries["fs"],  "whichcell" , "-path" , "%s" % path ]
        return CmdList,PM.getCellByPath
        
    @execwrapper
    def setQuota(self, path, quota, _cfg=None):
        """
        Set a volume-quota by path
        """
        CmdList=[_cfg.binaries["fs"],  "setquota" , "-path" , "%s" % path, "-max", "%s" % quota ]
        return CmdList,PM.setQuota
        
    @execwrapper
    def listQuota(self, path, _cfg=None):
        """
        list a volume quota by path
        """
        CmdList=[_cfg.binaries["fs"],  "listquota" , "-path" , "%s" % path ]
        return CmdList,PM.listQuota
    
    @execwrapper
    def returnVolumeByPath(self, pathlist, _cfg=None):
        """
        Basically a fs examine
        """
        if type(pathlist) == types.ListType :
            pathes = string.join(pathlist)
        else :
            pathes = pathlist
        CmdList=[_cfg.binaries["fs"],  "examine" , "-path" , "%s" % pathes ]
        return CmdList,PM.returnVolumeByPath
        
