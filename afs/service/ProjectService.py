import datetime
import json
import re
import types

from afs.model.Project import Project
from afs.model.ProjectSpread import ProjectSpread
from afs.service.BaseService import BaseService
from afs.service.ProjectServiceError import ProjectServiceError
from afs.service.FSService import FSService
from afs.service.VolumeService import VolumeService
from afs.model.ExtendedVolumeAttributes import ExtVolAttr
import afs

class ProjectService(BaseService):
    """
    Provides Service about Project management.
    This deals only with the DBCache.
    """
   
    def __init__(self, conf=None):
        BaseService.__init__(self, conf, LLAList=["fs"])
        if not self._CFG.DB_CACHE:
            raise ProjectServiceError('Error, Projects work only with a DBCache defined ', None)
        self.ModelObj = Project()
        self._VS = VolumeService()
        self._FS = FSService()
        return

    def get_object(self, obj_or_param) :
        """
        turn a input parameter which might be a project name into an object.
        do nothing if input is already an object
        """
        if isinstance(obj_or_param, Project) :
            this_project = obj_or_param
        else : 
            this_project = self.DBManager.get_from_cache(Project, fresh_only=False, name=obj_or_param)
            self.Logger.debug("get_object: name %s gave %s" % (obj_or_param, this_project))

        return this_project

