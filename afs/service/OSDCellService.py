import socket,sys

from afs.exceptions.AfsError import AfsError
from afs.model.Cell import Cell
from afs.model.ExtendedPartitionAttributes import ExtPartAttr
from afs.service.BaseService import BaseService
from afs.service.CellService import CellService
from afs.service.ProjectService import ProjectService
from afs.util import afsutil


class OSDCellService(CellService):
    """
    Provides Service about a Cell global information.
    The cellname is set in the configuration passed to constructor.
    Thus one instance works only for cell.
    """
    def __init__(self, conf=None):
        BaseService.__init__(self, conf, DAOList=["osdfs", "bnode","vl", "vol", "rx", "ubik", "dns"])
        if self._CFG.DB_CACHE :
            self.PS=ProjectService()
            self.projList=self.PS.getProjectList()


    ###############################################
    # Internal helper Section
    ###############################################    
   
    def _getFileServers(self):
        """
        Return FileServers as a list of uuid and hostname pair as dict for each fileserver
        """
        self.Logger.debug("refreshing FileServers from live system")
        FileServers =[]
        for na in self._vlDAO.getFsServList(self._CFG.CELL_NAME, self._CFG.Token,noresolve=True) :
            na['hostnames'],na['ipaddrs']=afsutil.getDNSInfo(na['name_or_ip'])
            na.pop('name_or_ip')
            for ip in na['ipaddrs'] :
                if ip in self._CFG.ignoreIPList :
                    self.Logger.debug("ignoring IP=%s" %ip)
                    continue
                else :
                    na['version']=self._rxDAO.getVersion(ip,7000)
                    na['partitions']=self._osdfsDAO.getPartList(na['ipaddrs'][0], self._CFG.CELL_NAME, self._CFG.Token)
                    for i in range(len(na['partitions'])) :
                        numRW=0
                        numRO=0
                        numBK=0
                        for v in self._osdfsDAO.getVolList(na['ipaddrs'][0],na['partitions'][i]['name'],self._CFG.CELL_NAME, self._CFG.Token) :
                            if v['type'] == "RW" :
                                numRW += 1
                            elif v['type'] == "RO" :
                                numRO += 1
                            elif v['type'] == "BK" :
                                numBK += 1
                            else :
                                 raise AfsError()
                        na['partitions'][i]['numRW'] = numRW
                        na['partitions'][i]['numRO'] = numRO
                        na['partitions'][i]['numBK'] = numBK
                        serv_uuid=afsutil.getFSUUIDByName_IP(ip,self._CFG)
                        # XXX we update the cell from the live system, but the extended attr we get from the DB_CACHE
                        na['partitions'][i]['projects'] = {}
                        if self._CFG.DB_CACHE :
                            ExtPart=self.DBManager.getFromCache(ExtPartAttr,mustBeunique=True,serv_uuid=serv_uuid,name=na['partitions'][i]['name'])
                            if ExtPart.projectIDs : 
                                for pid in ExtPart.projectIDs.keys() :
                                    for prj in self.projList :
                                        if int(prj.id) == int(pid) :
                                            na['partitions'][i]['projects'][prj.name] = ExtPart.projectIDs[pid]
                    FileServers.append(na)
        self.Logger.debug("returning %s" % FileServers)
        return FileServers
    
    def _getUbikDBInfo(self, Port):
        """
        return (SyncSite,DBVersion) pair for DataBase accessible from Port
        """
        DBServIP=self._getDBServers()[0]["ipaddrs"][0]
        DBVersion=self._ubikDAO.getDBVersion(DBServIP, Port)
        DBSyncSite=self._ubikDAO.getSyncSite(DBServIP, Port)
        return (DBSyncSite, DBVersion)
    
    ################################################
    # Statistcis DB BASE
    ################################################
    
    #TODO Number of users 
    
    #getTotalVolume()
    
    #Number of Volumes
    
    #Number of partitions
    
    #Total Space
    
    #Number of Servers
    
    #Volume offline
    
    #Volume OK
