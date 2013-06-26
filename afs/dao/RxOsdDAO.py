from afs.dao.BaseDAO import BaseDAO, exec_wrapper
import ParseRxOsdDAO as PM
from afs.exceptions.RxOsdError import RxOsdError

class RxOsdDAO(BaseDAO):
    
    """
    stuff to do with rxosd-servers
    """
    
    def __init__(self) :
        BaseDAO.__init__(self)
        return
    @exec_wrapper  
    def examine(self, osd_id, fid,_cfg=None):
        """
        examine an object 
        """
        CmdList=[_cfg.binaries["osd"], "examine","-osd","%s" % osd_id,"-fid","%s" % fid, "-cell",  "%s" % _cfg.CELL_NAME ]
        return CmdList,PM.parse_examine
        
    @exec_wrapper  
    def getFetchQueue(self, osd_id=-1,  _cfg=None ):
        """
        query fetchqueues of archival osd.
        """
        CmdList=[_cfg.binaries["osd"], "fetchq", "-cell",  "%s" % _cfg.CELL_NAME ]
        if osd_id != -1:
            CmdList += ["-name" , "%s" % osd_id]
        return CmdList,PM.parse_getFetchQueue
    
    @exec_wrapper  
    def getListOfServerSettings(self,osd_id,_cfg=None):
        """
        query Servers for its tuneables
        """
        CmdList=[_cfg.binaries["osd"], "whichvariables","-server", "%s" % osd_id, "-cell",  "%s" % _cfg.CELL_NAME ]
        return CmdList,PM.parse_getListOfServerSettings
 
    @exec_wrapper  
    def getServerSetting(self,osd_id,key,_cfg=None):
        """
        query Servers for it tuneables
        """
        CmdList=[_cfg.binaries["osd"], "getvariable","-server", "%s" % osd_id,"-variable","%s" % key, "-cell",  "%s" % _cfg.CELL_NAME ]
        return CmdList,PM.parse_getServerSetting
   
    @exec_wrapper  
    def setServerSetting(self,osd_id,key,value,_cfg=None) :
        """
        set Server tunable. Verifies result
        """ 
        CmdList=[_cfg.binaries["osd"], "setvariable","-server", "%s" % osd_id, "-variable", "%s" % key, "-value" % value, "-cell",  "%s" % _cfg.CELL_NAME ]
        return CmdList,PM.parse_setServerSetting

    @exec_wrapper  
    def getObjectsofVolumeByOsd(self,osd_id,vid,lun,_cfg=None) :
        """
        get all objects of a given volume on an RxOsd. 
        Optional: define lun on RxOsd
        """ 
        CmdList=[_cfg.binaries["osd"], "objects", "-osd","%s" % osd_id, "-volume", "%s" % vid, "-cell",  "%s" % _cfg.CELL_NAME ]
        if osd_id :
            CmdList += ["-lun" , "%s" % lun]
        return CmdList,PM.parse_getObjectsofVolumeByOsd

    @exec_wrapper  
    def getStatistics(self,osd_id,extended=False,_cfg=None) :
        """
        get RPC-statistics of RxOsd-sever
        """
        CmdList=[_cfg.binaries["osd"], "statistics", "-osd","%s" % osd_id, "-cell",  "%s" % _cfg.CELL_NAME ]
        if extended :
            CmdList += ["-verbose" ]
        return CmdList,PM.parse_getStatistics

    @exec_wrapper  
    def resetStatistics(self,osd_id,_cfg=None) :
        """
        reset RPC-statistics of a RxOsd-sever
        """
        CmdList=[_cfg.binaries["osd"], "statistics", "-osd","%s" % osd_id,"-reset", "-cell",  "%s" % _cfg.CELL_NAME ]
        return CmdList,PM.parse_resetStatistics

    @exec_wrapper  
    def getActiveThreads(self,osd_id,extended=False,_cfg=None) :
        """
        get list of active threads of a RxOsd-sever
        """
        CmdList=[_cfg.binaries["osd"], "threads", "-server","%s" % osd_id, "-cell",  "%s" % _cfg.CELL_NAME ]
        if extended :
            CmdList += ["-verbose" ]
        return CmdList,PM.parse_getActiveThreads
   
    @exec_wrapper  
    def getWipeCandidates(self,osd_id,_cfg=None,lun=-1,maxNum=100,criteria="atime",minSizeMB=0) :
        CmdList=[_cfg.binaries["osd"], "threads", "-server","%s" % osd_id, "-max" , "%s" % maxNum, "-minMB", "%s" % minSizeMB, "-cell",  "%s" % _cfg.CELL_NAME ]
        if lun != -1 :
            CmdList += ["-lun", "%s" % lun ]
        if criteria == "atime" :
            CmdList += ["-crit" , "0"]
        elif criteria == "size" :
            CmdList += ["-crit" , "1"]
        elif criteria == "sizeXage" :
            CmdList += ["-crit" , "2"]
        else :
            raise RxOsdError("Error", "invalid criteria %s" % criteria)
        return CmdList,PM.parse_getWipeCandidates
            
