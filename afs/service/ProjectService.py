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

    def getVolumeIDs(self,prjname) :
        """
        return list of Volume IDs part of this project
        """
        thisProject=self.getProjectByName(prjname)
        if not thisProject : return None
        list = self.DBManager.getFromCacheByListElement(ExtVolAttr,ExtVolAttr.projectIDs_js,thisProject.id,mustBeUnique=False)
        if list == None :
            return []
        VolIDList=[]
        for l in list :
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
        for field in ["files_fs","files_osd","blocks_fs","blocks_osd_on","blocks_osd_off"] :
            rawsql='SELECT SUM(EOSD.%s) FROM tbl_extvolattr AS E JOIN tbl_extvolattr_osd AS EOSD on E.vid = EOSD.vid WHERE E.projectIDs_js REGEXP "%s";' % (field,RegEx)
            self.Logger.debug("Executing %s" % rawsql)
            res = conn.execute(rawsql).fetchall()
            self.Logger.debug("got res=%s" % res)
            if len(res) == 1 :
                resDict[field] = res[0][0]
            else :
                resDict[field] = -1
        transa.commit()
        conn.close()  
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

    def getNewVolumeLocation(self, prjname, VolType) :
        """
        get a new volume location for this project.
        Has to be called separately for RW and external RO.
        For now, only choose on size, but we should also take the number of accessed Volumes 
        into account !?
        """
        thisProject = self.getProjectByName(prjname)
        if not thisProject : return None

        if VolType == "RW" :
            sps = thisProject.rw_serverparts 
        elif VolType == "RO" :
            sps = thisProject.ro_serverparts
        else :
            raise RuntimeError("Invalid Voltype : %s" % VolType)    

        # get Partinfos from livesystem

        PartInfos={}
        for serv_uuid, thisPart in sps :
            thisFsName = afs.LookupUtil[self._CFG.CELL_NAME].getHostnameByFSUUID(serv_uuid)
            if not thisFSName in PartInfos :
                for p in self._fsDAO.getPartList(thisFSName) :
                    PartInfos[thisFsName] = { p["name"] : p["free"]} 
        self.Logger.debug("ServerPartitions of Prj %s: %s" % (thisProject.name,sps)) 
        # find one with most Free size        
        # we need to iterate over sps again, since we might have more parttions
        # than belonging to this project
        maxFree = -1
        FsName = Part = None
        for serv_uuid, thisPart in sps :
            thisFsName = afs.LookupUtil[self._CFG.CELL_NAME].getHostnameByFSUUID(serv_uuid)
            if PartInfos[thisFsName][part] > maxFree : 
                maxFree = PartInfos[thisFsName][thisPart]
                FsName = thisFsName
                Part = thisPart
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