#
# methods accessing project objects 
#
    
    def create_project(self, name, description, owner="", rw_locations=[], ro_locations=[]) :
        """
        create an empty project
        """
        this_project = Project()
        this_project.name = name
        this_project.description = description
        this_project.owner = owner
        this_project.rw_locations = rw_locations
        this_project.ro_locations = ro_locations
        # store_project adds db_id
        return self.store_project(this_project)

    def delete_project(self, name_or_obj) :
        """
        remove on project from the database. 
        take name as string or ProjectObject
        """
        this_project = self.get_object(name_or_obj)
        return self.DBManager.delete_from_cache(Project, name=this_project.name)

    def store_project(self, this_project):
        """
        store object into DBCache
        """
        self.Logger.debug("store_project: Obj=%s" % (this_project))
        this_project.update_db_repr()
        self.DBManager.set_into_cache(Project, this_project, name=this_project.name)
        # we need to return the object from the DB to set db_id. 
        return self.get_object(this_project.name)

    def get_project_by_name(self, name) :
        """
        return ProjectObj from Projectname
        """
        self.Logger.debug("get_project_by_name: called with name='%s'" % name)
        # Note: fresh_only must be false for all get_from_cache operations,
        # otherwise we get None
        this_project = self.DBManager.get_from_cache(Project, fresh_only=False, name="%s" % name)
        return this_project
   
    def get_project_list(self) :
        """
        return list of ProjectObjects
        """
        project_list = self.DBManager.get_from_cache(Project, fresh_only=False, must_be_unique=False) 
        if project_list == None :
            project_list = []
        return project_list

    def get_server_partitions(self, obj_or_param) :
        """
        return lists of (fs-name, part) tuples
        for RW and RO.
        So basically it is like rw_serverparts and ro_serverparts, but the 
        uuids replaced by hostnames.
        """
        this_project = self.get_object(obj_or_param)
        if not this_project : return None
        rw_list = [] 
        ro_list = []
        for fileserver_uuid, part in this_project.rw_serverparts :
            fs_name = afs.LOOKUP_UTIL[self._CFG.cell].get_hostname_by_fsuuid(fileserver_uuid)
            rw_list.append((fs_name,part),)
        for fileserver_uuid, part in this_project.ro_serverparts :
            fs_name = afs.LOOKUP_UTIL[self._CFG.cell].get_hostname_by_fsuuid(fileserver_uuid)
            ro_list.append((fs_name,part),)
        return rw_list, ro_list

    def add_server_partition(self, obj_or_param, server_partition, volume_type) :
        """
        assign a server_partition to a project
        """
        this_project = self.get_object(obj_or_param)
        fs_name, part = server_partition
        fileserver_uuid = afs.LOOKUP_UTIL[self._CFG.cell].get_fsuuid(fs_name)
        part = afs.util.misc.canonicalize_partition(part)
        if volume_type == "RW" :
            this_project.rw_serverparts.append((fileserver_uuid, part))
        elif volume_type == "RO" :
            this_project.ro_serverparts.append((fileserver_uuid, part))
        else :
            raise RuntimeError("assign_server_partition: Invalid volume_type '%s'" % volume_type)
        self.store_project(this_project)
        return this_project

    def remove_server_partition(self, obj_or_param, server_partition, volume_type) :
        """
        remove server_partition assignment from a project
        """
        this_project = self.get_object(obj_or_param)
        self.Logger.debug("called with: server_partition=%s, this_project=%s" % (server_partition, this_project) )
        fs_name, part = server_partition
        fileserver_uuid = afs.LOOKUP_UTIL[self._CFG.cell].get_fsuuid(fs_name)
        part = afs.util.misc.canonicalize_partition(part)
        if volume_type == "RW" :
            this_project.rw_serverparts.remove((fileserver_uuid, part))
        elif volume_type == "RO" :
            this_project.ro_serverparts.remove((fileserver_uuid, part))
        else :
            raise RuntimeError("resign_server_partition: Invalid volume_type '%s'" % volume_type)
        self.store_project(this_project)
        return this_project

    def add_location(self, obj_or_param, location, volume_type) :
        """
        add a location 
        """
        this_project = self.get_object(obj_or_param)
        if volume_type == "RW" :
            this_project.rw_locations.append(location)
        elif volume_type == "RO" :
            this_project.ro_locations.append(location)
        else :
            raise RuntimeError("add_location: Invalid volume_type '%s'" % volume_type)
        self.store_project(this_project)
        return this_project

    def remove_location(self, obj_or_param, location, volume_type) :
        """
        remove a location 
        """
        this_project = self.get_object(obj_or_param)
        if volume_type == "RW" :
            this_project.rw_locations.remove(location)
        elif volume_type == "RO" :
            this_project.ro_locations.remove(location)
        else :
            raise RuntimeError("remove_location: Invalid volume_type '%s'" % volume_type)
        self.store_project(this_project)
        return this_project

    def set_parent(self, obj_or_param, parent_obj_or_param) :
        """
        set the parent of a project
        """
        this_project = self.get_object(obj_or_param)
        parent_project = self.get_object(parent_obj_or_param)  
        this_project.parent_db_id = parent_project.db_id
        self.store_project(this_project)
        return this_project

    def remove_parent(self, obj_or_param) :
        """         
        remove the parent of a project
        """         
        this_project = self.get_object(obj_or_param)
        this_project.parent_db_id = -1
        self.store_project(this_project)
        return this_project 

    def get_parent(self, obj_or_param) :
        """
        return the parent project object
        """
        this_project = self.get_object(obj_or_param)
        parent_project = self.DBManager.get_from_cache(Project, fresh_only=False, must_be_unique=True, db_id = this_project.parent_db_id)
        return parent_project 

    def set_owner(self, obj_or_param, owner) :
        """
        set the owner attribute
        """
        this_project = self.get_object(obj_or_param)
        this_project.owner = owner
        self.store_project(this_project)
        return this_project

    def add_volume_regex(self, obj_or_param, regex) :
        """
        add a volume name regex for this project.
        """
        this_project = self.get_object(obj_or_param)
        if not regex in this_project.volname_regex :
            this_project.volname_regex.append(regex)
        self.store_project(this_project)
        return this_project

    def remove_volume_regex(self, obj_or_param, regex) :
        """
        add a volume name regex for this project.
        """
        this_project = self.get_object(obj_or_param)
        this_project.volname_regex.remove(regex)
        self.store_project(this_project)
        return this_project
   
    def add_additional_volume(self, obj_or_param, volname) : 
        """
        add an extra volume not covered by the regex to be part of this project
        """
        this_project = self.get_object(obj_or_param)
        if not volname in this_project.additional_volnames :
            this_project.additional_volnames.append(volname)
        self.store_project(this_project)
        return this_project

    def remove_additional_volume(self, obj_or_param, volname) :
        """
        remove an extra volume not covered by the regex to be part of this project
        """
        this_project = self.get_object(obj_or_param)
        this_project.additional_volnames.remove(volname)
        self.store_project(this_project)
        return this_project

    def add_excluded_volume(self, obj_or_param, volname) :
        """
        add a volume name to be excluded efrom this project ven if it matches a regex.
        """
        this_project = self.get_object(obj_or_param)
        if not volname in this_project.excluded_volnames :
            this_project.excluded_volnames.append(volname)
        self.store_project(this_project)
        return this_project
 
    def remove_excluded_volume(self, obj_or_param, volname) :
        """
        remove a volume name to be excluded efrom this project ven if it matches a regex.
        """
        this_project = self.get_object(obj_or_param)
        this_project.excluded_volnames.remove(volname)
        self.store_project(this_project)
        return this_project


