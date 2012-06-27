import string,json
from afs.model.Volume import Volume
from afs.model.ExtendedVolumeAttributes import ExtVolAttr
from afs.model.VolumeGroup import VolumeGroup
from afs.service.BaseService import BaseService
from afs.service.CellService import CellService
from afs.service.FsService import FsService
from afs.exceptions.VolError import VolError
from afs.exceptions.AfsError import AfsError
from afs.util import afsutil


class VolService (BaseService):
    """
    Provides Service about a Volume management.
    The cellname is set in the methods so that we 
    can use this for more than one cell.
    """
    
    def __init__(self, conf=None):
        BaseService.__init__(self, conf, DAOList=["vol","fs"])
        self.CS=CellService()
        self.FsS=FsService()
       
    ###############################################
    # Volume Section
    ###############################################    
    
    """
    Retrieve Volume Group
    """
    def getVolGroup(self, id , cached=False):
        self.Logger.debug("entering with id=%s" % id) 
        if cached :
            return self.DBCService.getFromCacheByListElement(VolumeGroup,VolumeGroup.RW,id)
        list = self._volDAO.getVolGroupList(id,  self._CFG.CELL_NAME, self._CFG.Token)
        volGroup = None
        if len(list) > 0:
            volGroup =  VolumeGroup()
            for el in list:
                volGroup.name = el['volname']
                if el['type'] == 'RW':
                    volGroup.RW=el
                elif el['type'] == 'RO':
                    volGroup.RO.append(el)
                else :
                    volGroup.BK=el
        self.Logger.debug("returning : %s" % volGroup)
        if self._CFG.DB_CACHE :
            self.DBCService.setIntoCache(VolumeGroup,volGroup,name = volGroup.name)
        return volGroup
       
    """
    Retrieve Volume Information by Name or ID
    """
    def getVolume(self, name_or_id, serv, part,  cached=False):
        if cached :
            serv_uuid=self.FsS.getUUID(serv, cached=cached)
            # need function in util name_or_ip and name_or_id?
            if afsutil.isName(name_or_id) :
                vol=self.DBCService.getFromCache(Volume,name=name_or_id,serv_uuid=serv_uuid)
            else :
                vol=self.DBCService.getFromCache(Volume,vid=name_or_id,serv_uuid=serv_uuid)
            return vol
        vdict = self._volDAO.getVolume(name_or_id, serv, part,  self._CFG.CELL_NAME, self._CFG.Token)
        vdict["serv_uuid"]=self.FsS.getUUID(serv)
        vdict.pop("serv")
        vol = None
        if vdict:
            vol = Volume()
            vol.setByDict(vdict)
            if self._CFG.DB_CACHE :
                self.DBCService.setIntoCache(Volume,vol,vid = vol.vid)
        return  vol

    def saveExtVolAttr(self, Obj):
        cachedObj=self.DBCService.setIntoCache(ExtVolAttr,Obj,vid=Obj.vid)
        return cachedObj

    def saveExtVolAttrbyDict(self,vid,dict) :
        cachedObj=ExtVolAttr()
        cachedObj.setByDict(dict)
        cachedObj=self.saveExtVolAttr(cachedObj)
        return cachedObj

    ################################################
    # AFS-operations
    ################################################
 
    def release(self, id) :
        #Check before the call (must be RW)
        pass
