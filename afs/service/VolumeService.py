import string,json,logging
from afs.model.Volume import Volume
from afs.model.ExtendedVolumeAttributes import ExtVolAttr
from afs.service.BaseService import BaseService, task_wrapper
from afs.service.VolumeServiceError import VolumeServiceError
from afs.util import misc
import afs


class VolumeService (BaseService):
    """
    Provides Service about a Volume management.
    The cellname is set in the methods so that we 
    can use this for more than one cell.
    """
    
    def __init__(self, conf=None):
        BaseService.__init__(self, conf, LLAList=["fs", "vol"])
       
    def get_object(self, obj_or_param) :
        """
        return an object, regardless of what was the input (object or unique parameters)
        unique paramter is name_or_id (either volume name or volume id)
        """
        if isinstance(obj_or_param, Volume) :
             this_Volume = obj_or_param
        else : 
             this_Volume = Volume()
             if misc.is_name(obj_or_param) :
                 this_Volume.name = obj_or_param
             else :
                 this_Volume.vid = obj_or_param
        return this_Volume

    @task_wrapper
    def get_volume_group(self, obj_or_param, _thread_name="", _user="", cached=True, async=False):
        """
        Retrieve Volume Group.
        Returns dict "RW": RWVolObj, "RO": [ROVolObj1, ROVolObj2, ...]
        """
        self.Logger.debug("get_volume_group: entering with obj_or_param=%s" % obj_or_param) 
        this_Volume = self.get_object(obj_or_param)

        volume_group = {"RW" : None, "RO" : [], "BK": None}
        if cached :
            if this_Volume.name != "" :
               volume_list = self.DBManager.get_from_cache(Volume, name=this_Volume.name, mustBeUnique=False)
            else :
               volume_list = self.DBManager.get_from_cache(Volume, vid=this_Volume.vid, mustBeUnique=False)
            self.Logger.debug("volume_list=%s" % volume_list)
            if volume_list != [] and volume_list != None :
                parent_id = volume_list[0].parent_id
                volume_list = self.DBManager.get_from_cache(Volume, parent_id=parent_id, mustBeUnique=False)
                for v in volume_list :
                    if v.type == "RW" :
                        volume_group["RW"] = v  
                    elif v.type == "RO" : 
                        volume_group["RO"].append(v)  
                    elif v.type == "BK" :
                        volume_group["BK"] = v  
                    else :
                        raise VolumeServiceError("get_volume_group: invalid volume type encountered: %s" % v.type)
                return self.do_return(_thread_name, volume_group)
            self.Logger.info("found no VolumeGroup for obj_or_param %s in cache. Trying live-system." % obj_or_param) 
        vol = self._volLLA.examine(this_Volume, _cfg=self._CFG, _user=_user)
        if vol == None : 
            self.Logger.debug("get_volume_group: returning live: None")
            return self.do_return(_thread_name, None)
        vol = vol[0]
        self.Logger.debug("get_volume_group: got vol=%s" % vol)
       
        # depending on what we got fill in the others
        rw_vol = self.get_object(vol.parent_id)
        ro_vol = self.get_object(vol.readonly_id)
        bk_vol = self.get_object(vol.backup_id)
        if vol.parent_id != 0 :
            volume_group["RW"] = self._volLLA.examine(rw_vol, _cfg=self._CFG, _user=_user)[0]
            volume_group["RW"].fileserver_uuid = afs.LOOKUP_UTIL[self._CFG.cell].get_fsuuid(volume_group["RW"].servername, self._CFG)
        if vol.readonly_id != 0 :
            volume_group["RO"] = self._volLLA.examine(ro_vol, _cfg=self._CFG, _user=_user)
            for volume in volume_group["RO"] :
                volume.fileserver_uuid = afs.LOOKUP_UTIL[self._CFG.cell].get_fsuuid(volume.servername, self._CFG)
        if vol.backup_id != 0 :
            volume_group["BK"].fileserver_uuid = afs.LOOKUP_UTIL[self._CFG.cell].get_fsuuid(volume_group["BK"].servername, self._CFG)
            volume_group["BK"] = self._volLLA.examine(bk_vol, _cfg=self._CFG, _user=_user)[0]  
        
        if self._CFG.DB_CACHE :
            if volume_group["RW"] != None :
                self.DBManager.set_into_cache(Volume, volume_group["RW"], vid=volume_group["RW"].vid, fileserver_uuid=volume_group["RW"].fileserver_uuid)
            for volume in volume_group["RO"] :
                self.DBManager.set_into_cache(Volume, volume, vid=volume.vid, fileserver_uuid=volume.fileserver_uuid)
                
            if volume_group["BK"] != None :
                self.DBManager.set_into_cache(Volume, volume_group["BK"], vid=volume_group["BK"].vid, fileserver_uuid=volume_group["BK"].fileserver_uuid)
       
        self.Logger.debug("get_volume_group: returning: %s " % (volume_group))
        return self.do_return(_thread_name, volume_group)

    @task_wrapper
    def get_volume(self, obj_or_param, fileserver="", _thread_name="", _user="", cached=True, async=False):
        """
        Retrieve Volume Information by Name or ID
        Always return a list
        """
        this_Volume = self.get_object(obj_or_param)

        if fileserver != "" :
            wanted_fileserver_uuid = afs.LOOKUP_UTIL[self._CFG.cell].get_fsuuid(fileserver, self._CFG)
        else : # make it an invalid UUID
            wanted_fileserver_uuid = "XXX"
      
        self.Logger.debug("get_volume: called with obj_or_param=%s, fileserver=%s->wanted_fileserver_uuid=%s, _user=%s" % (obj_or_param, fileserver, wanted_fileserver_uuid, _user))

        if cached :
            if fileserver != "" : 
                if this_Volume.name != "" :
                    volume_list = self.DBManager.get_from_cache(Volume, name=this_Volume.name, fileserver_uuid=wanted_fileserver_uuid, mustBeUnique=False)
                else :
                    volume_list = self.DBManager.get_from_cache(Volume, vid=this_Volume.vid, fileserver_uuid=wanted_fileserver_uuid, mustBeUnique=False)
            else :
                if this_Volume.name != "" :
                    volume_list = self.DBManager.get_from_cache(Volume, name=this_Volume.name, mustBeUnique=False)
                else :
                    volume_list = self.DBManager.get_from_cache(Volume, vid=this_Volume.vid, mustBeUnique=False)
                
            if volume_list != [] and volume_list != None :
                return self.do_return(_thread_name, volume_list)
        volume_list = self._volLLA.examine(this_Volume, _cfg=self._CFG, _user=_user)
        self.Logger.debug("get_volume: got volume_list from LLA : %s" % volume_list)
        if volume_list == None :
            return self.do_return(_thread_name, None)
        to_be_removed = []
        for volume in volume_list : 
            volume.fileserver_uuid = afs.LOOKUP_UTIL[self._CFG.cell].get_fsuuid(volume.servername, self._CFG)
            if volume.fileserver_uuid != wanted_fileserver_uuid  and wanted_fileserver_uuid != "XXX" :
                to_be_removed.append(volume)

        for volume in to_be_removed :
            volume_list.remove(volume)
            
        self.Logger.debug("get_volume: v=%s" % volume)
        
        # XXX Need a sync mechanism, in order to update Volume-entries, (since we only update if a volume has not been moved
        # to another server)
        if self._CFG.DB_CACHE :
            for volume in volume_list :
                self.DBManager.set_into_cache(Volume, volume, vid=volume.vid, fileserver_uuid=volume.fileserver_uuid)
        return self.do_return(_thread_name, volume_list)

    def get_extended_volume_attributes(self, vid) :
        cachedi_obj = self.DBManager.get_from_cache(ExtVolAttr, vid=vid)
        return cached_obj

    def save_extended_volume_attributes(self, Obj):
        cached_obj = self.DBManager.set_into_cache(ExtVolAttr, Obj, vid=Obj.vid)
        return cached_obj
