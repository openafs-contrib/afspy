from afs.model.Project import Project
from afs.service.BaseService import BaseService
from afs.exceptions.AfsError import AfsError
from afs.service.VolService import VolService

class ProjectService (BaseService):
    """
    Provides Service about Project management.
    This deals only with the DBCache.
    """
    
    def __init__(self, conf=None):
        BaseService.__init__(self, conf)
        if not self._CFG.DB_CACHE:
            raise AfsError('Error, Projects work only with a DBCache defined ',None)
        self.VS=VolService()
        return
        
    def getProjectByName(self, name) :
        """
        return ProjectObj from Projectname
        """
        thisProject=self.DBSession.query(Project).filter(Project.name == name).filrst()
        return thisProject
        
    def getProjectsByVolumeName(self):
        """
        return Project Obj from VolumeName
        """
        # check volume extra data if project ids are given
        # if yes, check if those are still valid.
        
        theseProjects=[]
        return theseProjects

    
    def getProjectVolumes(self):
        """
        return dict["fs-name"]["part-name"] = numVolumes
        """
        dict={}
        return dict
        
