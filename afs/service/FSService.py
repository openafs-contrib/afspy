"""
Provides Service about a FileServer
"""
from afs.service.BaseService import BaseService
from afs.service.FSServiceError import FSServiceError
from afs.model.ExtendedPartitionAttributes import ExtPartAttr
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
        BaseService.__init__(self, conf, DAOList=["fs", "vl", "rx", "vol"])

    ###############################################
    # Volume Section
    ###############################################    
    
    def get_object(self, obj_or_param) :
        """
        return a FileServer object
        """
        if isinstance(obj_or_param, FileServer) :
            this_fileserver = obj_or_param
        else :
            dns_info = afs.LOOKUP_UTIL[self._CFG.cell].get_dns_info(obj_or_param)
            this_fileserver = FileServer()
            this_fileserver.servernames = dns_info["names"]
            this_fileserver.uuid = afs.LOOKUP_UTIL[self._CFG.cell].get_fsuuid(\
                dns_info["names"][0], self._CFG, cached)
        return this_fileserver

    


    def get_volumes(self, obj_or_param, **kw ):
        """
        Return list of volumes
        """
        cached = kw.get("cached", True)
        _user = kw.get("_user", "")
        part = kw.get("part", "")

        this_fileserver = self.get_object(obj_or_param)

        self.Logger.debug("get_volume_list: called with obj=%s, kw=%s"\
            % (obj_or_param,kw))

        this_fileserver = self.get_object(obj_or_param)

        vols = []
            
        if part :    
            vols = self._fsDAO.get_volume_list(this_fileserver, part=part, \
                _cfg=self._CFG, _user=_user)
        else:
            for part in this_fileserver.parts:
                vols += self._fsDAO.get_volume_list(this_fileserver, part=part.name, \
                    _cfg=self._CFG, _user=_user)
        return vols
    
    ###############################################
    # File Server Section
    ###############################################
    
    def get_fileserver(self, name_or_ip, **kw):
        """
        Retrieve Fileserver Object by hostname or IP or uuid
        and update DBCache, if enabled 
        """
        self.Logger.debug("get_fileserver: called with name_or_ip=%s, kw=%s"\
            % (name_or_ip,kw))
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
                self.Logger.warn("getFileServer: FS with uuid=%s not in DB."\
                    % uuid)
            else :
                this_fileserver.parts = []
                for part in self.DBManager.get_from_cache(Partition, \
                    mustBeUnique=False, fileserver_uuid=uuid) :
                    part.ExtAttr = self.DBManager.get_from_cache(ExtPartAttr, \
                        mustBeUnique=True, fileserver_uuid=uuid, name=part.name)
                    # XXX if there's no entry, fix default value of projectIDS
                    if part.ExtAttr == None :
                        part.ExtAttr = ExtPartAttr()
                    this_fileserver.parts.append(part)
                return this_fileserver

        this_fileserver = FileServer()
        this_fileserver.servernames = dns_info["names"]
        this_fileserver.ipaddrs = dns_info["ipaddrs"]
        # UUID
        this_fileserver.uuid = uuid
        this_fileserver.version, this_fileserver.build_date = \
            self._rxDAO.getVersionandBuildDate(this_fileserver.servernames[0], \
            7000, _cfg=self._CFG, _user=_user)

        # Partitions
        this_fileserver.parts = []
        for part in self._fsDAO.get_partitions(this_fileserver, \
            _cfg=self._CFG, _user=_user) :
            part.fileserver_uuid = uuid
            part.ExtAttr = ExtPartAttr()
            this_fileserver.parts.append(part)
            if self._CFG.DB_CACHE :
                self.DBManager.set_into_cache(Partition, part, fileserver_uuid=\
                    uuid, name=part.name)
        # update cache
        if self._CFG.DB_CACHE :
            self.DBManager.set_into_cache(FileServer, this_fileserver, \
                 uuid=this_fileserver.uuid)
        # Projects are only available in the DB_CACHE
        
        this_fileserver.projects = []
        self.Logger.debug("get_file_server: returning: %s" % this_fileserver)
        return this_fileserver

        if cached :
            return partition_list

