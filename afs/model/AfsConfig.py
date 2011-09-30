import sys, os
import afs.util.options
from afs.util.options import define, options


def setupOptions():
    """
    setup all available options
    """
    define("conf", default="",help="path to configuration file")
    import afs.orm.DbMapper    
    afs.orm.DbMapper.setupOptions() 
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
        if fresh:
            # 1. load system-wide config /etc/sysconfig/afspy
            if os.path.exists(self.BASE_CFG_FILE) :
                self.load(self.BASE_CFG_FILE)
            # 2. load personal config $HOME/.config/afspy
            HOME=os.environ.get("HOME","")
            if HOME :
                if os.path.exists("%s/.config/afspy") :
                    self.load("%s/.config/afspy")
            # 4. parse command line to get config-file
            afs.util.options.parse_command_line()
            # 5. load config-file given on command line
            if options.conf :
                self.load(options.conf)
            # 5. reparse command line to give it the highest priority
            afs.util.options.parse_command_line()
            # setup DB_CACHE if required
            self.DB_CACHE = eval(options.DB_CACHE)
        return
    
    def load(self, conf_file):
        try :
            afs.util.options.parse_config_file(conf_file) 
        except afs.util.options.Error :
            print "Error: " , sys.exc_info()[1]
            sys.exit()
        except:
            return       
        
