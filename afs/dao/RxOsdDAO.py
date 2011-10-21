import re,string,os,sys
import afs.dao.bin

class RxOsdDAO():
    
    """
    stuff to do with rxosd-servers
    """
    
    def __init__(self):
        pass
    
    def examine(self, osd_id, fid,cellname,token,lun=0):
        """
        examine an object 
        """
        CmdList=[afs.dao.bin.OSDBIN, "examine","-osd","%s" % osd_id,"-fid","%s" % fid, "-cell",  "%s" % cellname ]
        rc,output,outerr=afs.dao.bin.execute(CmdList)
        if rc:
            raise RxOsdError("Error", outerr)
        
        obj_dict={}
        
        return obj_dict
        
    def getFetchQueue(self, cellname,token, osd_id=None,):
        """
        query fetchqueues of archival osd.
        """
        CmdList=[afs.dao.bin.OSDBIN, "fetchq", "-cell",  "%s" % cellname ]
        if osd_id :
            CmdList += ["-name" , "%s" % osd_id]
        rc,output,outerr=afs.dao.bin.execute(CmdList)
        if rc:
            raise RxOsdError("Error", outerr)
        FetchQDict={}
        return FetchQDict
    
    def getListOfServerSettings(self,osd_id,cellname,token):
        """
        query Servers for it tuneables
        """
        CmdList=[afs.dao.bin.OSDBIN, "whichvariables","-server", "%s" % osd_id, "-cell",  "%s" % cellname ]
        rc,output,outerr=afs.dao.bin.execute(CmdList)
        if rc:
            raise RxOsdError("Error", outerr)
        settingsList=[]
        return settingsList       
 
    def getServerSetting(self,osd_id,key,cellname,token):
        """
        query Servers for it tuneables
        """
        CmdList=[afs.dao.bin.OSDBIN, "getvariable","-server", "%s" % osd_id,"-variable","%s" % key, "-cell",  "%s" % cellname ]
        rc,output,outerr=afs.dao.bin.execute(CmdList)
        if rc:
            raise RxOsdError("Error", outerr)
        value=""
        return value
   
    def setServerSettings(self,osd_id,key,value,cellname,token) :
        """
        set Server tunable. Verifies result
        """ 
        CmdList=[afs.dao.bin.OSDBIN, "setvariable","-server", "%s" % osd_id, "-variable", "%s" % key, "-value" % value, "-cell",  "%s" % cellname ]
        rc,output,outerr=afs.dao.bin.execute(CmdList)
        if rc:
            raise RxOsdError("Error", outerr)
        newSettings=self.getServeSettings(self,osd_id,key,cellname,token)
        if newSettings[key] == value :
            return value
        else :
            raise RxOsdError("Error", "failed to set variable")

    def getObjectsofVolumeByOsd(self,osd_id,vid,lun,cellname,token) :
        """
        get all objects of a given volume on an RxOsd. 
        Optional: define lun on RxOsd
        """ 
        CmdList=[afs.dao.bin.OSDBIN, "objects", "-osd","%s" % osd_id, "-volume", "%s" % vid, "-cell",  "%s" % cellname ]
        if osd_id :
            CmdList += ["-lun" , "%s" % lun]
        rc,output,outerr=afs.dao.bin.execute(CmdList)
        if rc:
            raise RxOsdError("Error", outerr)
        obj_list=[]
        return obj_list

    def getStatistics(self,osd_id,cellname,token,extended=False) :
        """
        get RPC-statistics of RxOsd-sever
        """
        CmdList=[afs.dao.bin.OSDBIN, "statistics", "-osd","%s" % osd_id, "-cell",  "%s" % cellname ]
        if extended :
            CmdList += ["-verbose" ]
        rc,output,outerr=afs.dao.bin.execute(CmdList)
        if rc:
            raise RxOsdError("Error", outerr)
        statDict={}
        return statDict

    def resetStatistics(self,osd_id,cellname,token) :
        """
        reset RPC-statistics of a RxOsd-sever
        """
        CmdList=[afs.dao.bin.OSDBIN, "statistics", "-osd","%s" % osd_id,"-reset", "-cell",  "%s" % cellname ]
        rc,output,outerr=afs.dao.bin.execute(CmdList)
        if rc:
            raise RxOsdError("Error", outerr)
        return 

    def getActiveThreads(self,osd_id,cellname,token) :
        """
        get list of active threads of a RxOsd-sever
        """
        CmdList=[afs.dao.bin.OSDBIN, "threads", "-server","%s" % osd_id, "-cell",  "%s" % cellname ]
        if extended :
            CmdList += ["-verbose" ]
        rc,output,outerr=afs.dao.bin.execute(CmdList)
        if rc:
            raise RxOsdError("Error", outerr)
        threadList=[]
        return threadList
   
    def getWipeCandidates(self,osd_id,cellname,token,lun=None,maxNum=100,criteria="atime",minSizeMB=0) :
        CmdList=[afs.dao.bin.OSDBIN, "threads", "-server","%s" % osd_id, "-max" , "%s" % maxNum, "-minMB", "%s" % minSizeMB, "-cell",  "%s" % cellname ]
        if lun :
            CmdList += ["-lun", "%s" % lun ]
        if criteria == "atime" :
            CmdList += ["-crit" , "0"]
        elif criteria == "size" :
            CmdList += ["-crit" , "1"]
        elif criteria == "sizeXage" :
            CmdList += ["-crit" , "2"]
        else :
            raise RxOsdError("Error", "invalid criteria %s" % criteria)
            
        rc,output,outerr=afs.dao.bin.execute(CmdList)
        if rc:
            raise RxOsdError("Error", outerr)
        candList=[]
        return candList
