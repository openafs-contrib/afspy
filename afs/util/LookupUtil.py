"""
DNS and AFS uuid Lookup
"""
import logging
import socket
import afs
from afs.util.misc import is_name
from afs.util.LookupUtilError import LookupUtilError

class LookupUtil :
    """
    Singleton class to make name lookups efficient 
    throughout the afspy-application.
    DNS and FSUUID-lookups provided.
    Caches lookups in memory, then uses DB-Cache and finally the
    live-system.
    """
  
    def __init__(self, conf = None) :

        # CONF INIT
        if conf:
            self._config = conf
        else: 
            self._config = afs.CONFIG

        # LOG INIT
        class_loglevel = getattr(afs.CONFIG,"LogLevel_%s" % \
            self.__class__.__name__, "").upper()
        numeric_loglevel = getattr(logging, class_loglevel, 0)
        self._logger = logging.getLogger(\
            "afs.util.%s" % self.__class__.__name__)
        self._logger.setLevel(numeric_loglevel)
        self._logger.debug("initializing %s-Object with conf=%s" % \
            (self.__class__.__name__, conf))      
        # fast class-local Lookup cache 
        self.memory_cache = {
            "dns_info" : {},
            "fsuuids" : {}
        }

        return   

    def get_dns_info(self, name_or_ip) :
        """ 
        get DNS-info about server
        returns dict{"names" : [], "ipaddrs" : []}
        """
        self._logger.debug("get_dns_info: entering with name_or_ip=%s" % \
            (name_or_ip))
        if not is_name(name_or_ip) : # check for matching ipaddress
            for hostname in afs.CONFIG.hosts :
                if name_or_ip in afs.CONFIG.hosts[hostname] :
                    self._logger.debug("%s is hard-mapped to (%s,%s)" % \
                        (name_or_ip, [hostname,],afs.CONFIG.hosts[hostname]))
                    self._logger.debug("returning %s" % ({ "names" : [hostname, ], \
                             "ipaddrs" : afs.CONFIG.hosts[hostname] }) )
                    return { "names" : [hostname, ], \
                             "ipaddrs" : afs.CONFIG.hosts[hostname] }

        # is a hostname
       
        # hard-mapped, primary Hostname given 
        if name_or_ip in afs.CONFIG.hosts.keys() :
            self._logger.debug("%s is hard-mapped to (%s,%s)" % ( name_or_ip, \
                [name_or_ip, ], afs.CONFIG.hosts[name_or_ip]))
            self._logger.debug("returning %s" % ({"names" : [name_or_ip,], "ipaddrs" : \
                afs.CONFIG.hosts[name_or_ip] }) )
            return {"names" : [name_or_ip,], "ipaddrs" : \
                afs.CONFIG.hosts[name_or_ip] }

       
        # memory_cache 
        if name_or_ip in self.memory_cache["dns_info"] :
            self._logger.debug("%s in localcache hard-mapped (%s)" % \
                (name_or_ip,self.memory_cache["dns_info"][name_or_ip] ))
            self._logger.debug("returning %s" % (self.memory_cache["dns_info"][name_or_ip]))
            return self.memory_cache["dns_info"][name_or_ip]
        
        for srv in self.memory_cache["dns_info"] :
            if name_or_ip in self.memory_cache["dns_info"][srv]["names"] :
                self._logger.debug("%s is hard-mapped to %s" % (name_or_ip, \
                    self.memory_cache["dns_info"][srv] ))
                self._logger.debug("returning %s" % (self.memory_cache["dns_info"][srv]) )
                return self.memory_cache["dns_info"][srv]

        # lookup from OS
  
        try : 
            dns_info = socket.gethostbyaddr(name_or_ip)
            servernames = [dns_info[0]] + dns_info[1]
            ipaddrs = dns_info[2]
        except socket.gaierror :
            if is_name(name_or_ip) :
                raise LookupUtilError("Cannot resolve %s" % name_or_ip)
            else :
                self._logger.warn("Cannot resolve %s" % name_or_ip)
                self._logger.debug("returning %s" % ({"names": [], "ipaddrs" : [name_or_ip,]}) )
                return {"names": [], "ipaddrs" : [name_or_ip,]}


        self._logger.debug("%s resolves to %s" % (name_or_ip, dns_info)) 
        # check if resolved ip-address matches (if hostalias was used)
        for hostname in afs.CONFIG.hosts :
            for ipaddr in ipaddrs :
                if ipaddr in afs.CONFIG.hosts[hostname] :
                    self._logger.debug("%s is hard-mapped to (%s,%s)" % \
                        (ipaddrs, [hostname,],afs.CONFIG.hosts[hostname]))
                    # add this hostalias to list in memory_cache
                    if self.memory_cache["dns_info"].has_key(hostname) :
                        self.memory_cache["dns_info"][hostname]["names"] = \
                            [hostname, ]
                        self.memory_cache["dns_info"][hostname]["ipaddrs"] = \
                            afs.CONFIG.hosts[hostname]
                    else :
                        self.memory_cache["dns_info"][hostname] = { \
                            "names" : [hostname,], \
                            "ipaddrs" : afs.CONFIG.hosts[hostname]}
                    self._logger.debug("memory_cache = %s" % \
                        (self.memory_cache))
                    ipaddrs = []
                    self._logger.debug("returning %s" % ({ "names" : [hostname], "ipaddrs" : \
                        afs.CONFIG.hosts[hostname] }) )
                    return { "names" : [hostname], "ipaddrs" : \
                        afs.CONFIG.hosts[hostname] }

        if "nxdomain" in servernames[0] : 
            raise LookupUtilError("cannot resolve DNS-entry %s" % name_or_ip)
        # fill up localcache
        self.memory_cache["dns_info"][servernames[0]] = { \
            "names" : servernames, "ipaddrs" : ipaddrs }
        self._logger.debug("memory_cache = %s" % (self.memory_cache))
        self._logger.debug("returning %s" % ({"names": servernames, "ipaddrs" : ipaddrs}) )
        return {"names": servernames, "ipaddrs" : ipaddrs}

    #
    # FSUUID - translations
    #
    # In AFS all fileservers have a uuid. This is used in the database
    # to identify a fileserver
    # 

    def get_fsuuid(self, name_or_ip, _user = "", cached = True) :
        """
        returns UUID of a fileserver, which is used as key for server-entries
        in other tables. This does not silently update the Cache
        """
        self._logger.debug("get_fsuuid: called with %s" % name_or_ip)
        if cached :
        # local Cache first
            if name_or_ip in self.memory_cache["fsuuids"].keys() :
                return self.memory_cache["fsuuids"][name_or_ip]
            else :
                name_or_ip = self.get_dns_info(name_or_ip)["names"][0] 
                if name_or_ip in self.memory_cache["fsuuids"].keys() :
                    return self.memory_cache["fsuuids"][name_or_ip]
        # then DB
            if  self._config.DB_CACHE:
                from afs.util.DBManager import DBManager
                from afs.model.FileServer import FileServer
                self._logger.debug("looking up FSUUID in DB_Cache for serv=%s" \
                     % name_or_ip)
                dns_info = self.get_dns_info(name_or_ip)
                this_dbmanager = DBManager(self._config)
                fileserver = this_dbmanager.get_from_cache_by_list_element(\
                    FileServer, FileServer.servernames_js, \
                    dns_info["names"][0])
                if fileserver != None :
                    # store it in memory_cache 
                    self.memory_cache["fsuuids"][fileserver.servernames[0]] = \
                        fileserver.uuid 
                    self.memory_cache["fsuuids"][fileserver.ipaddrs[0]] = \
                        fileserver.uuid
                    return fileserver.uuid

        # not found in local cache and not in DB Cache, get it from live-system
            
        from afs.lla.VLDBLLA import VLDBLLA
        dns_info = self.get_dns_info(name_or_ip)
        uuid = ""
        _vl_lla = VLDBLLA()

        uuid = _vl_lla.get_fileserver_uuid(dns_info["names"][0], _user = _user, \
             _cfg = self._config)

        # store it in memory_cache 
        self.memory_cache["fsuuids"][name_or_ip] = uuid                  
        self.memory_cache["fsuuids"][dns_info["names"][0]] = uuid
        self._logger.debug("returning %s" % (uuid))
        return uuid
    
    def get_hostname_by_fsuuid(self, uuid, _user = "", cached = True) :
        """
        returns hostname of a fileserver by uuid
        """
        self._logger.debug("called with %s, cached=%s" % (uuid, cached))
        if cached :
            # local Cache first
            for hostname in self.memory_cache["fsuuids"] :
                if not is_name(hostname) : 
                    continue
                if self.memory_cache["fsuuids"][hostname] == uuid :
                    self._logger.debug("returning from local cache: %s" % \
                        hostname)
                    return hostname
            # then DB 
            if self._config.DB_CACHE:
                from afs.util.DBManager import DBManager
                from afs.model.FileServer import FileServer
                this_dbmanager = DBManager(self._config)
                fileserver = this_dbmanager.get_from_cache(FileServer, \
                    uuid = uuid)
                self._logger.debug("looking up hostname in db_cache " + \
                   "for uuid=%s" % uuid)
                if fileserver != None :
                    self.memory_cache["fsuuids"][fileserver.servernames[0]] = \
                        fileserver.uuid
                    return fileserver.servernames[0]

        # not found in local cache and not in DB Cache, or cacheing disabled.
        # get it from live-system
        from afs.lla.VLDBLLA import VLDBLLA
        _vl_lla = VLDBLLA()
        name_or_ip = None
        for fileserver in _vl_lla.getFsServList(\
            _cfg = self._config, _user="" ) :
            if fileserver['uuid'] == uuid :
                name_or_ip = fileserver['name_or_ip']
        if name_or_ip == None :
            raise LookupUtilError("No Server with uuid=%s " + \
                "registered in live-system" % uuid)
        # store it in memory_cache 
        self._logger.debug("get_hostname_by_fsuuid: got " + \
            " name_or_ip = %s from live-system" % name_or_ip)
        name_or_ip = self.get_dns_info(name_or_ip)["names"][0]
        self.memory_cache["fsuuids"][name_or_ip] = uuid                  
        self._logger.debug("returning: %s" % name_or_ip)
        return name_or_ip
