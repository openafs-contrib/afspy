from afs.service.BaseService import BaseService
from afs.exceptions.AfsError import AfsError
from afs.model.BosServer import BosServer
from afs.util import afsutil


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
        servernames, ipaddrs=afsutil.getDNSInfo(name_or_ip)
        if cached :
            this_BosServer=self.DBManager.getFromCache(BosServer,servernames[0])
            # XXX get BNodes
            self.BNodes=[]
            return this_BosServer
        this_BosServer = BosServer()
        RTs=self.getRestartTimes()
        # get BNodes
        if self._CFG.DB_CACHE :
            self.DBManager.setIntoCache(BosServer, this_BosServer, ipaddr=ipaddrs[0])
        return this_BosServer

    def getRestartTimes(self, name_or_ip, _user="", cached=False):
        """
        return Dict about the restart times of the afs-server
        """
        TimesDict=self._bnodeDAO.getRestartTimes(name_or_ip, self._CFG.CELL_NAME, _cfg=self._CFG, _user=_user)
        return TimesDict
            
    def setRestartTimes(self, this_BosServer, time, restarttype, _user="" ):
        """
        Ask Bosserver about the restart times of the fileserver
        """
        servernames, ipaddrs=afsutil.getDNSInfo(this_BosServer)
        self._bnodeDAO.setRestartTimes(this_BosServer.ipaddrs[0], time, restarttype, self._CFG.CELL_NAME, _cfg=self._CFG, _user=_user)
        if self._CFG.DB_CACHE : 
            self.DBManager.setIntoCache(BosServer, this_BosServer, ipaddr=ipaddrs[0])
        return
