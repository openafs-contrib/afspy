from afs.model.Volume import Volume
from afs.model.ExtendedVolumeAttributes_OSD import ExtVolAttr_OSD
from afs.model.VolumeGroup import VolumeGroup
from afs.service.BaseService import BaseService
from afs.service.VolService import VolService
from afs.service.CellService import CellService
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
        BaseService.__init__(self, conf, DAOList=["osdvol","fs"])


    """
    Retrieve Volume Information by Name or ID
    Overridden from VolService.
    """
    def getVolume(self, name_or_id, serv="", part="", _user="", cached=False):
        self.Logger.debug("Entering with name_or_id=%s, serv=%s, part=%s,cached=%s",name_or_id, serv, part,  cached) 
        if cached :
            if serv != "" :
                serv_uuid=afs.LookupUtil[self._CFG.CELL_NAME].getFSUUID(serv,self._CFG,cached=True)
                # need function in util name_or_ip and name_or_id?
                if afsutil.isName(name_or_id) :
                    vol=self.DBManager.getFromCache(Volume,name=name_or_id,serv_uuid=serv_uuid)
                else :
                    vol=self.DBManager.getFromCache(Volume,vid=name_or_id,serv_uuid=serv_uuid)
            else :
                if afsutil.isName(name_or_id) :
                    vol=self.DBManager.getFromCache(Volume,name=name_or_id)
                else :
                    vol=self.DBManager.getFromCache(Volume,vid=name_or_id)
            vol.ExtAttr=self.getExtVolAttr(vol.vid)
            vol.OsdAttr=self.DBManager.getFromCache(ExtVolAttr_OSD,vid=vol.vid)
            return vol
        osdExtAttr=ExtVolAttr_OSD()
        odict=osdExtAttr.getDict()
        vdict = self._osdvolDAO.getVolume(name_or_id, serv, part, _cfg=self._CFG, _user=_user)
        self.Logger.debug("getVolume: vdict=%s" % vdict)
        if not vdict :
            return None
        StorageUsage=self.getStorageUsage([serv,],vdict["vid"])
        vdict["blocks_osd_on"]=StorageUsage["storageUsage"]["online"]["Data"]
        vdict["blocks_osd_off"]=StorageUsage["storageUsage"]["archival"]["Data"]
        vdict["blocks_fs"]=StorageUsage["storageUsage"]["fileserver"]["Data"]
        vdict["serv_uuid"]=afs.LookupUtil[self._CFG.CELL_NAME].getFSUUID(serv,self._CFG,cached=False)
        vdict.pop("serv")
        self.Logger.debug("getVolume: vdict=%s" % vdict)
        # move stuff to OSD-dict
        for k in vdict.keys() :
            if k in odict.keys() : 
                odict[k] = vdict[k] 
                if k == "vid" : continue
                vdict.pop(k)
        vol = Volume()
        # XXX: we need this to ignore the OsdAttr and ExtAttr in the copy-operation.
        vdict["ignAttrList"]=vol.ignAttrList
        vol.setByDict(vdict)
        if odict['osdPolicy'] != 0 : 
            vol.OsdAttr=odict
            osdExtAttr.setByDict(odict)
        if self._CFG.DB_CACHE :
            self.DBManager.setIntoCache(Volume,vol,vid=vol.vid) 
            if odict['osdPolicy'] != 0 : 
                self.DBManager.setIntoCache(ExtVolAttr_OSD,osdExtAttr,vid=osdExtAttr.vid) 
        return vol

    def saveOsdVolAttr(self,Obj):
        cachedObj=self.DBManager.setIntoCache(ExtVolAttr_OSD,Obj,vid=Obj.vid)
        return cachedObj

    def getStorageUsage(self,servers,vid,oldStorageUsage=None,_user="",cached=False) :
        """
        do a vos traverse and merge with another histogram, if given
        return result as a dict
        if cached = True, then save in DBCache
        """
        try:
            StorageUsage=self._osdvolDAO.traverse(servers,vid, _cfg=self._CFG, _user=_user)
        except:
            return emptyStorageUsageDict

        # store OsdVolAttr in DB_CACHE 
        if cached :
            cachedObj=self.DBManager.getFromCache(ExtVolAttr_OSD,vid=vid)
            return cachedObj

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
