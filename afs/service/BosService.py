from afs.service.BaseService import BaseService
from afs.service.BosServiceError import BosServiceError
from afs.model.BosServer import BosServer
from afs.model.BNode import BNode
import afs


class BosService (BaseService):
    """
    Provides Service about a Bosserver
    """
    
    def __init__(self, _cfg = None):
        BaseService.__init__(self, _cfg, LLAList=["BosServer" ])
        return

    def get_object(self, obj_or_param) :
        if isinstance(obj_or_param, BosServer) :
             this_BosServer = obj_or_param
        else : 
             DNSInfo=afs.LOOKUP_UTIL[self._CFG.cell].get_dns_info(obj_or_param)
             this_BosServer = BosServer()
             this_BosServer.servernames = DNSInfo["names"]

        return this_bosserver

    def pull_bos_server(self, obj_or_param, cached=True) :
        """
        Returning BosServer Object.
        As input parameter, give a BosServer Object or name_or_ip.
        This also pulls up any accompanying bnode objects
        """
        self.Logger.debug("Entering pull_bos_server")

        this_bosserver = self.get_object(obj_or_param)
        
        if self._CFG.DB_CACHE :
            if cached :
                cached_BosServer = self.DBManager.get_from_cache_by_list_element(BosServer, BosServer.servernames_js, this_BosServer.servernames[0], True)
                if cached_BosServer != None :
                    # XXX get BNodes
                    cached_BosServer.bnodes = []
                    self.Logger.debug("pull_bosserver: returning cached object")
                    return cached_BosServer
        this_BosServer = self._bosserver_lla.pull_bos_server(this_BosServer, _cfg=self._CFG)
        # update cache if present
        if self._CFG.DB_CACHE :
            cached_BosServer = self.DBManager.set_into_cache_by_list_element(BosServer, this_BosServer, BosServer.servernames_js, this_BosServer.servernames[0])
            for bn in this_BosServer.bnodes :
                bn.bos_db_id = cached_BosServer.db_id
                self.DBManager.set_into_cache(BNode, bn, bos_db_id=bn.bos_db_id, instance_name=bn.instance_name)
        return this_BosServer

    #
    # modifying methods
    #

    def startup(self, obj_or_param) :
        this_bosserver = self.get_object(obj_or_param)
        return 

    def shutdown(self, obj_or_param) :
        this_bosserver = self.get_object(obj_or_param)
        return 

    def set_general_restart_time(self, bos_server ) :
        this_bosserver = self.get_object(obj_or_param)
        return 

    def set_binary_restart_time(self, bos_server) :
        this_bosserver = self.get_object(obj_or_param)
        return 
