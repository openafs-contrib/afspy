import re,json,datetime

from afs.model.Project import Project
from afs.model.ProjectSpread import ProjectSpread
from afs.service.BaseService import BaseService
from afs.exceptions.AfsError import AfsError
from afs.service.OSDVolService import OSDVolService
from afs.service.FsService import FsService
from afs.model.ExtendedVolumeAttributes import ExtVolAttr
from afs.model.ExtendedVolumeAttributes_OSD import ExtVolAttr_OSD
import afs

class ProjectService(BaseService):
    """
    Provides Service about Project management.
    This deals only with the DBCache.
    """
   
    def __init__(self, conf=None):
        BaseService.__init__(self, conf, DAOList=["fs"])
        if not self._CFG.DB_CACHE:
            raise AfsError('Error, Projects work only with a DBCache defined ',None)
        self.ModelObj=Project()
        self._VS = OSDVolService()
        self._FS = FsService()
        return
        
    def getProjectByName(self, name) :
        """
        return ProjectObj from Projectname
        """
        thisProject=self.DBManager.getFromCache(Project,name=name)
        return thisProject
   
    def deleteProject(self,name_or_obj) :
        """
        remove on project from the database. 
        take name as string or ProjectObject
        """
        if  isinstance(name_or_obj, basestring) :
            PrjName = name_or_obj
        else :
            try :
                PrjName = name_or_obj.name
            except :
                raise AfsError("Name of prj (string) or Project instance required.") 
        return self.DBManager.deleteFromCache(Project,name=PrjName)
        
    def getProjectsByVolumeName(self, volname):
        """
        return List of Projects Objs from VolumeName.
        This list is sorted by the Nesting Level of the projects
        """
        unsortedList=[]
        sortedList=[]
        for p in self.DBManager.getFromCache(Project,mustBeUnique=False) :
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

    def getAssignedServers(self,prjname) :
        """
        return lists of (fs-name,part) tuples
        for RW and RO.
        So basically it is like rw_serverparts and ro_serverparts, but the 
        uuids replaced by hostnames.
        """
        thisProject=self.getProjectByName(prjname)
        if not thisProject : return None
        RWList = [] 
        ROList = []
        for serv_uuid,part in thisProject.rw_serverparts :
            FsName=afs.LookupUtil[self._CFG.CELL_NAME].getHostnameByFSUUID(serv_uuid)
            RWList.append((FsName,part),)
        for serv_uuid,part in thisProject.ro_serverparts :
            FsName=afs.LookupUtil[self._CFG.CELL_NAME].getHostnameByFSUUID(serv_uuid)
            ROList.append((FsName,part),)
        return RWList,ROList


    def getProjectsOnServer(self, name_or_obj) :
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
                raise AfsError("Name of server (string) or Fileserver-Instance required.")
        FSUUID=afs.LookupUtil[self._CFG.CELL_NAME].getFSUUID(FSName)
        result_dict={}
        for p in self._FS.getPartitions(FSName) :
            result_dict[p]=[]
            for prj_spread in self.DBManager.getFromCache(ProjectSpread, mustBeUnique=False, serv_uuid=FSUUID, part=p) :
                result_dict[p].append({ "project"  : self.DBManager.getFromCache(Project,id=prj_spread.project_id), "spread" : prj_spread})
        return result_dict
 
    def getServerSpread(self, prjname, cached = True):
        """
        return dict of lists of ProjectSpread Objects :
        [VolType]=[ProjectSpread]
        """
        thisProject=self.getProjectByName(prjname)
        if not thisProject : return None
        ResDict = {"RW" : [], "RO" : [], "BK" : []}

        if cached :
            for vol_type in ResDict :
                ResDict[vol_type]=self.DBManager.getFromCache(ProjectSpread, mustBeUnique=False, vol_type=vol_type, project_id = thisProject.id)
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
                    OSDAttributes = self._VS.getExtVolAttr_OSD(vol.vid)
                    if OSDAttributes == None :
                        OSDAttributes = ExtVolAttr_OSD()
                        v = self._VS.getVolume(vol.vid,cached=True)
                        # satisfy OSD attributes
                        OSDAttributes.blocks_fs = v[0].diskused

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
                        thisPrjSPObj.project_id = thisProject.id
                        thisPrjSPObj.part = Part
                        thisPrjSPObj.serv_uuid = FSUUID    
                        thisPrjSPObj.vol_type = vol_type
                    
                    thisPrjSPObj.num_vol += 1 
                    thisPrjSPObj.blocks_fs += OSDAttributes.blocks_fs
                    thisPrjSPObj.blocks_osd_on += OSDAttributes.blocks_osd_on
                    thisPrjSPObj.blocks_osd_off += OSDAttributes.blocks_osd_off
                    if ResDictIndex == -1 :
                        ResDict[vol_type].append(thisPrjSPObj)
                    else :
                        ResDict[vol_type][ResDictIndex] = thisPrjSPObj

        if self._CFG.DB_CACHE :
            for vol_type in ResDict :
                for thisPrjSPObj in ResDict[vol_type] :
                    self.DBManager.setIntoCache(ProjectSpread, thisPrjSPObj, vol_type=vol_type, project_id=thisPrjSPObj.project_id, serv_uuid=thisPrjSPObj.serv_uuid, part=thisPrjSPObj.part)
        return ResDict

    def getVolumeIDs(self,prjname,servers=None) :
        """
        return list of Volume IDs part of this project.
        servers is an optional list of server_uuids to be used. 
        """
        self.Logger.debug("Entering with prjname=%s and servers=%s" % (prjname,servers))
        thisProject=self.getProjectByName(prjname)
        if not thisProject : 
            self.Logger.debug("Invalid project-name %s given.", prjname)
            return None
        list = self.DBManager.getFromCacheByListElement(ExtVolAttr,ExtVolAttr.projectIDs_js,thisProject.id,mustBeUnique=False)
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
                for v in self._VS.getVolume(l.vid,cached=True) :
                    self.Logger.debug("Comparing '%s' to '%s'" % (v.serv_uuid,servers))
                    if v.serv_uuid in servers :
                        VolIDList.append(l.vid)
        return VolIDList

    def getStorageUsage(self,prjname) :
        """
        return dict of storage usage for given project.
        """
        thisProject=self.getProjectByName(prjname)
        if not thisProject : return None
        resDict={}
        conn = self._CFG.DB_ENGINE.connect()
        transa = conn.begin()
        RegEx="\\\[({0}|.*, {0}|{0},.*|.*, {0},.*)\\\]".format(thisProject.id)
        # osd volumes
        for field in ["files_fs","files_osd","blocks_fs","blocks_osd_on","blocks_osd_off"] :
            rawsql='SELECT SUM(EOSD.%s) FROM tbl_extvolattr AS E JOIN tbl_extvolattr_osd AS EOSD on E.vid = EOSD.vid WHERE E.projectIDs_js REGEXP "%s";' % (field,RegEx)
            self.Logger.debug("Executing %s" % rawsql)
            res = conn.execute(rawsql).fetchall()
            self.Logger.debug("got res=%s" % res)
            try : 
                resDict[field] = res[0][0]
            except :
                resDict[field] = 0
            if resDict[field] == None : resDict[field] = 0
        # openafs volumes
        # this is not very efficient
        # for external RO we need the list of vids
        # get VolIDs of osd volumes first.
        rawsql='SELECT E.vid  FROM tbl_extvolattr AS E JOIN tbl_extvolattr_osd AS EOSD on E.vid = EOSD.vid WHERE E.projectIDs_js REGEXP "%s";' % (RegEx)
        self.Logger.debug("Executing %s" % rawsql)
        res = conn.execute(rawsql).fetchall()
        self.Logger.debug("got res=%s" % res)
        OSD_VolIDs=[]
        for vid in res :
            OSD_VolIDs.append(vid[0])
        
        # all vids
        rawsql='SELECT E.vid FROM tbl_extvolattr AS E JOIN tbl_volume AS VOL on E.vid = VOL.vid WHERE E.projectIDs_js REGEXP "%s";' % (RegEx)
        self.Logger.debug("Executing %s" % rawsql)
        res = conn.execute(rawsql).fetchall()
        self.Logger.debug("got res=%s" % res)
        VolIDs=[]
        for vid in res :
            if not vid[0] in OSD_VolIDs :   # do not add OSD-Volumes
                VolIDs.append(vid[0])
        
        self.Logger.debug("VolIDs=%s,OSD_VolIDs=%s" % (VolIDs,OSD_VolIDs))
        resDict["diskused"]=0  
        resDict["filecount"]=0  
       
        for vid in VolIDs :
            for field in ["diskused","filecount"] :
                rawsql='SELECT %s FROM tbl_volume  WHERE vid="%s";' % (field,vid)
                self.Logger.debug("Executing %s" % rawsql)
                res = conn.execute(rawsql).fetchall()
                self.Logger.debug("got res=%s" % res)
                try :
                    resDict[field] += res[0][0]
                except :
                    resDict[field] = 0
                if resDict[field] == None : resDict[field] = 0

            for field in ["diskused","filecount"] :
                rawsql='SELECT SUM(VOL.%s) FROM tbl_volume AS Vol2 JOIN tbl_volume AS VOL on Vol2.vid = VOL.parentID WHERE Vol2.vid="%s" AND VOL.servername != Vol2.servername;' % (field,vid)
                self.Logger.debug("Executing %s" % rawsql)
                res = conn.execute(rawsql).fetchall()
                self.Logger.debug("got res=%s" % res)
                try :
                    resDict[field] += res[0][0]
                except :
                    pass
        transa.commit()
        conn.close()  
        resDict["blocks_fs"] += resDict["diskused"]*1024 # XXX diskused is in Kbytes, osd stuff in bytes!    
        resDict["files_fs"] += resDict["filecount"]    
        self.Logger.debug("getStorageUsage: returning %s" % resDict) 
        return resDict
        
    def getProjectList(self) :
        """
        return list of ProjectDicts
        """
        projList=self.DBManager.getFromCache(Project,mustBeUnique=False) 
        return projList

    def saveProject(self,prjObj):
        """
        store object into DBCache
        """
        self.Logger.debug("saveProject: Class=%s\nObj=%s" % (Project,prjObj))
        self.DBManager.setIntoCache(Project,prjObj,name=prjObj.name)
        return 

    def getNewVolumeLocation(self, prjname, VolObj, reservedSpace={}) :
        """
        get a new volume location for a volume in the given project.
        Has to be called separately for RW and external RO.
        If volume already exists, return alternate location.
        For now, only choose on size.
        reservedSpace is substracted from the current free space of fileservers, 
        so that parallel transfers/creations are possible.
        must be of form {"serv_uuid" : {"partname" : reservedSpace/kB } }
        """
        self.Logger.debug("called with Prj=%s, VolObj=%s"  % (prjname,VolObj))
        thisProject = self.getProjectByName(prjname)
        if not thisProject : return None

        if VolObj.type == "RW" :
            sps = thisProject.rw_serverparts 
        elif VolObj.type == "RO" :
            sps = thisProject.ro_serverparts
        else :
            raise RuntimeError("Invalid Voltype : %s" % VolObj.type)    


        # get locations of Volume
        # check if we're dealing with an existing Volume
        ## XXX does it work with RO, where the RW has been deleted ??
       
        try :
            existingVol = self._VS.getVolume(VolObj.name, cached=False)
        except :
            existingVol = []

        if len(existingVol) > 0 :
            existingVol = self._VS.getVolume(VolObj.name, cached=False)[0]
            RWVolLocation = (existingVol.serv_uuid,existingVol.part)
        else :
            self.Logger.debug("Volume of name %s doesn't exist" % VolObj.name)
            RWVolLocation=()
            if VolObj.type != "RW" :
                raise AfsError("RW-Volume %s does not exist. Cannot create non-RW volumes for that name." % VolObj.name)

        ROVolLocations=[]
        if VolObj.name[-9:] != ".readonly" :
            use_vol_name = "%s.readonly" % VolObj.name
        else :
            use_vol_name = VolObj.name
        try :
            existingROVols=self._VS.getVolume(use_vol_name, cached=False)
        except :
            existingROVols=[]

        for v in existingROVols :
            ROVolLocations.append((v.serv_uuid,v.part)) 
        # get PartInfos from livesystem

        PartInfos={}
        for serv_uuid, thisPart in sps :
            thisFSName = afs.LookupUtil[self._CFG.CELL_NAME].getHostnameByFSUUID(serv_uuid)
            if not serv_uuid in PartInfos : 
                PartInfos[serv_uuid] = {}
                for p in self._fsDAO.getPartList(thisFSName) :
                    PartInfos[serv_uuid][p["name"]] = p["free"] 
        # XXX partinfo contains now all partitions    
        self.Logger.debug("PartInfos of Prj %s: %s" % (thisProject.name,PartInfos)) 
        self.Logger.debug("ServerPartitions of Prj %s: %s" % (thisProject.name,sps)) 
        self.Logger.debug("VolumeLocations: RW: %s  RO:%s" % (RWVolLocation, ROVolLocations)) 
        # find one with most Free size        
        # we need to iterate over sps again, since we might have more partitions
        # than belonging to this project
        maxFree = -1
        FsName = Part = None
        for serv_uuid, thisPart in sps :
            self.Logger.debug("serv_uuid =%s, thisPart = %s" % (serv_uuid,thisPart)) 
            thisFSName = afs.LookupUtil[self._CFG.CELL_NAME].getHostnameByFSUUID(serv_uuid)
            if not thisPart in PartInfos[serv_uuid].keys() :
                raise AfsError("Project %s incorrectly defined. Server %s has no partition %s" % (prjname,thisFSName,thisPart)) 
            if VolObj.type == "RW" :
                # ignore the original SP
                if (serv_uuid, thisPart) == RWVolLocation : continue
                haveVolonOtherPart=False
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
                 raise AfsError("Internal Error. Got invalid volume-type %s" % VolObj.type)
            # substract reservedSpace
            try :
                effectiveSpace = PartInfos[serv_uuid][thisPart] - reservedSpace[serv_uuid][thisPart]
            except :
                effectiveSpace = PartInfos[serv_uuid][thisPart]
            # leave at least 100 GB free on destination server
            if effectiveSpace > maxFree and effectiveSpace > 1024*1024*100 : 
                maxFree = PartInfos[serv_uuid][thisPart]
                FsName = thisFSName
                Part = thisPart
                self.Logger.debug("best bet so far: srv %s, part %s, max_free: %s" % (FsName,Part,maxFree) )
        return FsName, Part

    def updateVolumeMappings(self) :
        """
        update all ExtVolAttr to current Project definitions
        """
        # cycle through all Projects, collect volumes matching their regex in a dict
        RWVols={}
        Projects=self.getProjectList()
        for prj in Projects :
            self.Logger.debug("Updating Project %s" % prj.name)
            if len(prj.volnameRegEx) > 0 :
                regEXSQL='AND ( name REGEXP ("%s")' % prj.volnameRegEx[0]
                if len (prj.volnameRegEx) > 1 :
                    for i in range(1,len(prj.volnameRegEx)) :
                        regEXSQL += 'OR name REGEXP ("%s") ' %  prj.volnameRegEx[1]
                rawSQL='SELECT vid,name FROM tbl_volume WHERE type="RW" %s );'  % regEXSQL
                for vid,name in self.DBManager.executeRaw(rawSQL).fetchall() :
                    if name in prj.excludedVolnames : continue
                    if RWVols.has_key(vid) :
                        RWVols[vid].append(prj.id)
                    else :
                        RWVols[vid]=[prj.id,]
            # additional volumes 
            for name in prj.additionalVolnames :
                if len(name) == 0 : continue
                res=self.DBManager.executeRaw('SELECT vid,name FROM tbl_volume WHERE type="RW" and name="%s"'% name ).fetchone()
                if res == None : raise AfsError('Project %s corrupted. additional Volume "%s" does not exist.' % (prj.name,name))
                vid,vname=res
                if RWVols.has_key(vid) :
                    if prj.id in RWVols[vid] :
                        self.Logger.warning("Project %s: Volume %s already caught by regexes." % (prj.name,vname))
                    RWVols[vid].append(prj.id)
                else :
                    RWVols[vid]=[prj.id,]
   

        # create dict of Projects, prjid is key
        Prjs={} 
        for p in Projects :
            Prjs[p.id]=p
        # clean list of nested projects for one volume. 

        # a volume should have only the one with the lowest nesting-level
        for v in RWVols :
            if len(RWVols[v]) <= 1 : continue
            self.Logger.debug("clean up nested projects for RWVols[%s]=%s" % (v,RWVols[v]))
            lowestNest=-1
            for prjid in RWVols[v] :
                if lowestNest == -1 : lowestNest=Prjs[prjid].NestingLevel
                if Prjs[prjid].NestingLevel < lowestNest :
                    lowestNest = Prjs[prjid].NestingLevel    
            self.Logger.debug("got lowest nesting-level = %s" % lowestNest) 
            removals=[]
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
        updates=[]
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
            projectIDs_js=json.dumps(RWVols[vid])
            self.Logger.debug("projectIDs_js=%s"  % projectIDs_js)
            if vid in updates :
                rawsql="""UPDATE tbl_extvolattr SET projectIDs_js='%s', udate='%s' WHERE vid = '%s';""" % (projectIDs_js, udate,vid)
                self.Logger.debug("Updating: %s" % vid)
            else :
                mincopy = 2
                owner = "N/A"
                pinnedOnServer=0
                rawsql="""INSERT INTO tbl_extvolattr (vid, mincopy, owner, projectIDs_js, pinnedOnServer,udate, cdate) VALUES ('%s','%s','%s','%s','%s','%s','%s');""" % (vid, mincopy, owner, projectIDs_js, pinnedOnServer, udate, cdate)
                self.Logger.debug("Inserting: %s" % vid)
            res = conn.execute(rawsql)
        transa.commit()
        conn.close()  
        return 
