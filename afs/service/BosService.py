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
        BaseService.__init__(self, _cfg, LLAList=["bos" ])
        return

    def get_object(self, obj_or_param) :
        if isinstance(obj_or_param, BosServer) :
             this_bos_server = obj_or_param
        else : 
             DNSInfo=afs.LOOKUP_UTIL[self._CFG.cell].get_dns_info(obj_or_param)
             this_bos_server = BosServer()
             this_bos_server.servernames = DNSInfo["names"]

        return this_bos_server

    def get_bos_server(self, obj_or_param, cached=True) :
        """
        Returning BosServer Object.
        As input parameter, give a BosServer Object or name_or_ip.
        This also get up any accompanying bnode objects
        """
        self.Logger.debug("Entering get_bos_server")

        this_bos_server = self.get_object(obj_or_param)
        
        if self._CFG.DB_CACHE :
            if cached :
                cached_BosServer = self.DBManager.get_from_cache_by_list_element(BosServer, BosServer.servernames_js, this_bos_server.servernames[0], True)
                if cached_BosServer != None :
                    cached_BosServer.bnodes = self.DBManager.get_from_cache(BNode, must_be_unique=False, bos_db_id=cached_BosServer.db_id)
                    self.Logger.debug("get_bosserver: returning cached object")
                    return cached_BosServer

        # get from live_system
        this_bos_server = self._bosLLA.get_bos_server(this_bos_server.servernames[0], _cfg=self._CFG)

        # update cache if present
        if self._CFG.DB_CACHE :
            cached_BosServer = self.DBManager.set_into_cache_by_list_element(BosServer, this_bos_server, BosServer.servernames_js, this_bos_server.servernames[0])
            # get Bnodes as well
            for bn in this_bos_server.bnodes :
                bn.bos_db_id = cached_BosServer.db_id
                self.DBManager.set_into_cache(BNode, bn, bos_db_id=bn.bos_db_id, instance_name=bn.instance_name)
        return this_bos_server

    #
    # modifying methods
    #

    def set_restart_times(self, bosserver) :
        self._bosLLA.set_restart_time(bosserver.servernames[0], "general", bosserver.restart_times["general"])
        self._bosLLA.set_restart_time(bosserver.servernames[0], "newbinary", bosserver.restart_times["newbinary"])
        return

    def set_superusers(self, bosserver, remove=False) :
        """
        add / remove users to match the superusers in the object  
        """
        current_superusers = self._bosLLA.get_superuserlist(bosserver.servernames[0])
        self.Logger.debug("set_superusers: current_superuser_list=%s" % current_superusers)
        to_be_removed = []
        for user in current_superusers :
            if not user in bosserver.superusers :
                to_be_removed.append(user) 
        if len(to_be_removed) > 0  and remove :
            self.Logger.warn("set_superusers: to_be_removed=%s" % to_be_removed)
            bosserver = self._bosLLA.remove_superuser(bosserver.servernames[0], to_be_removed)

        to_be_added = []
        for user in bosserver.superusers :
            if not user in current_superusers :
                to_be_added.append(user) 
        if len(to_be_added) > 0:
            self.Logger.warn("set_superusers: to_be_added=%s" % to_be_added)
            bosserver = self._bosLLA.add_superuser(bosserver.servernames[0], to_be_added)
        return bosserver

    #
    # interrupting methods
    #

    def startup(self, bosserver) :
        self._bosLLA.startup(bosserver.servernames[0])
        return self.get_bos_server(bosserver, cached=False)

    def shutdown(self, bosserver) :
        self._bosLLA.shutdown(bosserver.servernames[0])
        return self.get_bos_server(bosserver, cached=False)
