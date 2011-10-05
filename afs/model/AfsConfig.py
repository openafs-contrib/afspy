import sys, os
import afs.util.options
from afs.util.options import define, options
import afs.orm.DbMapper    
import afs

def setupOptions():
    """
    setup all available options
    """
    define("conf", default="",help="path to configuration file")
    define("DB_CACHE",  default="False", help="Flag")
    afs.orm.DbMapper.setupOptions() 
    return

def setupDefaultConfig():
    
        HOME=os.environ.get("HOME","")
        #LOCAL
        if options.conf :
            afs.defaultConfig.load(options.conf)
        elif os.path.exists("./afspy.cfg") :
             afs.defaultConfig.load("./afspy.cfg")
        # load personal config $HOME/.config/afspy  
        elif HOME :
            if os.path.exists("%s/.config/afspy.cfg") :
                afs.defaultConfig.load("%s/.config/afspy.cfg")
        # 1. load system-wide config /etc/sysconfig/afspy
        elif os.path.exists(defaultConfig.BASE_CFG_FILE) :
            afs.defaultConfig.load(defaultConfig.BASE_CFG_FILE)
        
        # Overwrite from commandline
        afs.util.options.parse_command_line()
        
        # setup DB_CACHE if required
        try: 
            afs.defaultConfig.DB_CACHE = eval(options.DB_CACHE)
        except:
            afs.defaultConfig.DB_CACHE = False
            
        if afs.defaultConfig. DB_CACHE :
            afs.defaultConfig.DB_TYPE=options.DB_TYPE
            afs.defaultConfig.DB_DEBUG=eval(options.DB_DEBUG)
            afs.defaultConfig.DB_SID=options.DB_SID
            afs.defaultConfig.DB_HOST=options.DB_HOST
            afs.defaultConfig.DB_PORT=options.DB_PORT
            afs.defaultConfig.DB_USER=options.DB_USER
            afs.defaultConfig.DB_PASSWD=options.DB_PASSWD
            afs.defaultConfig.DB_ENGINE=afs.orm.DbMapper.createDbEngine(afs.defaultConfig)
            afs.orm.DbMapper.setupDbMappers(afs.defaultConfig)
        return


class AfsConfig(object):
    """
    Representation of config.
    For a secondary configuration object, do
    not parse the config files directly, but
    set the attributes directly
    """
    ## System-wide Configuration file
    BASE_CFG_FILE="/etc/sysconfig/afspy"
    ## Flag if database cache should be used
    DB_CACHE = "False"
    
    def __init__(self,fresh=False):
        return
    
    def load(self, conf_file):
        try :
            afs.util.options.parse_config_file(conf_file) 
        except afs.util.options.Error :
            print "Error: " , sys.exc_info()[1]
            sys.exit()
        except:
            return
