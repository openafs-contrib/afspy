from afs.service.BaseService import BaseService
from afs.model.DBServer import DBServer
from afs.util import afsutil
from afs.exceptions.AfsError import AfsError


class DBsService(BaseService) :

    """
    Provides Service about a DBServer
    the info about the blessed DB they are providing are in the CellService!
    """
    
    _CFG    = None
    
    def __init__(self,conf=None):
        BaseService.__init__(self, conf, DAOList=["vl","ubik","rx"])

    def getDBServer(self, name_or_ip, DBType,_user="",cached=False) :
        """
        Return DB-Server object
        """ 

        self.Logger.debug("Entering getDBServer with name_or_ip=%s, DBType=%s" % (name_or_ip,DBType) )

        if not DBType in ["vldb","ptdb" ] : raise AfsError ("invalid DBType DB-Type %s. Valid DBTypes are vldb and ptdb." % DBType)

        servernames, ipaddrs=afsutil.getDNSInfo(name_or_ip)
        mandIP=""
        if len(ipaddrs) != 0 :
            for ip in ipaddrs :
                if not ip in self._CFG.ignoreIPList :
                    if mandIP != "" : AfsError ("DB-Servers may only be registered with one IP here for the time being. Please add all non.used IPs to the ignoreList.")
                mandIP=ip
        else :
            mandIP=ip
    
        if cached :
            this_DBServer=self.DBManager.getFromCache(DBServer,ipaddr=mandIP)
            return this_DBServer

        if DBType == "vldb" :
            port=7003
        elif DBType == "ptdb": 
            port=7002
        else :
            raise AfsError("Invalid DBType %s" % DBType)

        this_DBServer = DBServer()
        this_DBServer.type = DBType
        this_DBServer.servernames=servernames
        this_DBServer.ipaddr=mandIP
        shortInfo=self._ubikDAO.getShortInfo(mandIP,port,self._CFG.CELL_NAME, _cfg=self._CFG, _user=_user)
        this_DBServer.isClone=shortInfo["isClone"]
        this_DBServer.localDBVersion =  shortInfo["localDBVersion"]
        this_DBServer.version,this_DBServer.builddate=self._rxDAO.getVersionandBuildDate(mandIP,port)

        if self._CFG.DB_CACHE :
            self.DBManager.setIntoCache(DBServer,this_DBServer,ipaddr=this_DBServer.ipaddr,type=DBType)
 
        return this_DBServer