#
# methods scanning cell 
#
    
    def get_projects_by_volume_name(self, volname):
        """
        return List of lists of Projects Objs from VolumeName.
        These lists are sorted by parent hierarchy of the projects
        """
        unsorted_list = []
        for p in self.DBManager.get_from_cache(Project, fresh_only=False, must_be_unique=False) :
            for rx in p.volname_regex :
                if re.compile(rx).match(volname) :
                    unsorted_list.append(p)

        hierarchies = []
        for p in unsorted_list :
            if p.parent_db_id == -1 :
                 hierarchies.append([p,])
        
        self.Logger.debug("hierarchies=%s" % hierarchies )
        self.Logger.debug("unsorted_list=%s" % [ (x.db_id, x.parent_db_id) for x in unsorted_list] )
        
        loop_again = True
        while loop_again :
            loop_again = False
            for p in unsorted_list :
                self.Logger.debug("project=%s,%s" % (p.db_id, p.parent_db_id))
                for hier in hierarchies :
                    self.Logger.debug("hierarchy=%s" % hier[-1:][0].db_id)
                    if p.parent_db_id == hier[-1:][0].db_id and p.db_id not in [ x.db_id for x in hier ] :
                        hier.append(p) 
                        self.Logger.debug("adding p %s to hierarchy %s" % ( (p.parent_db_id, p.db_id), [ x.db_id for x in hier ] ))
                        loop_again = True

        self.Logger.debug("hierarchies=%s" % [ (x[0].db_id, x[0].parent_db_id) for x in hierarchies] )
        return hierarchies

    def get_projects_on_server(self, name_or_obj) :
        """
        return dict[Partition] of lists of [(ProjectName, VolType)] for a fileserver
        """
        ProjectList = self.get_project_list()
        if isinstance(name_or_obj, basestring) :
            fs_name = name_or_obj
        else :
            try :
                fs_name = name_or_obj.hostnames[0]
            except :
                raise ProjectServiceError("Name of server (string) or Fileserver-Instance required.")
        FSUUID = afs.LOOKUP_UTIL[self._CFG.cell].get_fsuuid(fs_name)
        res_dict={}
        this_fs = self._FS.get_fileserver(fs_name)
        self.Logger.debug("this_fs=%s" % this_fs.servernames)
        self.Logger.debug("parts=%s" % this_fs.parts)
        for part in this_fs.parts :
            p = part.name
            res_dict[p]=[]
            all_prjs = self.DBManager.get_from_cache(ProjectSpread, fresh_only=False, must_be_unique=False, fileserver_uuid=FSUUID, part=p)
            self.Logger.debug("Results from DB: %s" % all_prjs )
            if all_prjs :
                for prj_spr in all_prjs :
                    prj = self.DBManager.get_from_cache(Project, fresh_only=False, must_be_unique=True, db_id=prj_spr.project_id)
                    res_dict[p].append((prj.name, prj_spr.vol_type))
        return res_dict
 
    def get_server_spread(self, obj_or_param):
        """
        return dict of lists of ProjectSpread Objects :
        [VolType]=[ProjectSpread]
        """
        self.Logger.debug("get_server_spread: called with %s" % obj_or_param)
        this_project = self.get_object(obj_or_param)
        if not this_project : return None
        res_dict = {"RW" : [], "RO" : [], "BK" : []}

        for vol_type in res_dict :
            res_dict[vol_type] = self.DBManager.get_from_cache(ProjectSpread, fresh_only=False, must_be_unique=False, vol_type=vol_type, project_id = this_project.db_id)
        return res_dict

    def gc_server_spread(self) :
        registered_prj_ids = [ p.db_id for p in self.get_project_list() ] 
        all_project_spreads = self.DBManager.get_from_cache(ProjectSpread, fresh_only=False, must_be_unique=False)
        if not all_project_spreads :
            return
        to_be_removed = []
        for prj_sprd  in all_project_spreads :
            if not prj_sprd.project_id in registered_prj_ids :
                to_be_removed.append(prj_sprd)

        for prj_sprd in to_be_removed :
            self.DBManager.delete_from_cache(ProjectSpread, db_id = prj_sprd.db_id)
        return
               
       
    def update_server_spread(self, obj_or_param):
        """
        update the server spread from the live cell into the DB.
        """
        this_project = self.get_object(obj_or_param)
        self.Logger.debug("update_server_spread called for prj %s" % this_project.name)
        res_dict = {"RW" : [], "RO" : [], "BK" : []}
        VolIDList = self.get_volume_IDs(this_project.name)
        if VolIDList == None : return None
        for v in VolIDList :
            VolGroup = self._VS.get_volume_group(v) 
            for vol_type in res_dict :
                if VolGroup[vol_type] == None : continue
                if not isinstance(VolGroup[vol_type],types.ListType) : 
                    VolGroup[vol_type] = [VolGroup[vol_type],]
                for vol in VolGroup[vol_type] :
                    FSUUID = vol.fileserver_uuid
                    Part = vol.partition

                    thisPrjSPObj = None
                    ResDictIndex = -1
                    for i in range(len(res_dict[vol_type])) :
                        prjspObj = res_dict[vol_type][i]
                        self.Logger.debug("comparing %s,%s,%s with %s,%s,%s" % ( prjspObj.fileserver_uuid, prjspObj.part, prjspObj.vol_type, FSUUID, Part, vol_type) )
                        if prjspObj.fileserver_uuid == FSUUID and prjspObj.part == Part and prjspObj.vol_type == vol_type :
                            thisPrjSPObj=prjspObj
                            ResDictIndex=i
                            break

                    if thisPrjSPObj == None :
                        thisPrjSPObj = ProjectSpread()
                        thisPrjSPObj.project_id = this_project.db_id
                        thisPrjSPObj.part = Part
                        thisPrjSPObj.fileserver_uuid = FSUUID    
                        thisPrjSPObj.vol_type = vol_type
                        thisPrjSPObj.num_vol = 0 
                    
                    thisPrjSPObj.num_vol += 1 
                    if ResDictIndex == -1 :
                        res_dict[vol_type].append(thisPrjSPObj)
                    else :
                        res_dict[vol_type][ResDictIndex] = thisPrjSPObj

        for vol_type in res_dict :
            for thisPrjSPObj in res_dict[vol_type] :
                self.DBManager.set_into_cache(ProjectSpread, thisPrjSPObj, vol_type=vol_type, project_id=thisPrjSPObj.project_id, fileserver_uuid=thisPrjSPObj.fileserver_uuid, part=thisPrjSPObj.part)
        
        self.Logger.debug("update_server_spread: returning %s" % res_dict)
        return res_dict

    def get_volume_IDs(self, prjname, servers=None) :
        """
        return list of Volume IDs part of this project.
        servers is an optional list of server_uuids to be used. 
        """
        self.Logger.debug("Entering with prjname=%s and servers=%s" % (prjname,servers))
        this_project = self.get_project_by_name(prjname)
        if not this_project : 
            self.Logger.debug("Invalid project-name %s given.", prjname)
            return None
         
        list = self.DBManager.get_from_cache(ExtVolAttr,fresh_only=False, must_be_unique=False)
        self.Logger.debug("Results from DB: %s" % list)
        list = self.DBManager.get_from_cache_by_list_element(ExtVolAttr, ExtVolAttr.project_ids_js, this_project.db_id, fresh_only=False, must_be_unique=False)
        if list == None :
            self.Logger.debug("Results from DB: %s" % list )
            return []
        elif len(list) > 0 :
            self.Logger.debug("Results[:10] from DB: %s" % list[:min(10,len(list))] )
        else :
            self.Logger.debug("Results from DB: %s" % list)
        VolIDList=[]
        for l in list :
            if servers == None :
                VolIDList.append(l.vid) 
            else  :
                for v in self._VS.get_volume(l.vid, cached=True) :
                    self.Logger.debug("Comparing '%s' to '%s'" % (v.fileserver_uuid,servers))
                    if v.fileserver_uuid in servers :
                        VolIDList.append(l.vid)
        self.Logger.debug("Returning VolIDList=%s" % VolIDList)
        return VolIDList

    def get_storage_usage(self, prjname) :
        """
        return dict of storage usage for given project.
        """
        this_project=self.get_project_by_name(prjname)
        if not this_project : return None
        res_dict={}
        conn = self._CFG.DB_ENGINE.connect()
        transa = conn.begin()
        RegEx="\\\[({0}|.*, {0}|{0},.*|.*, {0},.*)\\\]".format(this_project.db_id)
        # openafs volumes
        # this is not very efficient
        # for external RO we need the list of vids
        # all vids
        rawsql='SELECT E.vid FROM tbl_extvolattr AS E JOIN tbl_volume AS VOL on E.vid = VOL.vid WHERE E.project_ids_js REGEXP "%s";' % (RegEx)
        self.Logger.debug("Executing %s" % rawsql)
        res = conn.execute(rawsql).fetchall()
        self.Logger.debug("got res=%s" % res)
        VolIDs=[]
        for vid in res :
            VolIDs.append(vid[0])
        
        self.Logger.debug("VolIDs=%s" % (VolIDs))
        res_dict["diskused"]=0  
        res_dict["filecount"]=0  
       
        for vid in VolIDs :
            for field in ["diskused","filecount"] :
                rawsql='SELECT %s FROM tbl_volume  WHERE vid="%s";' % (field,vid)
                self.Logger.debug("Executing %s" % rawsql)
                res = conn.execute(rawsql).fetchall()
                self.Logger.debug("got res=%s" % res)
                try :
                    res_dict[field] += res[0][0]
                except :
                    res_dict[field] = 0
                if res_dict[field] == None : res_dict[field] = 0

            for field in ["diskused","filecount"] :
                rawsql='SELECT SUM(VOL.%s) FROM tbl_volume AS Vol2 JOIN tbl_volume AS VOL on Vol2.vid = VOL.parentID WHERE Vol2.vid="%s" AND VOL.servername != Vol2.servername;' % (field,vid)
                self.Logger.debug("Executing %s" % rawsql)
                res = conn.execute(rawsql).fetchall()
                self.Logger.debug("got res=%s" % res)
                try :
                    res_dict[field] += res[0][0]
                except :
                    pass
        transa.commit()
        conn.close()  
        res_dict["blocks_fs"] += res_dict["diskused"]*1024 # XXX diskused is in Kbytes    
        res_dict["files_fs"] += res_dict["filecount"]    
        self.Logger.debug("get_storage_uUsage: returning %s" % res_dict) 
        return res_dict
        
    def get_new_volume_location(self, obj_or_param, VolObj, reservedSpace={}) :
        """
        get a new volume location for a volume in the given project.
        Has to be called separately for RW and external RO.
        If volume already exists, return alternate location.
        For now, only choose on size.
        reservedSpace is substracted from the current free space of fileservers, 
        so that parallel transfers/creations are possible.
        must be of form {"fileserver_uuid" : {"partname" : reservedSpace/kB } }
        """
        self.Logger.debug("called with Prj=%s, VolObj=%s"  % (obj_or_param, VolObj))
        this_project = self.get_object(obj_or_param)
        if not this_project : return None

        if VolObj.type == "RW" :
            sps = this_project.rw_serverparts 
        elif VolObj.type == "RO" :
            sps = this_project.ro_serverparts
        else :
            raise RuntimeError("Invalid Voltype : %s" % VolObj.type)    


        # get locations of Volume
        # check if we're dealing with an existing Volume
        ## XXX does it work with RO, where the RW has been deleted ??
       
        try :
            existing_volume = self._VS.get_volume(VolObj.name, cached=False)
        except :
            existing_volume = []

        if len(existing_volume) > 0 :
            existing_volume = self._VS.get_volume(VolObj.name, cached=False)[0]
            RWVolLocation = (existing_volume.fileserver_uuid, existing_volume.part)
        else :
            self.Logger.debug("Volume of name %s doesn't exist" % VolObj.name)
            RWVolLocation = ()
            if VolObj.type != "RW" :
                raise ProjectServiceError("RW-Volume %s does not exist. Cannot create non-RW volumes for that name." % VolObj.name)

        ROVolLocations=[]
        if VolObj.name[-9:] != ".readonly" :
            use_vol_name = "%s.readonly" % VolObj.name
        else :
            use_vol_name = VolObj.name
        try :
            existingROVols = self._VS.get_volume(use_vol_name, cached=False)
        except :
            existingROVols = []

        for v in existingROVols :
            ROVolLocations.append((v.fileserver_uuid, v.part)) 
        # get PartInfos from livesystem

        PartInfos = {}
        for fileserver_uuid, thisPart in sps :
            this_fs_name = afs.LOOKUP_UTIL[self._CFG.cell].get_hostname_by_fsuuid(fileserver_uuid)
            if not fileserver_uuid in PartInfos : 
                PartInfos[fileserver_uuid] = {}
                for p in self._fsLLA.get_partitions(this_fs_name) :
                    PartInfos[fileserver_uuid][p.name] = p.free 
        # XXX partinfo contains now all partitions    
        self.Logger.debug("PartInfos of Prj %s: %s" % (this_project.name, PartInfos)) 
        self.Logger.debug("ServerPartitions of Prj %s: %s" % (this_project.name, sps)) 
        self.Logger.debug("VolumeLocations: RW: %s  RO:%s" % (RWVolLocation, ROVolLocations)) 
        # find one with most Free size        
        # we need to iterate over sps again, since we might have more partitions
        # than belonging to this project
        maxFree = -1
        fs_name = Part = None
        for fileserver_uuid, thisPart in sps :
            self.Logger.debug("fileserver_uuid =%s, thisPart = %s" % (fileserver_uuid,thisPart)) 
            this_fs_name = afs.LOOKUP_UTIL[self._CFG.CELL_NAME].get_hostname_by_fsuuid(fileserver_uuid)
            if not thisPart in PartInfos[fileserver_uuid].keys() :
                raise ProjectServiceError("Project %s incorrectly defined. Server %s has no partition %s" % (prjname,this_fs_name,thisPart)) 
            if VolObj.type == "RW" :
                # ignore the original SP
                if (fileserver_uuid, thisPart) == RWVolLocation : continue
                haveVolonOtherPart = False
                # if Vol already on dst Server, just consider the corresponding partition
                for o_fileserver_uuid,o_part in ROVolLocations :
                    if o_fileserver_uuid == fileserver_uuid and o_part != thisPart : 
                        haveVolonOtherPart = True
                if haveVolonOtherPart : continue
            elif VolObj.type == "RO" :
                # ignore servers having alread one RO
                skip_it = False
                for ro_srv_uuid, ro_srv_part in ROVolLocations :
                    if fileserver_uuid == ro_srv_uuid :
                        self.Logger.debug("Have already on RO on this server, ignore it.")
                        skip_it = True
                if skip_it :
                    continue
                # if we have a single RW on this SP, ignore other partitions 
                if fileserver_uuid == RWVolLocation[0] and thisPart != RWVolLocation[1] : 
                    self.Logger.debug("this SP is a different Partition on the RW-Server, ignore it.")
                    continue
            else :
                 raise ProjectServiceError("Internal Error. Got invalid volume-type %s" % VolObj.type)
            # substract reservedSpace
            try :
                effective_space = PartInfos[fileserver_uuid][thisPart] - reservedSpace[fileserver_uuid][thisPart]
            except :
                effective_space = PartInfos[fileserver_uuid][thisPart]
            # leave at least 100 GB free on destination server
            if effective_space > maxFree and effective_space > 1024*1024*100 : 
                maxFree = PartInfos[fileserver_uuid][thisPart]
                fs_name = this_fs_name
                Part = thisPart
                self.Logger.debug("best bet so far: srv %s, part %s, max_free: %s" % (fs_name,Part,maxFree) )
        return fs_name, Part

    def update_volume_mappings(self) :
        """
        (Re-)scan the entire cell
        update all ExtVolAttr to current Project definitions
        """
        # cycle through all Projects, collect volumes matching their regex in a dict
        RWVols = {}
        vname_vid_mapping = {}
        Projects = self.get_project_list()
        for prj in Projects :
            self.Logger.debug("Updating Project %s" % prj.name)
            if len(prj.volname_regex) > 0 :
                regEXSQL = 'AND ( name REGEXP ("%s")' % prj.volname_regex[0]
                if len (prj.volname_regex) > 1 :
                    for i in range(1,len(prj.volname_regex)) :
                        regEXSQL += 'OR name REGEXP ("%s") ' %  prj.volname_regex[1]
                rawSQL = 'SELECT vid, name FROM tbl_volume WHERE type="RW" %s );'  % regEXSQL
                for vid, vname in self.DBManager.execute_raw(rawSQL).fetchall() :
                    if vname in prj.excluded_volnames : continue
                    vname_vid_mapping[vname] = vid
                    if RWVols.has_key(vname) :
                        RWVols[vname].append(prj.db_id)
                    else :
                        RWVols[vname] = [prj.db_id,]
            # additional volumes 
            for _vname in prj.additional_volnames :
                if len(_vname) == 0 : continue
                res = self.DBManager.execute_raw('SELECT vid, name FROM tbl_volume WHERE type="RW" and name="%s"' % _vname ).fetchone()
                if res == None : raise ProjectServiceError('Project %s corrupted. additional Volume "%s" does not exist.' % (prj.name, _vname))
                vid, vname = res
                vname_vid_mapping[vname] = vid
                if RWVols.has_key(vname) :
                    if prj.db_id in RWVols[vname] :
                        self.Logger.warning("Project %s: Volume %s already caught by regexes." % (prj.name,vname))
                    RWVols[vname].append(prj.db_id)
                else :
                    RWVols[vname] = [prj.db_id,]

        # create dict of Projects, prjid is key
        Prjs={} 
        for p in Projects :
            Prjs[p.db_id] = p
        # clean list of nested projects for one volume. 

        # a volume should have only leaf projects
        for vname in RWVols :
            if len(RWVols[vname]) <= 1 : continue
            self.Logger.debug("clean up nested projects for RWVols[%s]=%s" % (vname, RWVols[vname]))
            prj_hierarchy = self.get_projects_by_volume_name(vname)
            
            #for prjid in RWVols[v] :
            #    if Prjs[prjid].NestingLevel == 0 : continue
            #    if Prjs[prjid].NestingLevel > lowestNest :
            #        self.Logger.debug("Removing prj with id=%s" % prjid)
            #        removals.append(prjid)
            #for r in removals :
            #    RWVols[v].remove(r)
    

        for vname in RWVols :
            vid = vname_vid_mapping[vname]
            self.Logger.debug("processing v=%s"  % vid)
            if vid == None : 
                self.Logger.warn("got a None in vols=%s" % RWVols)
                continue
            self.Logger.debug("processing v=%s"  % RWVols[vname])
            project_ids = RWVols[vname]
            self.Logger.debug("project_ids=%s"  % project_ids)
            this_ext_volume_attributes = self.DBManager.get_from_cache(ExtVolAttr, vid=vid, fresh_only=False, must_be_unique=True)
            if this_ext_volume_attributes != None :
                this_ext_volume_attributes.project_ids = project_ids 
            else :
                this_ext_volume_attributes = ExtVolAttr() 
                this_ext_volume_attributes.vid = vid
                this_ext_volume_attributes.project_ids = project_ids
                this_ext_volume_attributes.num_min_ro = 2
                this_ext_volume_attributes.owner = "N/A"
                this_ext_volume_attributes.pinned_on_server = 0
            this_ext_volume_attributes.update_db_repr()
            self.DBManager.set_into_cache(ExtVolAttr, this_ext_volume_attributes, vid=vid )
        for p in Projects :
            self.update_server_spread(p)
        return 
