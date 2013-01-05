import re,json,datetime

from afs.model.Project import Project
from afs.service.BaseService import BaseService
from afs.exceptions.AfsError import AfsError
from afs.service.VolService import VolService
from afs.model.ExtendedVolumeAttributes import ExtVolAttr

class ProjectService(BaseService):
    """
    Provides Service about Project management.
    This deals only with the DBCache.
    """
   
    def __init__(self, conf=None):
        BaseService.__init__(self, conf,DAOList=[])
        if not self._CFG.DB_CACHE:
            raise AfsError('Error, Projects work only with a DBCache defined ',None)
        self.ModelObj=Project()
        return
        
    def getProjectByName(self, name) :
        """
        return ProjectObj from Projectname
        """
        thisProject=self.DBManager.getFromCache(Project,name=name)
        return thisProject
        
    def getProjectsByVolumeName(self, volname):
        """
        return List of Projects Objs from VolumeName
        """
        list=[]
        for p in self.DBManager.getFromCache(Project,mustBeunique=False) :
            pDict=p.getDict()
            for rx in pDict["volnameRegEx"] :
                if re.compile(rx).match(volname) :
                     list.append(p)
        return list

    def getAssignedServers(self,prjname) :
        """
        return dict[VolType]["fs-name"]=[parts] 
        """
        thisProject=self.getProjectByName(prjname)
        if not thisProject : return None
        return dict
 
    def getServerSpread(self,prjname):
        """
        return dict["fs-name"]["part-name"] = [numRWVolumes,numROVolumes]
        """
        dict={}
        return dict

    def getVolumeIDs(self,prjname) :
        """
        return list of Volume IDs part of  this project
        """
        thisProject=self.getProjectByName(prjname)
        if not thisProject : return None
        list = self.DBManager.getFromCacheByListElement(ExtVolAttr,ExtVolAttr.projectIDs_js,thisProject.id)
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
            self.Logger.debug("got  res=%s" % res)
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
        projList=self.DBManager.getFromCache(Project,mustBeunique=False) 
        return projList

    def saveProject(self,prjObj):
        """
        store object into DBCache
        """
        cachedObj=self.DBManager.setIntoCache(Project,prjObj,name=prjObj.name)
        return cachedObj

    def createVolume(self,prjObj,name,blkquota=-1,osdpolicy=False) :
        """
        create a new volume for this project. 
        For now, only choose on size, but we should also take the number of accessed Volumes 
        into account !?
        """
        return True

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


