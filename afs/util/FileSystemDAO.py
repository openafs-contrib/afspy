import types,string
from afs.dao.BaseDAO import BaseDAO, exec_wrapper
import FileSystemDAOParse as PM

class FileSystemDAO(BaseDAO) :
    """
    low level access to the FileSystem
    ATM this requires a cache-manager, since most of 
    it is done through an AFS-path
    """

    def __init__(self) :
        BaseDAO.__init__(self)
        return


    @exec_wrapper
    def copyACL(self, fromdir, todir, clear=False,  _cfg=None) :
        CmdList=[_cfg.binaries["fs"],  "copyacl" , "-fromdir" , "%s" % fromdir, "-todir", "%s" % todir ]
        if clear :
            CmdList.append("-clear")
        return CmdList,PM.copyACL


    @exec_wrapper
    def makeMountpoint(self, path, target, toRW=False, _cfg=None) :
        CmdList=[_cfg.binaries["fs"],  "mkmount" , "-dir" , "%s" % path, "-vol", "%s" % target, "-cell",  "%s" % _cfg.cell ]
        if toRW :
            CmdList.append("-rw")
        return CmdList,PM.makeMountpoint
        
    @exec_wrapper
    def removeMountpoint(self, pathlist, _cfg=None) :
        if type(pathlist) == types.ListType :
            pathes = string.join(pathlist)
        else :
            pathes = pathlist
        CmdList=[_cfg.binaries["fs"],  "rmmount" , "-dir" , "%s" % pathes ]
        return CmdList,PM.removeMountpoint
        
    @exec_wrapper
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
        
    @exec_wrapper
    def getCellByPath(self, path, _cfg=None):
        """
        Returns the cell to which a file or directory belongs
        """
        CmdList=[_cfg.binaries["fs"],  "whichcell" , "-path" , "%s" % path ]
        return CmdList,PM.getCellByPath
        
    @exec_wrapper
    def setQuota(self, path, quota, _cfg=None):
        """
        Set a volume-quota by path
        """
        CmdList=[_cfg.binaries["fs"],  "setquota" , "-path" , "%s" % path, "-max", "%s" % quota ]
        return CmdList,PM.setQuota
        
    @exec_wrapper
    def listQuota(self, path, _cfg=None):
        """
        list a volume quota by path
        """
        CmdList=[_cfg.binaries["fs"],  "listquota" , "-path" , "%s" % path ]
        return CmdList,PM.listQuota
    
    @exec_wrapper
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
        
