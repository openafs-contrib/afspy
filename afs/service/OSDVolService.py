from afs.model.Volume import Volume
from afs.model.ExtendedVolumeAttributes_OSD import ExtVolAttr_OSD
from afs.model.VolumeGroup import VolumeGroup
from afs.service.BaseService import BaseService
from afs.service.VolService import VolService
from afs.service.FsService import FsService
from afs.exceptions.VolError import VolError
from afs.exceptions.AfsError import AfsError
from afs.util import afsutil
import afs

emptyStorageUsageDict={'storageUsage': {'detailed': [], 'fileserver': {'Data': -1, 'numFiles': -1}, 'archival': {'Data': -1, 'numFiles': -1}, 'online': {'Data': -1, 'numFiles': -1}}, 'withoutCopy': {'detailed': [], 'fileserver': {'Data': -1, 'numFiles': -1}, 'archival': {'Data': -1, 'numFiles': -1}, 'online': {'Data': -1, 'numFiles': -1}}, 'logical': [{'binData': -1, 'lowerSize': 0, 'upperSize': 4096, 'numFiles': -1}, {'binData': -1, 'lowerSize': 4096, 'upperSize': 8192, 'numFiles': -1}, {'binData': -1, 'lowerSize': 8192, 'upperSize': 16384, 'numFiles': -1}, {'binData': -1, 'lowerSize': 16384, 'upperSize': 32768, 'numFiles': -1}, {'binData': -1, 'lowerSize': 32768, 'upperSize': 65536, 'numFiles': -1}, {'binData': -1, 'lowerSize': 65536, 'upperSize': 131072, 'numFiles': -1}, {'binData': -1, 'lowerSize': 131072, 'upperSize': 262144, 'numFiles': 1}, {'binData': -1, 'lowerSize': 262144, 'upperSize': 524288, 'numFiles': -1}, {'binData': -1, 'lowerSize': 524288, 'upperSize': 1048576, 'numFiles': -1}, {'binData': -1, 'lowerSize': 1048576, 'upperSize': 2097152, 'numFiles': -1}, {'binData': -1, 'lowerSize': 2097152, 'upperSize': 4194304, 'numFiles': -1}, {'binData': -1, 'lowerSize': 4194304, 'upperSize': 8388608, 'numFiles': -1}, {'binData': -1, 'lowerSize': 8388608, 'upperSize': 16777216, 'numFiles': -1}, {'binData': -1, 'lowerSize': 16777216, 'upperSize': 33554432, 'numFiles': -1}, {'binData': -1, 'lowerSize': 33554432, 'upperSize': 67108864, 'numFiles': -1}, {'binData': -1, 'lowerSize': 67108864, 'upperSize': 134217728, 'numFiles': -1}, {'binData': -1, 'lowerSize': 134217728, 'upperSize': 268435456, 'numFiles': -1}, {'binData': -1, 'lowerSize': 268435456, 'upperSize': 536870912, 'numFiles': -1}], 'totals': {'storageUsage': {'Data': -1, 'numFiles': -1}, 'withoutCopy': {'Data': -1, 'numFiles': -1}, 'logical': {'Data': -1, 'numFiles': -1}}}

