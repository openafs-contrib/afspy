from afs.service.BaseService import BaseService
from afs.exceptions.AfsError import AfsError
from afs.model.BosServer import BosServer
from afs.util import afsutil
import afs


class BsService (BaseService):
    """
    Provides Service about a Bosserver
    """
    
    _CFG    = None
    
    def __init__(self, conf=None):
        BaseService.__init__(self, conf, DAOList=["bnode" ])
        return

    def getBosServer(self, name_or_ip, cached=False) :
        self.Logger.debug("Entering getBosServer")
        DNSInfo=afs.LookupUtil[self._CFG.CELL_NAME].getDNSInfo(name_or_ip)
        if cached :
            this_BosServer=self.DBManager.getFromCache(BosServer,DNSInfo["names"][0])
            # XXX get BNodes
            self.BNodes=[]
            return this_BosServer
        this_BosServer = BosServer()
        RTs=self.getRestartTimes(DNSInfo["names"][0])
        # get BNodes
        if self._CFG.DB_CACHE :
            self.DBManager.setIntoCache(BosServer, this_BosServer, ipaddr=DNSInfo["ipaddrs"][0])
        return this_BosServer

    def getRestartTimes(self, name_or_ip, _user="", cached=False):
        """
        return Dict about the restart times of the afs-server
        """
        TimesDict=self._bnodeDAO.getRestartTimes(name_or_ip, _cfg=self._CFG, _user=_user)
        return TimesDict
            
    def setRestartTimes(self, name_or_ip, time, restarttype, _user="" ):
        """
        Ask Bosserver about the restart times of the fileserver
        """
        DNSInfo=afs.LookupUtil[self._CFG.CELL_NAME].getDNSInfo(name_or_ip)
        self._bnodeDAO.setRestartTimes(name_or_ip, time, restarttype, _cfg=self._CFG, _user=_user)
        if self._CFG.DB_CACHE : 
            self.DBManager.setIntoCache(BosServer, DNSInfo["names"][0], ipaddr=DNSInfo["ipaddrs"][0])
        return
