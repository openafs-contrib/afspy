import re,json,datetime

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
            this_Project = obj_or_param
        else : 
            this_Project = self.DBManager.get_from_cache(Project, fresh_only=False, name=obj_or_param)
            self.Logger.debug("get_object: name %s gave %s" % (obj_or_param, this_Project))

        return this_Project

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
        this_Project = self.get_object(name_or_obj)
        return self.DBManager.delete_from_cache(Project, name=this_Project.name)

    def store_project(self, this_Project):
        """
        store object into DBCache
        """
        self.Logger.debug("store_project: Obj=%s" % (this_Project))
        this_Project.update_db_repr()
        self.DBManager.set_into_cache(Project, this_Project, name=this_Project.name)
        # we need to return the object from the DB to set db_id. 
        return self.get_object(this_Project.name)

    def get_project_by_name(self, name) :
        """
        return ProjectObj from Projectname
        """
        self.Logger.debug("get_project_by_name: called with name='%s'" % name)
        # Note: fresh_only must be false for all get_from_cache operations,
        # otherwise we get None
        this_Project = self.DBManager.get_from_cache(Project, fresh_only=False, name="%s" % name)
        return this_Project
   
    def get_project_list(self) :
        """
        return list of ProjectObjects
        """
        project_list = self.DBManager.get_from_cache(Project, fresh_only=False, mustBeUnique=False) 
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
        this_Project = self.get_object(obj_or_param)
        if not this_Project : return None
        rw_list = [] 
        ro_list = []
        for serv_uuid, part in this_Project.rw_serverparts :
            fs_name = afs.LOOKUP_UTIL[self._CFG.cell].get_hostname_by_fsuuid(serv_uuid)
            rw_list.append((fs_name,part),)
        for serv_uuid, part in this_Project.ro_serverparts :
            fs_name = afs.LOOKUP_UTIL[self._CFG.cell].get_hostname_by_fsuuid(serv_uuid)
            ro_list.append((fs_name,part),)
        return rw_list, ro_list

    def add_server_partition(self, obj_or_param, server_partition, volume_type) :
        """
        assign a server_partition to a project
        """
        this_Project = self.get_object(obj_or_param)
        fs_name, part = server_partition
        serv_uuid = afs.LOOKUP_UTIL[self._CFG.cell].get_fsuuid(fs_name)
        part = afs.util.misc.canonicalize_partition(part)
        if volume_type == "RW" :
            this_Project.rw_serverparts.append((serv_uuid, part))
        elif volume_type == "RO" :
            this_Project.ro_serverparts.append((serv_uuid, part))
        else :
            raise RuntimeError("assign_server_partition: Invalid volume_type '%s'" % volume_type)
        self.store_project(this_Project)
        return this_Project

    def remove_server_partition(self, obj_or_param, server_partition, volume_type) :
        """
        remove server_partition assignment from a project
        """
        this_Project = self.get_object(obj_or_param)
        self.Logger.debug("called with: server_partition=%s, this_Project=%s" % (server_partition, this_Project) )
        fs_name, part = server_partition
        serv_uuid = afs.LOOKUP_UTIL[self._CFG.cell].get_fsuuid(fs_name)
        part = afs.util.misc.canonicalize_partition(part)
        if volume_type == "RW" :
            this_Project.rw_serverparts.remove((serv_uuid, part))
        elif volume_type == "RO" :
            this_Project.ro_serverparts.remove((serv_uuid, part))
        else :
            raise RuntimeError("resign_server_partition: Invalid volume_type '%s'" % volume_type)
        self.store_project(this_Project)
        return this_Project

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
        set the parent of an object
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
        parent_project = self.DBManager.get_from_cache(Project, fresh_only=False, mustBeUnique=True, db_id = this_project.parent_db_id)
        return parent_project 

    def set_owner(self, obj_or_param, owner) :
        """
        set the owner attribute
        """
        this_project = self.get_object(obj_or_param)
        this_project.owner = owner
        self.store_project(this_project)
        return this_project


