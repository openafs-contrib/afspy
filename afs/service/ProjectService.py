import re

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
        thisProject=self.DBCService.getFromCache(Project,name=name)
        return thisProject
        
    def getProjectsByVolumeName(self, volname):
        """
        return List of Projects Objs from VolumeName
        """
        list=[]
        for p in self.DBCService.getFromCache(Project,mustBeunique=False) :
            pDict=p.getDict()
            for rx in pDict["volnameRegEx"] :
                if re.compile(rx).match(volname) :
                     list.append(p)
        return list

    def getAssignedServers(self,prjname) :
        """
        return dict[VolType]["fs-name"]=[parts] 
        """
        return dict
 
    def getProjectSpread(self,prjname):
        """
        return dict["fs-name"]["part-name"] = [numRWVolumes,numROVolumes]
        """
        dict={}
        return dict

    def getProjectVolumes(self,prjname) :
        thisProject=self.getProjectByName(prjname)
        if not thisProject : return []
        list = self.DBCService.getFromCacheByListElement(ExtVolAttr,ExtVolAttr.projectIDs_js,thisProject.id)
        return list
        
    def getProjectList(self) :
        """
        return list of ProjectDicts
        """
        projList=self.DBCService.getFromCache(Project,mustBeunique=False) 
        return projList

    def saveProject(self,prjObj):
        """
        store object into DBCache
        """
        cachedObj=self.DBCService.setIntoCache(Project,prjObj,name=prjObj.name)
        return cachedObj


    def createVolume(self,prjObj,name,blkquota=-1,osdpolicy=False) :
        """
        create a new volume for this project. 
        For now, only choose on size, but we should also take the number of accessed Volumes 
        into account !?
        """
        return True
