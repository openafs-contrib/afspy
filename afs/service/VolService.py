import string,json
from afs.model.Volume import Volume
from afs.model.ExtendedVolumeAttributes import ExtVolAttr
from afs.model.VolumeGroup import VolumeGroup
from afs.service.BaseService import BaseService
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
       
    ###############################################
    # Volume Section
    ###############################################    
    
    """
    Retrieve Volume Group
    """
    def getVolGroup(self, id, _user="", cached=False):
        self.Logger.debug("entering with id=%s" % id) 
        if cached :
            return self.DBManager.getFromCacheByListElement(VolumeGroup,VolumeGroup.RW_js,id)
        list = self._volDAO.getVolGroupList(id,  self._CFG.CELL_NAME, _cfg=self._CFG, _user=_user)
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
            self.DBManager.setIntoCache(VolumeGroup,volGroup,name = volGroup.name)
        return volGroup
       
    """
    Retrieve Volume Information by Name or ID
    """
    def getVolume(self, name_or_id, serv="", part="", _user="", cached=False):
        if cached :
            if serv != "" :
                serv_uuid=afsutil.getFSUUIDByName_IP_FromCache(serv,self._CFG)
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
            return vol
        vdict = self._volDAO.getVolume(name_or_id, serv, part,  self._CFG.CELL_NAME, _cfg=self._CFG, _user=_user)
        if vdict == None :
            return None
        vdict["serv_uuid"]=afsutil.getFSUUIDByName_IP(serv,self._CFG)
        vdict.pop("serv")
        self.Logger.debug("getVolume: vdict=%s" % vdict)
        vol = None
        if vdict:
            vol = Volume()
            vol.setByDict(vdict)
            if self._CFG.DB_CACHE :
                self.DBManager.setIntoCache(Volume,vol,vid = vol.vid)
        return vol

    def getExtVolAttr(self,vid) :
        cachedObj=self.DBManager.getFromCache(ExtVolAttr,vid=vid)
        return cachedObj

    def saveExtVolAttr(self, Obj):
        cachedObj=self.DBManager.setIntoCache(ExtVolAttr,Obj,vid=Obj.vid)
        return cachedObj

    ################################################
    # AFS-operations
    ################################################
 
    def release(self, id) :
        #Check before the call (must be RW)
        pass
