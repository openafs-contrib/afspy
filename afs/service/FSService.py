"""
Provides Service about a FileServer
"""

import datetime

from afs.service.BaseService import BaseService, task_wrapper
from afs.service.FSServiceError import FSServiceError
from afs.model.ExtendedPartitionAttributes import ExtPartAttr
from afs.model.ExtendedFileServerAttributes import ExtFileServAttr
from afs.model.FileServer import FileServer
from afs.model.Partition import Partition
from afs.model.Volume import Volume
from afs.magix import VolStatus, VolType
import afs


class FSService (BaseService):
    """
    Provides Service about a FileServer
    """
    
    def __init__(self, conf=None):
        BaseService.__init__(self, conf, LLAList=["fs", "rx", "vl"])

    ###############################################
    # Volume Section
    ###############################################    
    
    def get_object(self, obj_or_param, cached) :
        """
        return a FileServer object
        """
        if isinstance(obj_or_param, FileServer) :
            this_fileserver = obj_or_param
        else :
            this_fileserver = self.get_fileserver(obj_or_param, cached=cached)
        return this_fileserver

    
    @task_wrapper
    def get_details(self, obj_or_param, **kw ):
        """
        add partition-objs and the extraneous attributes to the partitions
        """
        cached = kw.get("cached", True)
        _user = kw.get("_user", "")

        this_fileserver = self.get_object(obj_or_param, cached)

        stale_date = ( datetime.datetime.now() -  datetime.timedelta(seconds=int(self._CFG.STALE_DAYS)))

        self.Logger.debug("get_details: called with obj=%s, kw=%s"\
            % (obj_or_param,kw))

        vols = []
        if cached :
            vols = self.DBManager.get_from_cache(Volume, must_be_unique=False, fileserver_uuid=this_fileserver.uuid) 
            this_fileserver.volumes = vols
            return this_fileserver
                
        vols = []
        for part in this_fileserver.parts :    
            this_vols = self._fsLLA.get_volume_list(this_fileserver, part=part.name, \
                _cfg=self._CFG, _user=_user)
            vols += this_vols
        
            part.ExtAttr = ExtPartAttr()
            part.ExtAttr.num_vol_rw = 0
            part.ExtAttr.num_vol_ro = 0
            part.ExtAttr.num_vol_bk = 0
            part.ExtAttr.num_vol_offline = 0
            part.ExtAttr.allocated = 0
            part.ExtAttr.allocated_stale = 0
            part.ExtAttr.name = part.name
            part.ExtAttr.fileserver_uuid = this_fileserver.uuid
            for v in this_vols :
                if v.status  == "UNATTACHABLE" :
                    part.ExtAttr.num_vol_offline += 1
                    continue
                if v.status  == "BUSY" :
                    self.Logger.warn("get_details: skipping %s on fileserver=%s. It's busy." % (v.vid, this_fileserver.servernames[0]))
                    continue
                if v.type == "RW" :
                    part.ExtAttr.num_vol_rw += 1
                elif v.type == "RO" :
                    part.ExtAttr.num_vol_ro += 1
                elif v.type == "BK" :
                    part.ExtAttr.num_vol_bk += 1
                else :
                    raise RuntimeError("wrong volume type '%s' for vid=%s on fileserver=%s found." % (v.type, v.vid, this_fileserver.servernames[0]))
                if v.update_date < stale_date :
                     part.ExtAttr.allocated_stale += v.maxquota
                else :
                     part.ExtAttr.allocated += v.maxquota
                v.fileserver_uuid = this_fileserver.uuid
                v.partition = part.name
                # update cache
                if self._CFG.DB_CACHE :
                    self.DBManager.set_into_cache(Volume, v, must_be_unique=True, vid = v.vid, fileserver_uuid = this_fileserver.uuid, partition = part.name)

            if self._CFG.DB_CACHE :
                self.DBManager.set_into_cache(Partition, part, must_be_unique=True,  \
                    fileserver_uuid=this_fileserver.uuid, name=part.name)    
                self.DBManager.set_into_cache(ExtPartAttr, part.ExtAttr, must_be_unique=True, \
                    fileserver_uuid=this_fileserver.uuid, name=part.name)    
        # update cache
        if self._CFG.DB_CACHE :
            self.DBManager.set_into_cache(FileServer, this_fileserver, must_be_unique=True, uuid = this_fileserver.uuid)

        this_fileserver.volumes = vols

        if kw.get("async", True) :
            self.task_results[kw["_thread_name"]] = this_fileserver
        else : 
            return this_fileserver
    
    ###############################################
    # File Server Section
    ###############################################
    
    @task_wrapper
    def get_fileserver(self, name_or_ip, **kw):
        """
        Retrieve Fileserver Object by hostname or IP or uuid
        and update DBCache, if enabled 
        """
        self.Logger.debug("get_fileserver: called with name_or_ip=%s, kw=%s"\
            % (name_or_ip, kw))
        uuid = kw.get("uuid", "")
        cached = kw.get("cached", True)
        _user = kw.get("_user", "")

        dns_info = afs.LOOKUP_UTIL[self._CFG.cell].get_dns_info(name_or_ip)
        if dns_info["ipaddrs"][0] in self._CFG.ignoreIPList :
            return None
        if uuid != "" :
            if uuid != afs.LOOKUP_UTIL[self._CFG.cell].get_fsuuid(name_or_ip, \
                self._CFG, cached) :
                uuid = afs.LOOKUP_UTIL[self._CFG.cell].get_fsuuid(name_or_ip, \
                    self._CFG, cached)
        else :
            uuid = afs.LOOKUP_UTIL[self._CFG.cell].get_fsuuid(name_or_ip, \
                self._CFG, cached)
         
        self.Logger.debug("uuid=%s" % uuid)
        if cached :
            this_fileserver = self.DBManager.get_from_cache(FileServer, \
                 uuid=uuid)
            if this_fileserver == None : # not in the cache. 
                self.Logger.warn("get_fileserver: FS with name_or_ip=%s, uuid=%s not in DB or outdated."\
                    % (name_or_ip, uuid))
            else :
                this_fileserver.ExtAttr = self.DBManager.get_from_cache(ExtFileServAttr, \
			must_be_unique=True, fileserver_uuid=uuid)
                if this_fileserver.ExtAttr == None :
                    this_fileserver.ExtAttr = ExtFileServAttr()
                this_fileserver.parts = []
                try :
                    for part in self.DBManager.get_from_cache(Partition, \
                        must_be_unique=False, fileserver_uuid=uuid) :
                        part.ExtAttr = self.DBManager.get_from_cache(ExtPartAttr, \
                            must_be_unique=True, fileserver_uuid=uuid, name=part.name)
                        if part.ExtAttr == None :
                            part.ExtAttr = ExtPartAttr()
                        # XXX if there's no entry, fix default value of projectIDS
                        this_fileserver.parts.append(part)
                    return this_fileserver
                except TypeError : # no info from DB, let's pass onto live-system
                    self.Logger.warn("get_fileserver: Partition info about FS with uuid=%s not in DB. Maybe it has no partitions ?"\
                         % uuid)
                    return this_fileserver

        this_fileserver = FileServer()
        this_fileserver.servernames = dns_info["names"]
        this_fileserver.ipaddrs = dns_info["ipaddrs"]
        # UUID
        this_fileserver.uuid = uuid
        try :
            this_fileserver.version, this_fileserver.build_date = \
                self._rxLLA.getVersionandBuildDate(this_fileserver.servernames[0], \
                7000, _cfg=self._CFG, _user=_user)
        except :
            self.Logger.error("get_fileserver: cannot get information from fileserver %s. Is it up? Returning dummy-info" % this_fileserver.servernames[0])
            this_fileserver.version = -1
            this_fileserver.build_date = -1
            this_fileserver.parts = []
            return this_fileserver

        # update cache
        if self._CFG.DB_CACHE :
            self.DBManager.set_into_cache(FileServer, this_fileserver, \
                 uuid=this_fileserver.uuid)
            
        # Partitions
        this_fileserver.parts = []
        for part in self._fsLLA.get_partitions(this_fileserver, \
            _cfg=self._CFG, _user=_user) :
            part.fileserver_uuid = uuid
            part.ExtAttr = ExtPartAttr()
            part.ExtAttr.name = part.name
            part.ExtAttr.fileserver_uuid = uuid
            this_fileserver.parts.append(part)
            # update cache
            if self._CFG.DB_CACHE :
                self.DBManager.set_into_cache(Partition, part, fileserver_uuid=\
                    uuid, name=part.name)
                self.DBManager.set_into_cache(ExtPartAttr, part.ExtAttr, fileserver_uuid=\
                    uuid, name=part.name)
        self.Logger.debug("get_fileserver: returning: %s" % this_fileserver)
        if kw.get("async", True) :
            self.task_results[kw["_thread_name"]] = this_fileserver
        else : 
            return this_fileserver
