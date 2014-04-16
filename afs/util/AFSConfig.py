"""
module for parsing the configuration from different sources:
- global system config
- user local config
- commandline
the latter overrides the earlier configs in the oerder given above.
"""
import logging
import os 
import types

import afs
from afs.util.AFSError import AFSError
import afs.util.LookupUtil
import afs.orm.DBMapper

def parse_configs(my_parser=None):
    """
    setup all available options
    """
    home_dir = os.environ.get("HOME","")
    ## module-wide Configuration file
    base_config_dir = "%s/etc/" % os.path.dirname(afs.__file__)
    if not my_parser :
        my_parser = afs.ARGPARSER
    
    # mix commandline parsing with giving options in files :
    # 
    # parse most specific first, default is empty string for all.
    # latter ones do not overwrite earlier ones.
    # if config file is given on command line, do not parse 
    # the one in the home-directory or the system-wide one.
    # add hard-coded defaults to options still being
    # an empty-string
    
    afs.CONFIG = my_parser.parse_args()
    if afs.CONFIG.config  :
        afs.CONFIG = load_config_from_file(afs.CONFIG, \
            afs.CONFIG.config)
    if os.path.exists("./afspy.cfg") :
        afs.CONFIG = load_config_from_file(afs.CONFIG, \
            "./afspy.cfg")
    elif os.path.exists("%s/.config/afspy.cfg" % home_dir) :
        afs.CONFIG = load_config_from_file(afs.CONFIG, \
            "%s/.config/afspy.cfg" % home_dir)
    elif os.path.exists(base_config_dir + "afspy.cfg") :
        afs.CONFIG = load_config_from_file(afs.CONFIG, 
            base_config_dir + "afspy.cfg")

    # parse hosts and ignore_IP
    afs.CONFIG.hosts = {}
    for host_entry in afs.CONFIG.hostmap :
        hostname, ips = host_entry.split("=")
        ips = ips.split(",")
        afs.CONFIG.hosts[hostname] = ips
    afs.CONFIG.ignoreIPList = []
    for host_entry in afs.CONFIG.ignoreIP :
        afs.CONFIG.ignoreIPList.append(host_entry)

    # cast DB_CACHE to Boolean
    if afs.CONFIG.DB_CACHE.upper() == "TRUE" :  
        afs.CONFIG.DB_CACHE = True
    else :
        afs.CONFIG.DB_CACHE = False

    # LogLevels
    # don't do any logging with globalLogLevel == off
    # if empty loglevel, set to NOTSET
    
    root_logger = logging.getLogger("afs")
    if afs.CONFIG.globalLogLevel.upper() != "OFF" :
        log_handler = logging.StreamHandler()
        log_handler.setFormatter(logging.Formatter("[%(levelname)8s " + \
        "%(asctime)-15s %(name)s in %(module)s:%(lineno)d]: %(message)s "))
        root_logger.addHandler(log_handler)
        root_logger.setLevel(get_numeric_loglevel(\
            afs.CONFIG.globalLogLevel))
        #
        # setup non-DAO and non-Service loggers
        #
        if afs.CONFIG.DB_CACHE :
            # setup DB_CACHE Logging
            if afs.CONFIG.LogLevel_sqlalchemy.upper() != "OFF" :
                _logger = logging.getLogger("sqlalchemy")
                numeric_level = get_numeric_loglevel(\
                    afs.CONFIG.LogLevel_sqlalchemy)
                if numeric_level == 0 :
                    numeric_level = get_numeric_loglevel(\
                        afs.CONFIG.globalLogLevel)
                _logger.setLevel(numeric_level)
                _logger.addHandler(log_handler)
            if afs.CONFIG.LogLevel_DB_CACHE.upper() != "OFF" :
                dbcache_logger = logging.getLogger("afs.DB_CACHE") 
                dbcache_logger.setLevel(get_numeric_loglevel(\
                    afs.CONFIG.LogLevel_DB_CACHE))
        if afs.CONFIG.LogLevel_util.upper() != "OFF" :
            util_logger = logging.getLogger("afs.util") 
            util_logger.setLevel(get_numeric_loglevel(\
                afs.CONFIG.LogLevel_util))
        if afs.CONFIG.LogLevel_LookupUtil.upper() != "OFF" :
            lookuputil_logger = logging.getLogger("afs.LookupUtil") 
            lookuputil_logger.setLevel(get_numeric_loglevel(\
                afs.CONFIG.LogLevel_LookupUtil))
        if afs.CONFIG.LogLevel_Model.upper() != "OFF" :
            model_logger = logging.getLogger("afs.model") 
            model_logger.setLevel(get_numeric_loglevel(\
                afs.CONFIG.LogLevel_Model))
        #
        # setup intermediate level loggers
        #
        if afs.CONFIG.LogLevel_Service != "" :
            service_logger = logging.getLogger("afs.service") 
            service_logger.setLevel(get_numeric_loglevel(\
                afs.CONFIG.LogLevel_Service))
        if  afs.CONFIG.LogLevel_DAO != "" :
            dao_logger = logging.getLogger("afs.dao") 
            dao_logger.setLevel(get_numeric_loglevel(\
                afs.CONFIG.LogLevel_DAO))
    else :
        root_logger.addHandler(logging.NullHandler())

    # setup DB_CACHE
    if afs.CONFIG.DB_CACHE :
        import sqlalchemy
        afs.CONFIG.DB_ENGINE = afs.orm.DBMapper.create_db_engine(\
            afs.CONFIG)
        afs.orm.DBMapper.setup_db_mappings(afs.CONFIG)
        afs.DB_SESSION_FACTORY = sqlalchemy.orm.sessionmaker(\
            bind = afs.CONFIG.DB_ENGINE)

        # setup DB_HISTORY
        if afs.CONFIG.DB_HISTORY_NUM_PER_DAY > 0 :
            afs.orm.Historic.setup_db_mappings(afs.CONFIG) 

    # setup binary-pathes
    afs.CONFIG.binaries = {}
    if afs.CONFIG.binconfig == "" :
        binconfig = base_config_dir + "binaries.cfg"
    else :
        binconfig = afs.CONFIG.binconfig

    # setup LookupUtil
    afs.LOOKUP_UTIL[afs.CONFIG.cell] = \
        afs.util.LookupUtil.LookupUtil()

    file_ = file(binconfig, "r")
    while 1:
        line = file_.readline()
        if not line : 
            break
        line = line.strip()
        if len(line) == 0 : 
            continue
        if line[0] == "#" : 
            continue
        key, value = line.split("#")[0].split("=")
        if afs.CONFIG.binaries.has_key(key) :
            raise AFSError("binary %s defined twice in config file %s" % \
                (key,binconfig))
        afs.CONFIG.binaries[key] = value
    file_.close()
    return

def load_config_from_file(namespace_obj, config_file_):
    """
    load config from a file.
    Do not overwrite any already existing options.
    On lists, append new options
    """
    file_ = file(config_file_, "r")
    while 1 :
        line = file_.readline()
        if not line : 
            break
        line = line.strip()
        if not line : 
            continue
        if line[0] == "#" : 
            continue
        key = line.split("=")[0]
        value = '='.join(line.split("=")[1:])
        if hasattr(namespace_obj, key) :
            preset_key_value = namespace_obj.__getattribute__(key)
            if type(preset_key_value) == types.ListType :
                if not key in preset_key_value :
                    preset_key_value.append(value)
                    namespace_obj.__setattr__(key, preset_key_value)
            else :
                if  preset_key_value == "" :
                    namespace_obj.__setattr__(key, value)
        else :
            raise AFSError("%s: unknown option : %s " % (config_file_, key))
    file_.close()
    return namespace_obj

#
# Logger specific functions
#

def get_numeric_loglevel(string_loglevel):
    """
    return NOTSET if unknown level is given
    """
    return getattr(logging, string_loglevel.upper() , 0)
