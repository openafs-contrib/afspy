from afs.service.BaseService import BaseService
from afs.model.DBServer import DBServer
from afs.service.DBsServiceError import DBsServiceError
import afs


class DBsService(BaseService) :

    """
    Provides Service about a DBServer
    the info about the blessed DB they are providing are in the CellService!
    """
    
    _CFG    = None
    
    def __init__(self,conf=None):
        BaseService.__init__(self, conf, LLAList=["vl","ubik","rx"])

    def get_db_server(self, name_or_ip, DBType, _user="", cached=False) :
        """
        Return DB-Server object
        """ 

        self.Logger.debug("Entering get_db_server with name_or_ip=%s, DBType=%s" % (name_or_ip, DBType) )

        if not DBType in ["vldb","ptdb" ] : raise DBsServiceError ("invalid DBType DB-Type %s. Valid DBTypes are vldb and ptdb." % DBType)

        dns_info = afs.LOOKUP_UTIL[self._CFG.cell].get_dns_info(name_or_ip)

        true_ip = ""
        if len(dns_info["ipaddrs"]) != 0 :
            for ip in dns_info["ipaddrs"] :
                if not ip in self._CFG.ignore_ip_list :
                    if true_ip != "" : DBsServiceError ("DB-Servers may only be registered with one IP here for the time being. Please add all non.used IPs to the ignoreList.")
                true_ip = ip
        else :
            mandIP = ip
    
        if cached :
            this_db_server = self.DBManager.get_from_cache(DBServer, ipaddr=true_ip)
            return this_db_server 

        this_db_server = DBServer()
        this_db_server.type = DBType
        this_db_server.servernames=dns_info["names"]
        this_db_server.ipaddr=true_ip
        shortInfo = self._ubikLLA.getShortInfo(true_ip,port, _cfg=self._CFG, _user=_user)
        this_db_server.isClone=shortInfo["isClone"]
        this_db_server.localDBVersion =  shortInfo["localDBVersion"]
        this_db_server.version,this_db_server.build_date = self._rxLLA.getVersionandBuildDate(true_ip, port, _user=_user, _cfg=self._CFG)

        if self._CFG.DB_CACHE :
            self.DBManager.setIntoCache(DBServer,this_db_server,ipaddr = this_db_server.ipaddr,type=DBType)
 
        return this_db_server

