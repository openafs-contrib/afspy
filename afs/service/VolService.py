from afs.model.Volume import Volume
from afs.model.VolumeGroup import VolumeGroup
from afs.service.BaseService import BaseService
from afs.service.CellService import CellService
from afs.service.FsService import FsService
from afs.exceptions.VolError import VolError
from afs.exceptions.AfsError import AfsError
from afs.util import afsutil


class VolService (BaseService):
    """
    Provides Service about a Volume management.
    The cellname is set in the methods so that we 
    can use this for more than one cell.
    """
    
    def __init__(self, conf=None):
        BaseService.__init__(self, conf, DAOList=["vol"])
        self.CS=CellService()
        self.FsS=FsService()
       
    ###############################################
    # Volume Section
    ###############################################    
    
    """
    Retrieve Volume Group
    """
    def getVolGroup(self, id , cached=False):
    
        list = self._volDAO.getVolGroupList(id,  self._CFG.CELL_NAME, self._CFG.Token)
        volGroup = None
        if len(list) > 0:
            volGroup =  VolumeGroup()
            for el in list:
                volGroup.name = el['volname']
                if el['type'] == 'RW':
                    volGroup.RW.append(el)
                elif el['type'] == 'RO':
                    volGroup.RO.append(el)
                else :
                    volGroup.BK.append(el)
        return volGroup
       
    """
    Retrieve Volume Information by Name or ID
    """
    def getVolume(self, name, serv, part,  cached=False):
        if cached :
            serv_uuid=self.FsS.getUUID(serv)
            vol=self._getFromCache(name, serv_uuid, part)
            return vol
        vdict = self._volDAO.getVolume(name, serv, part,  self._CFG.CELL_NAME, self._CFG.Token)
        vdict["serv_uuid"]=self.FsS.getUUID(serv)
        vol = None
        if vdict:
            vol = Volume()
            vol.setByDict(vdict)
            if self._CFG.DB_CACHE :
                self._setIntoCache(vol)
        return  vol
    
    """
    Retrieve Volume extended information
    """
    def getVolExtended(self,id, cached=False):
        pass
 
    def release(self, id):
        #Check before the call (must be RW)
        pass
 
    ################################################
    #  Cache Query 
    ################################################
    def getVolCountByQuery(self,query):
         if not self._CFG.DB_CACHE:
            raise VolError('Error, no db Cache defined ',None)
        
         query._tbl= "Volume"
         queryc = query.getQueryCount()
         count  = eval(queryc)         
         
         return count
 
    def getVolByQuery(self,query):
         if not self._CFG.DB_CACHE:
            raise VolError('Error, no db Cache defined ',None)
        
         query._tbl= "Volume"
         query  = query.getQuery()
         res    = eval(query)
         
         return res
     
    def execQuery(self):
        pass
    
    def execOrmQuery(self):
        pass
 
    def refreshCache(self, serv, part):
        if not self._CFG.DB_CACHE:
            raise VolError('Error, no db Cache defined ',None)
       
        part = afsutil.canonicalizePartition(part)
        list = self._volDAO.getVolList( serv, part, self._CFG.CELL_NAME, self._CFG.Token)
        #Convert into dictionary
        idVolDict = {}
        cUpdate = len(list)
        for el in list:
            idVolDict[el['vid']] = el
            
        
        res  = self.DbSession.query(Volume).filter(self.or_(Volume.serv == serv,Volume.servername == serv )).filter(Volume.part == part)
        
        flush = 0
        for vol in res:
            flush +=1
            if idVolDict.has_key(vol.vid):
                vol.setByDict(idVolDict[vol.vid])
                del idVolDict[vol.vid]
            else:     
                self.DbSession.delete(vol) 
            
            if flush > self._CFG.DB_FLUSH:    
                self.DbSession.flush() 
        
        # ADD section 
        flush = 0
        for key in idVolDict.keys():
            flush +=1
            vol = Volume()
            vol.setByDict(idVolDict[key])
            self.DbSession.add(vol)    
            if flush > self._CFG.DB_FLUSH:    
                self.DbSession.flush() 
        self.DbSession.commit()
        
        return cUpdate
    
    ################################################
    #  Internal Cache Management 
    ################################################


    def _getFromCache(self,id, serv_uuid, part):
        #STORE info into  CACHE
        if not self._CFG.DB_CACHE:
            raise AfsError("DB_CACHE not configured")
        # Do update
        vol = self.DbSession.query(Volume).filter(self.or_(Volume.vid == id, Volume.name == id)).filter(Volume.serv_uuid == serv_uuid).filter(Volume.part == part).first()
        return vol
        
    def _setIntoCache(self,vol):
         #STORE info into  CACHE
       
        if not self._CFG.DB_CACHE:
            raise AfsError("DB_CACHE not configured")
        
        volCache = self.DbSession.query(Volume).filter(Volume.vid == vol.vid).filter(self.or_(Volume.serv_uuid == vol.serv_uuid,Volume.servername == vol.servername )).filter(Volume.part == vol.part).first()
        
        if volCache:
            volCache.copyObj(vol)
            self.DbSession.flush()
        else:
            volCache=self.DbSession.merge(vol)  
            self.DbSession.flush()
        
        self.DbSession.commit()  
        return volCache
    
    def _delCache(self,vol):
         #STORE info into  CACHE
        if not self._CFG.DB_CACHE:
            return None
        # Do update
        self.DbSession.delete(vol)
            
        self.DbSession.commit()
        
    
    #MERGE ?  
    
      
    