class OSDVolService (VolService):
    """
    Provides Service about a Volume management.
    The cellname is set in the methods so that we 
    can use this for more than one cell.
    Overly to VolService for adding OSD functionality
    """
    
    def __init__(self, conf=None):
        BaseService.__init__(self, conf, DAOList=["vol","osdvol","fs"])

    """
    Retrieve Volume Group.
    Returns dict "RW": RWVolObj, "RO": [ROVolObj1, ROVolObj2, ...]
    Overridden from VolumeService
    """

    def getVolGroup(self, id, _user="", cached=True):
        self.Logger.debug("getVolGroup: entering with id=%s" % id) 
        VolGroupDict={"RW" : [], "RO" : [], "BK": []}
        if cached :
            VolList=self.DBManager.getFromCache(Volume,vid=id,mustBeUnique=False)
            if VolList != None :
                parentID=VolList[0].parentID
                VolList=self.DBManager.getFromCache(Volume,parentID=parentID,mustBeUnique=False)
                for v in VolList :
                    if v.type == "RW" :
                        VolGroupDict["RW"].append(v)  
                    elif v.type == "RO" : 
                        VolGroupDict["RO"].append(v)  
                    elif v.type == "BK" :
                        VolGroupDict["BK"].append(v) 
                    else :
                        raise AfsError("getVolGroup: invalid volume type encountered: %s" % v.type)
                return VolGroupDict 

        vol = self._osdvolDAO.getVolume(id, _cfg=self._CFG, _user=_user)
        if vol == None : 
            self.Logger.debug("getVolGroup: returning live: None")
            return None
        self.Logger.debug("getVolGroup: got vol=%s" % vol)
        if vol[0]["vid"] == vol[0]["parentID"] : # is RW
            rwvol = vol
            try :
                rovol = self._osdvolDAO.getVolume(vol[0]["cloneID"], _cfg=self._CFG, _user=_user)
            except : 
                rovol = []
            try :           
                bkvol = self._osdvolDAO.getVolume(vol[0]["backupID"], _cfg=self._CFG, _user=_user)  
            except :
                bkvol = []
        elif vol[0]["vid"] == vol[0]["cloneID"] : # is RO
            rovol = vol
            try :
                rwvol = self._osdvolDAO.getVolume(vol[0]["parentID"], _cfg=self._CFG, _user=_user)
            except :
                rwvol = []
            try :
                bkvol = self._osdvolDAO.getVolume(vol[0]["backupID"], _cfg=self._CFG, _user=_user)  
            except :
                bkvol = []
        elif vol[0]["vid"] == vol[0]["backupID"] : # is RO
            bkvol = vol
            try :
                rwvol = self._osdvolDAO.getVolume(vol[0]["parentID"], _cfg=self._CFG, _user=_user)
            except :
                rwvol = []
            try :           
                rovol = self._osdvolDAO.getVolume(vol[0]["cloneID"], _cfg=self._CFG, _user=_user)  
            except :
                rovol = []
        else : # error
            raise AfsError("getVolGroup: error parsing intrenal vollist: %s" % vol)

        self.Logger.debug("getVolGroup: got rwvol=%s,rovol=%s,bkvol=%s" % (rwvol,rovol,bkvol))
        VolGroupDict["RW"] = self.getVolume(int(rwvol[0]["vid"]),serv=rwvol[0]["servername"],cached=False)
        VolGroupDict["RO"] = self.getVolume(int(rovol[0]["vid"]),cached=False)
        #VolGroupDict["BK"] = self.getVolume(bkvol[0]["vid"])   
        return VolGroupDict
        

    """
    Retrieve Volume Information by Name or ID
    Overridden from VolService.
    """
    def getVolume(self, name_or_id, serv=None,  _user="", cached=False):
        self.Logger.debug("Entering with name_or_id=%s, serv=%s, cached=%s" % (name_or_id, serv, cached) )
        VolList = []
        if cached :
            if serv != None :
                serv_uuid=afs.LookupUtil[self._CFG.CELL_NAME].getFSUUID(serv,self._CFG,cached=True)
                # need function in util name_or_ip and name_or_id?
                if afsutil.isName(name_or_id) :
                    vol=self.DBManager.getFromCache(Volume,name=name_or_id,serv_uuid=serv_uuid)
                else :
                    vol=self.DBManager.getFromCache(Volume,vid=name_or_id,serv_uuid=serv_uuid)
                VolList.append(vol)
            else :
                if afsutil.isName(name_or_id) :
                    VolList=self.DBManager.getFromCache(Volume,name=name_or_id,mustBeUnique=False)
                else :
                    VolList=self.DBManager.getFromCache(Volume,vid=name_or_id,mustBeUnique=False)
                self.Logger.debug("OSDgetVolume: VolList=%s" % VolList)
            for vol in VolList :
                vol.ExtAttr=self.getExtVolAttr(vol.vid)
                vol.OsdAttr=self.DBManager.getFromCache(ExtVolAttr_OSD,vid=vol.vid)
            return VolList
        osdExtAttr=ExtVolAttr_OSD()
        VolList = self._osdvolDAO.getVolume(name_or_id, serv=serv, _cfg=self._CFG, _user=_user)
        self.Logger.debug("OSDgetVolume: VolList=%s" % VolList)
        for vol in VolList :
            vol.serv_uuid=afs.LookupUtil[self._CFG.CELL_NAME].getFSUUID(vol.servername,self._CFG,cached=False)
            StorageUsage=self.getStorageUsage([serv,],vol.vid)
            if hasattr(vol,"filequota") :
                osdExtAttr.filequota=vol.filequota
                del(vol.filequota)
            if hasattr(vol,"osdPolicy") :
                osdExtAttr.osdPolicy=vol.osdPolicy
                del(vol.osdPolicy)
            osdExtAttr.blocks_osd_on=StorageUsage["storageUsage"]["online"]["Data"]
            osdExtAttr.blocks_osd_off=StorageUsage["storageUsage"]["archival"]["Data"]
            osdExtAttr.blocks_fs=StorageUsage["storageUsage"]["fileserver"]["Data"]
            osdExtAttr.vid=vol.vid
            self.Logger.debug("getVolume: osdExtAttr=%s" % osdExtAttr)
            if osdExtAttr.osdPolicy != 0 : 
                vol.OsdAttr=osdExtAttr

            if self._CFG.DB_CACHE :
                self.DBManager.setIntoCache(Volume,vol,vid=vol.vid,serv_uuid=vol.serv_uuid,part=vol.part) 
                if osdExtAttr.osdPolicy != 0 : 
                    self.DBManager.setIntoCache(ExtVolAttr_OSD,osdExtAttr,vid=osdExtAttr.vid) 
        return VolList

    def saveExtVolAttr_OSD(self,Obj):
        cachedObj=self.DBManager.setIntoCache(ExtVolAttr_OSD,Obj,vid=Obj.vid)
        return cachedObj

    def getExtVolAttr_OSD(self,vid) :
        cachedObj=self.DBManager.getFromCache(ExtVolAttr_OSD,vid=vid)
        return cachedObj

    def getStorageUsage(self,servers,vid,oldStorageUsage=None,_user="") :
        """
        do a vos traverse on a single Volume and merge with another histogram, if given
        return result as a dict
        if cached = True, then save ExtVolAttr_OSD in DBCache
        """
        try:
            StorageUsage=self._osdvolDAO.traverse(servers, vid, _cfg=self._CFG, _user=_user)
        except:
            return emptyStorageUsageDict

        if oldStorageUsage == None : return StorageUsage
        if len(oldStorageUsage) == 0 : return StorageUsage

        # merge with given histogram
        # totals
        for k in StorageUsage["totals"].keys() :
            StorageUsage["totals"][k]["numFiles"] += oldStorageUsage["totals"][k]["numFiles"] 
            StorageUsage["totals"][k]["Data"] += oldStorageUsage["totals"][k]["Data"] 
        # logical
        for oldbin in oldStorageUsage["logical"] :
            found=False
            for b in range(len(StorageUsage["logical"])) :
                if oldbin["lowerSize"] == StorageUsage["logical"][b]["lowerSize"] :
                    found = True
                    StorageUsage["logical"][b]["numFiles"] += oldbin["numFiles"] 
                    StorageUsage["logical"][b]["binData"] += oldbin["binData"] 
                    break
            if not found :
                StorageUsage["logical"].append(oldbin)                
        # real storage
        for k in ["numFiles","Data"] :
            StorageUsage["storageUsage"]["fileserver"][k] += oldStorageUsage["storageUsage"]["fileserver"][k]
            StorageUsage["storageUsage"]["archival"][k] += oldStorageUsage["storageUsage"]["archival"][k]
            StorageUsage["storageUsage"]["online"][k] += oldStorageUsage["storageUsage"]["online"][k]
        # detailed 
        for k in oldStorageUsage["storageUsage"]["detailed"] :
            found = False
            for b in range(len(StorageUsage["storageUsage"]["detailed"])) :
                if StorageUsage["storageUsage"]["detailed"][b]["osdid"] == k["osdid"] :
                    found = True
                    StorageUsage["storageUsage"]["detailed"][b]["Data"] += k["Data"]
                    StorageUsage["storageUsage"]["detailed"][b]["numFiles"] += k["numFiles"]
            if not found :
                StorageUsage["storageUsage"]["detailed"].append(k)
        # withoutCopy
        for k in ["numFiles","Data"] :
            StorageUsage["withoutCopy"]["fileserver"][k] += oldStorageUsage["withoutCopy"]["fileserver"][k]
            StorageUsage["withoutCopy"]["archival"][k] += oldStorageUsage["withoutCopy"]["archival"][k]
            StorageUsage["withoutCopy"]["online"][k] += oldStorageUsage["withoutCopy"]["online"][k]
        for k in oldStorageUsage["storageUsage"]["detailed"] :
            found = False
            for b in range(len(StorageUsage["withoutCopy"]["detailed"])) :
                if StorageUsage["withoutCopy"]["detailed"][b]["osdid"] == k["osdid"] :
                    found = True
                    StorageUsage["withoutCopy"]["detailed"][b]["Data"] += k["Data"]
                    StorageUsage["withoutCopy"]["detailed"][b]["numFiles"] += k["numFiles"]
            if not found :
                StorageUsage["withoutCopy"]["detailed"].append(k)

        if self._CFG.DB_CACHE :
            OsdVolAttr={}
            OsdVolAttr['vid'] = vid
            OsdVolAttr['blocks_fs']=int(StorageUsage["storageUsage"]["fileserver"]["Data"])
            OsdVolAttr['blocks_osd_on']=int(StorageUsage["storageUsage"]["online"]["Data"])
            OsdVolAttr['blocks_osd_off']=int(StorageUsage["storageUsage"]["archival"]["Data"])
            thisObj=ExtVolAttr_OSD()
            thisObj.setByDict(OsdVolAttr)
            self.DBManager.setIntoCache(ExtVolAttr_OSD,thisObj,vid=thisObj.vid)
        return StorageUsage