#
# methods scanning cell 
#
    
    def get_projects_by_volume_name(self, volname):
        """
        return List of Projects Objs from VolumeName.
        This list is sorted by the Nesting Level of the projects
        """
        unsortedList=[]
        sortedList=[]
        for p in self.DBManager.get_from_cache(Project, fresh_only=False, mustBeUnique=False) :
            pDict=p.getDict()
            for rx in pDict["volnameRegEx"] :
                if re.compile(rx).match(volname) :
                     unsortedList.append(p)
        # sort list by Nesting-Level of Projects
        tmpDict={} 
        for p in unsortedList :
            if p.NestingLevel in tmpDict.keys() :
                tmpDict[p.NestingLevel].append(p)
            else :
                tmpDict[p.NestingLevel]=[p]
        tmpKeys=tmpDict.keys()
        tmpKeys.sort()
        for k in tmpKeys :
            for p in tmpDict[k] :
                sortedList.append(p)
        return sortedList

    def get_projects_on_server(self, name_or_obj) :
        """
        return dict[Partition] of lists of [ProjectNames] for a fileserver
        """
        ProjectList=self.getProjectList()
        if isinstance(name_or_obj, basestring) :
            FSName = name_or_obj
        else :
            try :
                FSName = name_or_obj.hostnames[0]
            except :
                raise ProjectServiceError("Name of server (string) or Fileserver-Instance required.")
        FSUUID=afs.LOOKUP_UTIL[self._CFG.cell].getFSUUID(FSName)
        if cached :
            res_dict={}
            for p in self._FS.getPartitions(FSName) :
                res_dict[p]=[]
                for prj in self.DBManager.get_from_cache(ProjectSpread, fresh_only=False, mustBeUnique=False, serv_uuid=FSUUID, part=p) :
                    res_dict[p].append(prj)
            return res_dict
 
    def get_server_spread(self, prjname, cached = True):
        """
        return dict of lists of ProjectSpread Objects :
        [VolType]=[ProjectSpread]
        """
        this_Project=self.getProjectByName(prjname)
        if not this_Project : return None
        ResDict = {"RW" : [], "RO" : [], "BK" : []}

        if cached :
            for vol_type in ResDict :
                ResDict[vol_type]=self.DBManager.get_from_cache(ProjectSpread, fresh_only=False, mustBeUnique=False, vol_type=vol_type, project_id = this_Project.id)
            return ResDict
              
        VolIDList = self.getVolumeIDs(prjname)
        if VolIDList == None : return None
        for v in VolIDList :
            VolGroup = self._VS.getVolGroup(v) 
            for vol_type in ResDict :
                if VolGroup[vol_type] == None : continue
                for vol in VolGroup[vol_type] :
                    FSUUID = vol.serv_uuid
                    Part = vol.part

                    thisPrjSPObj = None
                    ResDictIndex = -1
                    for i in range(len(ResDict[vol_type])) :
                        prjspObj = ResDict[vol_type][i]
                        self.Logger.debug("comparing %s,%s,%s with %s,%s,%s" % (prjspObj.serv_uuid, prjspObj.part, prjspObj.vol_type, FSUUID, Part, vol_type) )
                        if prjspObj.serv_uuid == FSUUID and prjspObj.part == Part and prjspObj.vol_type == vol_type :
                            thisPrjSPObj=prjspObj
                            ResDictIndex=i
                            break

                    if thisPrjSPObj == None :
                        thisPrjSPObj = ProjectSpread()
                        thisPrjSPObj.project_id = this_Project.id
                        thisPrjSPObj.part = Part
                        thisPrjSPObj.serv_uuid = FSUUID    
                        thisPrjSPObj.vol_type = vol_type
                    
                    thisPrjSPObj.num_vol += 1 
                    if ResDictIndex == -1 :
                        ResDict[vol_type].append(thisPrjSPObj)
                    else :
                        ResDict[vol_type][ResDictIndex] = thisPrjSPObj

        if self._CFG.DB_CACHE :
            for vol_type in ResDict :
                for thisPrjSPObj in ResDict[vol_type] :
                    self.DBManager.setIntoCache(ProjectSpread, thisPrjSPObj, vol_type=vol_type, project_id=thisPrjSPObj.project_id, serv_uuid=thisPrjSPObj.serv_uuid, part=thisPrjSPObj.part)
        return ResDict

    def get_volume_IDs(self, prjname, servers=None) :
        """
        return list of Volume IDs part of this project.
        servers is an optional list of server_uuids to be used. 
        """
        self.Logger.debug("Entering with prjname=%s and servers=%s" % (prjname,servers))
        this_Project = self.getProjectByName(prjname)
        if not this_Project : 
            self.Logger.debug("Invalid project-name %s given.", prjname)
            return None
        list = self.DBManager.getFromCacheByListElement(ExtVolAttr, ExtVolAttr.projectIDs_js, this_Project.id, fresh_only=False, mustBeUnique=False)
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
                for v in self._VS.get_volume(l.vid,cached=True) :
                    self.Logger.debug("Comparing '%s' to '%s'" % (v.serv_uuid,servers))
                    if v.serv_uuid in servers :
                        VolIDList.append(l.vid)
        return VolIDList

    def get_storage_usage(self, prjname) :
        """
        return dict of storage usage for given project.
        """
        this_Project=self.getProjectByName(prjname)
        if not this_Project : return None
        res_dict={}
        conn = self._CFG.DB_ENGINE.connect()
        transa = conn.begin()
        RegEx="\\\[({0}|.*, {0}|{0},.*|.*, {0},.*)\\\]".format(this_Project.id)
        # openafs volumes
        # this is not very efficient
        # for external RO we need the list of vids
        # all vids
        rawsql='SELECT E.vid FROM tbl_extvolattr AS E JOIN tbl_volume AS VOL on E.vid = VOL.vid WHERE E.projectIDs_js REGEXP "%s";' % (RegEx)
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
        must be of form {"serv_uuid" : {"partname" : reservedSpace/kB } }
        """
        self.Logger.debug("called with Prj=%s, VolObj=%s"  % (obj_or_param, VolObj))
        this_Project = self.get_object(obj_or_param)
        if not this_Project : return None

        if VolObj.type == "RW" :
            sps = this_Project.rw_serverparts 
        elif VolObj.type == "RO" :
            sps = this_Project.ro_serverparts
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
            RWVolLocation = (existing_volume.serv_uuid,existing_volume.part)
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
            ROVolLocations.append((v.serv_uuid, v.part)) 
        # get PartInfos from livesystem

        PartInfos = {}
        for serv_uuid, thisPart in sps :
            this_fs_name = afs.LOOKUP_UTIL[self._CFG.cell].get_hostname_by_fsuuid(serv_uuid)
            if not serv_uuid in PartInfos : 
                PartInfos[serv_uuid] = {}
                for p in self._fsLLA.get_partitions(this_fs_name) :
                    PartInfos[serv_uuid][p.name] = p.free 
        # XXX partinfo contains now all partitions    
        self.Logger.debug("PartInfos of Prj %s: %s" % (this_Project.name, PartInfos)) 
        self.Logger.debug("ServerPartitions of Prj %s: %s" % (this_Project.name, sps)) 
        self.Logger.debug("VolumeLocations: RW: %s  RO:%s" % (RWVolLocation, ROVolLocations)) 
        # find one with most Free size        
        # we need to iterate over sps again, since we might have more partitions
        # than belonging to this project
        maxFree = -1
        fs_name = Part = None
        for serv_uuid, thisPart in sps :
            self.Logger.debug("serv_uuid =%s, thisPart = %s" % (serv_uuid,thisPart)) 
            this_fs_name = afs.LOOKUP_UTIL[self._CFG.CELL_NAME].get_hostname_by_fsuuid(serv_uuid)
            if not thisPart in PartInfos[serv_uuid].keys() :
                raise ProjectServiceError("Project %s incorrectly defined. Server %s has no partition %s" % (prjname,this_fs_name,thisPart)) 
            if VolObj.type == "RW" :
                # ignore the original SP
                if (serv_uuid, thisPart) == RWVolLocation : continue
                haveVolonOtherPart = False
                # if Vol already on dst Server, just consider the corresponding partition
                for o_serv_uuid,o_part in ROVolLocations :
                    if o_serv_uuid == serv_uuid and o_part != thisPart : 
                        haveVolonOtherPart = True
                if haveVolonOtherPart : continue
            elif VolObj.type == "RO" :
                # ignore servers having alread one RO
                skip_it = False
                for ro_srv_uuid, ro_srv_part in ROVolLocations :
                    if serv_uuid == ro_srv_uuid :
                        self.Logger.debug("Have already on RO on this server, ignore it.")
                        skip_it = True
                if skip_it :
                    continue
                # if we have a single RW on this SP, ignore other partitions 
                if serv_uuid == RWVolLocation[0] and thisPart != RWVolLocation[1] : 
                    self.Logger.debug("this SP is a different Partition on the RW-Server, ignore it.")
                    continue
            else :
                 raise ProjectServiceError("Internal Error. Got invalid volume-type %s" % VolObj.type)
            # substract reservedSpace
            try :
                effective_space = PartInfos[serv_uuid][thisPart] - reservedSpace[serv_uuid][thisPart]
            except :
                effective_space = PartInfos[serv_uuid][thisPart]
            # leave at least 100 GB free on destination server
            if effective_space > maxFree and effective_space > 1024*1024*100 : 
                maxFree = PartInfos[serv_uuid][thisPart]
                fs_name = this_fs_name
                Part = thisPart
                self.Logger.debug("best bet so far: srv %s, part %s, max_free: %s" % (fs_name,Part,maxFree) )
        return fs_name, Part

    def update_volume_mappings(self) :
        """
        update all ExtVolAttr to current Project definitions
        """
        # cycle through all Projects, collect volumes matching their regex in a dict
        RWVols = {}
        Projects = self.getProjectList()
        for prj in Projects :
            self.Logger.debug("Updating Project %s" % prj.name)
            if len(prj.volnameRegEx) > 0 :
                regEXSQL = 'AND ( name REGEXP ("%s")' % prj.volnameRegEx[0]
                if len (prj.volnameRegEx) > 1 :
                    for i in range(1,len(prj.volnameRegEx)) :
                        regEXSQL += 'OR name REGEXP ("%s") ' %  prj.volnameRegEx[1]
                rawSQL='SELECT vid,name FROM tbl_volume WHERE type="RW" %s );'  % regEXSQL
                for vid, name in self.DBManager.executeRaw(rawSQL).fetchall() :
                    if name in prj.excludedVolnames : continue
                    if RWVols.has_key(vid) :
                        RWVols[vid].append(prj.id)
                    else :
                        RWVols[vid] = [prj.id,]
            # additional volumes 
            for name in prj.additionalVolnames :
                if len(name) == 0 : continue
                res = self.DBManager.executeRaw('SELECT vid,name FROM tbl_volume WHERE type="RW" and name="%s"'% name ).fetchone()
                if res == None : raise ProjectServiceError('Project %s corrupted. additional Volume "%s" does not exist.' % (prj.name,name))
                vid, vname = res
                if RWVols.has_key(vid) :
                    if prj.id in RWVols[vid] :
                        self.Logger.warning("Project %s: Volume %s already caught by regexes." % (prj.name,vname))
                    RWVols[vid].append(prj.id)
                else :
                    RWVols[vid] = [prj.id,]
   

        # create dict of Projects, prjid is key
        Prjs={} 
        for p in Projects :
            Prjs[p.id] = p
        # clean list of nested projects for one volume. 

        # a volume should have only a leaf project
        for v in RWVols :
            if len(RWVols[v]) <= 1 : continue
            self.Logger.debug("clean up nested projects for RWVols[%s]=%s" % (v,RWVols[v]))
            lowestNest = -1
            for prjid in RWVols[v] :
                if lowestNest == -1 : lowestNest=Prjs[prjid].NestingLevel
                if Prjs[prjid].NestingLevel < lowestNest :
                    lowestNest = Prjs[prjid].NestingLevel    
            self.Logger.debug("got lowest nesting-level = %s" % lowestNest) 
            removals = []
            for prjid in RWVols[v] :
                if Prjs[prjid].NestingLevel == 0 : continue
                if Prjs[prjid].NestingLevel > lowestNest :
                    self.Logger.debug("Removing prj with id=%s" % prjid)
                    removals.append(prjid)
            for r in removals :
                RWVols[v].remove(r)
    
        # store assorted stuff in DB 
        conn = self._CFG.DB_ENGINE.connect()
        transa = conn.begin()
        # scan  server/partition for volids to insert/update
        cdate = udate =datetime.datetime(1970, 1, 1).now()
        updates = []
        for v in RWVols :
            rawsql = 'SELECT vid FROM tbl_extvolattr WHERE vid="%s"' % (v)
            for _vid in conn.execute(rawsql).fetchall() :
                if _vid[0] != None :
                    updates.append(_vid[0])

        for vid in RWVols :
            self.Logger.debug("processing v=%s"  % vid)
            if vid == None : 
                self.Logger.warn("got a None in vols=%s" % RWVols)
                continue
            self.Logger.debug("processing v=%s"  % RWVols[vid])
            #projectIDs_js=json.dumps(map(lambda x: "%s" % x ,RWVols[vid]))
            projectIDs_js = json.dumps(RWVols[vid])
            self.Logger.debug("projectIDs_js=%s"  % projectIDs_js)
            if vid in updates :
                rawsql = """UPDATE tbl_extvolattr SET projectIDs_js='%s', udate='%s' WHERE vid = '%s';""" % (projectIDs_js, udate,vid)
                self.Logger.debug("Updating: %s" % vid)
            else :
                mincopy = 2
                owner = "N/A"
                pinnedOnServer = 0
                rawsql = """INSERT INTO tbl_extvolattr (vid, mincopy, owner, projectIDs_js, pinnedOnServer,udate, cdate) VALUES ('%s','%s','%s','%s','%s','%s','%s');""" % (vid, mincopy, owner, projectIDs_js, pinnedOnServer, udate, cdate)
                self.Logger.debug("Inserting: %s" % vid)
            res = conn.execute(rawsql)
        transa.commit()
        conn.close()  
        return 
