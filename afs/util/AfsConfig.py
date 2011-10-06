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
    define("CELL_NAME", default="beolink.org", help="Default Cell")

    afs.orm.DbMapper.setupOptions() 
    return

def setupDefaultConfig():
    
        HOME=os.environ.get("HOME","")
        ## System-wide Configuration file
        BASE_CFG_FILE="/etc/sysconfig/afspy"
        
        afs.util.options.parse_command_line()
        #LOCAL
        if os.path.exists(BASE_CFG_FILE) :
            afs.defaultConfig.load(BASE_CFG_FILE)
        elif options.conf :
            afs.defaultConfig.load(options.conf)
        elif os.path.exists("./afspy.cfg") :
             afs.defaultConfig.load("./afspy.cfg")
        # load personal config $HOME/.config/afspy  
        elif HOME :
            if os.path.exists("%s/.config/afspy.cfg") :
                afs.defaultConfig.load("%s/.config/afspy.cfg")

        # Overwrite from commandline
        afs.util.options.parse_command_line()
        
        afs.defaultConfig.CELL_NAME = options.CELL_NAME
        
        # setup DB_CACHE if required
        try: 
            afs.defaultConfig.DB_CACHE = eval(options.DB_CACHE)
        except:
            afs.defaultConfig.DB_CACHE = False
            
        if afs.defaultConfig.DB_CACHE :
            afs.defaultConfig.DB_TYPE=options.DB_TYPE
            afs.defaultConfig.DB_DEBUG=eval(options.DB_DEBUG)
            afs.defaultConfig.DB_SID=options.DB_SID
            afs.defaultConfig.DB_HOST=options.DB_HOST
            afs.defaultConfig.DB_PORT=options.DB_PORT
            afs.defaultConfig.DB_USER=options.DB_USER
            afs.defaultConfig.DB_PASSWD=options.DB_PASSWD
            afs.defaultConfig.DB_FLUSH=options.DB_FLUSH
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
    
    def __init__(self,useDefaults=True):
        # define defaults here
        if useDefaults :
            self.CRED_TYPE="ShellToken"
            self.DB_CACHE=False
            self.AFSCell=""
            self.DB_FLUSH=100
            self.AFSID=-1
            self.Token=None
        return
    
    def load(self, conf_file):
        try :
            afs.util.options.parse_config_file(conf_file) 
        except afs.util.options.Error :
            print "Error: " , sys.exc_info()[1]
            sys.exit()
        except:
            return

    #FIXME put in the utils used in two places
    def getDict(self):
        """
        Get a dictionary representation of the configuration
        """
        res = {}
        for attr, value in self.__dict__.iteritems():
             if type(attr) is IntType or type(attr) is StringType or type(attr) is LongType or type(attr) is UnicodeType:
                res[attr] = value
             elif isinstance(attr, datetime.datetime):
                res[attr] = value.isoformat('-')
             
        return res
