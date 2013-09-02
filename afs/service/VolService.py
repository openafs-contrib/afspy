import string,json,logging
from afs.model.Volume import Volume
from afs.model.ExtendedVolumeAttributes import ExtVolAttr
from afs.service.BaseService import BaseService
from afs.exceptions.VolError import VolError
from afs.exceptions.AfsError import AfsError
from afs.util import afsutil
import afs


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
    Retrieve Volume Group.
    Returns dict "RW": RWVolObj, "RO": [ROVolObj1, ROVolObj2, ...]
    """
    def getVolGroup(self, id, _user="", cached=True):
        self.Logger.debug("getVolGroup: entering with id=%s" % id) 
        VolGroupDict={"RW" : None, "RO" : [], "BK": None}
        if cached :
            VolList=self.DBManager.getFromCache(Volume,vid=id,mustBeUnique=False)
            self.Logger.debug("VolList=%s" % VolList)
            if VolList != [] :
                parentID=VolList[0].parentID
                VolList=self.DBManager.getFromCache(Volume,parentID=parentID,mustBeUnique=False)
                for v in VolList :
                    if v.type == "RW" :
                        VolGroupDict["RW"] = v  
                    elif v.type == "RO" : 
                        VolGroupDict["RO"].append(v)  
                    elif v.type == "BK" :
                        VolGroupDict["BK"] = v  
                    else :
                        raise AfsError("getVolGroup: invalid volume type encountered: %s" % v.type)
                return VolGroupDict 
            self.Logger.info("found no VolumeGroup for name_or_id %s in cache. Trying live-system." % id) 
        vol = self._volDAO.getVolume(id, _cfg=self._CFG, _user=_user)
        if vol == None : 
            self.Logger.debug("getVolGroup: returning live: None")
            return None
        self.Logger.debug("getVolGroup: got vol=%s" % vol)
        if vol[0]["vid"] == vol[0]["parentID"] : # is RW
            rwvol = vol
            try :
                rovol = self._volDAO.getVolume(vol[0]["cloneID"], _cfg=self._CFG, _user=_user)
            except : 
                rovol = []
            try :           
                bkvol = self._volDAO.getVolume(vol[0]["backupID"], _cfg=self._CFG, _user=_user)  
            except :
                bkvol = []
        elif vol[0]["vid"] == vol[0]["cloneID"] : # is RO
            rovol = vol
            try :
                rwvol = self._volDAO.getVolume(vol[0]["parentID"], _cfg=self._CFG, _user=_user)
            except :
                rwvol = []
            try :
                bkvol = self._volDAO.getVolume(vol[0]["backupID"], _cfg=self._CFG, _user=_user)  
            except :
                bkvol = []
        elif vol[0]["vid"] == vol[0]["backupID"] : # is RO
            bkvol = vol
            try :
                rwvol = self._volDAO.getVolume(vol[0]["parentID"], _cfg=self._CFG, _user=_user)
            except :
                rwvol = []
            try :           
                rovol = self._volDAO.getVolume(vol[0]["cloneID"], _cfg=self._CFG, _user=_user)  
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
    returns list of volume-objects.
    """
    def getVolume(self, name_or_id, serv=None, _user="", cached=True):
        VolList=[]
        if cached :
            if serv != "" :
                serv_uuid=afs.LookupUtil[self._CFG.cell].getFSUUID(serv,self._CFG)
                if afsutil.isName(name_or_id) :
                    vol=self.DBManager.getFromCache(Volume,name=name_or_id,serv_uuid=serv_uuid)
                else :
                    vol=self.DBManager.getFromCache(Volume,vid=name_or_id,serv_uuid=serv_uuid)
            else :
                if afsutil.isName(name_or_id) :
                    vol=self.DBManager.getFromCache(Volume,name=name_or_id)
                else :
                    vol=self.DBManager.getFromCache(Volume,vid=name_or_id)
            if vol != None :
                for v in vol :
                    v.ExtAttr=self.getExtVolAttr(v.vid)
                    VolList.append(v)
                return vol
        vdictList = self._volDAO.getVolume(name_or_id, serv=serv, _cfg=self._CFG, _user=_user)
        for vdict in vdictList :
            vdict["serv_uuid"]=afs.LookupUtil[self._CFG.cell].getFSUUID(vdict["serv"],self._CFG)
            vdict.pop("serv")
            self.Logger.debug("getVolume: vdict=%s" % vdict)
            vol = Volume()
            vol.setByDict(vdict)
            # this doesnot work, since RO are not unique.  
            # we would need to write a setListIntoCache method for this
            #if self._CFG.DB_CACHE :
            #    self.DBManager.setIntoCache(Volume,vol,vid = vol.vid)
            VolList.append(vol)
        return VolList

    def getExtVolAttr(self,vid) :
        cachedObj=self.DBManager.getFromCache(ExtVolAttr,vid=vid)
        return cachedObj

    def saveExtVolAttr(self, Obj):
        cachedObj=self.DBManager.setIntoCache(ExtVolAttr,Obj,vid=Obj.vid)
        return cachedObj
