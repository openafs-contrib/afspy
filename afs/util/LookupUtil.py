import logging,socket
import afs
from afs.util.afsutil import isName
from afs.exceptions.LookupUtilError import LookupUtilError

class LookupUtil :
    """
    Singleton class to make name lookups efficient 
    throughout the afspy-application.
    DNS and FSUUID-lookups provided.
    Caches lookups in memory, then uses DB-Cache and finally the
    live-system.
    """
  
    def __init__(self,conf=None) :

        # CONF INIT
        if conf:
            self._CFG = conf
        else: 
            self._CFG = afs.defaultConfig

        # LOG INIT
        classLogLevel = getattr(afs.defaultConfig,"LogLevel_%s" % self.__class__.__name__, "").upper()
        numericLogLevel = getattr(logging,classLogLevel, 0)
        self.Logger=logging.getLogger("afs.util.%s" % self.__class__.__name__)
        self.Logger.setLevel(numericLogLevel)
        self.Logger.debug("initializing %s-Object with conf=%s" % (self.__class__.__name__, conf))      
        
        self.localCache = {
            "DNSInfo" : {},
            "FSUUIDs" : {}
        }

        return   

    def getDNSInfo(self,name_or_ip):
        """ 
        get DNS-info about server
        returns dict{"names" : [], "ipaddrs" : []}
        """
        self.Logger.debug("getDNSInfo: entering with name_or_ip=%s" % (name_or_ip))
        if not isName : # check for matching ipaddress
            for hn in afs.defaultConfig.hosts :
                if name_or_ip in afs.defaultConfig.hosts[hn] :
                    self.Logger.debug("%s is hard-mapped to (%s,%s)" % (name_or_ip, [hn,],afs.defaultConfig.hosts[hn]))
                    return { "names" : [hn,], "ipaddrs" :afs.defaultConfig.hosts[hn] }             
        # is a hostname
       
        # hard-mapped, primary Hostname given 
        if name_or_ip in afs.defaultConfig.hosts.keys() :
            self.Logger.debug("%s is hard-mapped to (%s,%s)" % (name_or_ip, [name_or_ip,], afs.defaultConfig.hosts[name_or_ip]))
            return {"names" : [name_or_ip,], "ipaddrs" : afs.defaultConfig.hosts[name_or_ip] }

       
        # localCache 
       
        if name_or_ip in self.localCache["DNSInfo"] :
            self.Logger.debug("%s is in localcache. returning hard-mapped to (%s)" % (name_or_ip,self.localCache["DNSInfo"][name_or_ip] ))
            return self.localCache["DNSInfo"][name_or_ip]
        
        for srv in self.localCache["DNSInfo"] :
            if name_or_ip in self.localCache["DNSInfo"][srv]["names"] :
                self.Logger.debug("%s is hard-mapped to %s" % (name_or_ip, self.localCache["DNSInfo"][srv] ))
                return self.localCache["DNSInfo"][srv]

        # lookup from OS
  
        try : 
            DNSInfo=socket.gethostbyaddr(name_or_ip)
            servernames=[DNSInfo[0]]+DNSInfo[1]
            ipaddrs=DNSInfo[2]
        except :
            raise LookupUtilError("Cannot resolve %s" % name_or_ip)

        self.Logger.debug("%s resolves to %s" % (name_or_ip,DNSInfo)) 
        # check if resolved ip-address matches (if hostalias was used)
        for hn in afs.defaultConfig.hosts :
            for ip in ipaddrs :
                if ip in afs.defaultConfig.hosts[hn] :
                    self.Logger.debug("%s is hard-mapped to (%s,%s)" % (ipaddrs, [hn,],afs.defaultConfig.hosts[hn]))
                    # add this hostalias to list in localCache
                    if self.localCache["DNSInfo"].has_key(hn) :
                        self.localCache["DNSInfo"][hn]["names"]=[hn,]
                        self.localCache["DNSInfo"][hn]["ipaddrs"]=afs.defaultConfig.hosts[hn]
                    else :
                        self.localCache["DNSInfo"][hn]={ "names" :[hn,], "ipaddrs" : afs.defaultConfig.hosts[hn]}
                    self.Logger.debug("localCache = %s" % (self.localCache))
                    ipaddrs=[]
                    return { "names" : [hn,], "ipaddrs" :afs.defaultConfig.hosts[hn] }             

        if "nxdomain" in servernames[0] : 
            raise LookupUtilError("cannot resolve DNS-entry %s" % name_or_ip)
        # fill up localcache
        self.localCache["DNSInfo"][servernames[0]]={"names" : servernames, "ipaddrs" : ipaddrs}
        self.Logger.debug("localCache = %s" % (self.localCache))
        return {"names": servernames, "ipaddrs" : ipaddrs}

    #
    # FSUUID - translations
    #
    # In AFS all fileservers have a uuid. This is used in the database
    # to identify a fileserver
    # 

    def getFSUUID(self,name_or_ip,_user="",cached=True):
        """
        returns UUID of a fileserver, which is used as key for server-entries
        in other tables. This does not silently update the Cache
        """
        if cached :
        # local Cache first
            if name_or_ip in self.localCache["FSUUIDs"].keys() :
                return self.localCache["FSUUIDs"][name_or_ip]
            else :
                name_or_ip =self.getDNSInfo(name_or_ip)["names"][0] 
                if name_or_ip in self.localCache["FSUUIDs"].keys() :
                    return self.localCache["FSUUIDs"][name_or_ip]
        # then DB
            if  self._CFG.DB_CACHE:
                from DBManager import DBManager
                from afs.model.FileServer import FileServer
                self.Logger.debug("looking up FSUUID in DB_Cache for serv=%s" % name_or_ip)
                DNSInfo=self.getDNSInfo(name_or_ip)
                thisDBManager=DBManager(self._CFG)
                list=thisDBManager.getFromCacheByListElement(FileServer,FileServer.servernames_js,DNSInfo["names"][0])         
                if list != None :
                    if len(list) > 1 :
                        raise LookupUtilError("DB_Cache error. Got more than one entry for server %s" % name_or_ip) 
                    if len(list) == 1  :
                        # store it in localCache 
                        self.localCache["FSUUIDs"][name_or_ip] = list[0].uuid                  
                        return list[0].uuid

        # not found in local cache and not in DB Cache, get it from live-system
            
        from afs.dao.VLDbDAO import VLDbDAO
        self.Logger.debug("getFSUUID: called with %s" % name_or_ip)
        DNSInfo=self.getDNSInfo(name_or_ip)
        uuid=""
        _vlDAO=VLDbDAO()
        uuid=_vlDAO.getFsUUID(DNSInfo["names"][0],_user=_user,_cfg=self._CFG)
        # store it in localCache 
        self.localCache["FSUUIDs"][name_or_ip] = uuid                  
        return uuid
    
    def getHostnameByFSUUID(self,uuid,_user="",cached=True) :
        """
        returns hostname of a fileserver by uuid
        """
        if cached :
            # local Cache first
            for hn in self.localCache["FSUUIDs"] :
                if self.localCache["FSUUIDs"][hn] == uuid :
                    return hn
            # then DB 
            if self._CFG.DB_CACHE:
                from DBManager import DBManager
                from afs.model.FileServer import FileServer
                thisDBManager=DBManager(self._CFG)
                list=thisDBManager.getFromCacheByListElement(FileServer,FileServer.uuid,uuid)
                self.Logger.debug("looking up hostname in DB_Cache for uuid=%s" % uuid)
                if list != None :
                    if len(list) > 1 :
                        raise LookupUtilError("DB_Cache error. Got more than one entry for fs-uuid %s" % uuid)
                    if len(list) == 1 :
                        self.localCache["FSUUIDs"][list[0].servernames[0]] = list[0].uuid                  
                        return list[0].servernames[0]

        # not found in local cache and not in DB Cache, or cacheing disabled.
        # get it from live-system
        from afs.dao.VLDbDAO import VLDbDAO
        self.Logger.debug("called with %s" % uuid)
        _vlDAO=VLDbDAO()
        name_or_ip=""
        for fs in _vlDAO.getFsServList(_cfg=self._CFG,_user="" ) :
            if fs['uuid'] == uuid :
               name_or_ip = fs['name_or_ip']
        # store it in localCache 
        self.Logger.debug("getHostnameByFSUUID: got name_or_ip =%s from live-system" % name_or_ip)
        name_or_ip=self.getDNSInfo(name_or_ip)["names"][0]
        self.localCache["FSUUIDs"][name_or_ip] = uuid                  
        self.Logger.debug("returning: %s" % name_or_ip)
        return name_or_ip
