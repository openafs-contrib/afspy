import sys, os
import afs.util.options
import logging
import sqlalchemy

#import module-wide logger
from afs.util import  logger

from afs.util.options import define, options
import afs.orm.DbMapper    
import afs

def setupOptions():
    """
    setup all available options
    """
    define("conf", default="",help="path to configuration file")
    define("DB_CACHE",  default="False", help="use DB cache")
    define("LogLevel", default="info", help="python Loglevel")
    define("CELL_NAME", default="beolink.org", help="Default Cell")
    define("KRB5_PRINC",  default="BEO", help="Kerberos5 Principal to use")
    define("KRB5_REALM",  default="BEOLINK.ORG", help="Kerberos5 REALM to use")
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

        # get logging level
        afs.defaultConfig.LogLevel=options.LogLevel
        numeric_level = getattr(logging,afs.defaultConfig.LogLevel.upper() , None)
        logger.setLevel(numeric_level)
        
         
        afs.defaultConfig.CELL_NAME = options.CELL_NAME
        afs.defaultConfig.KRB5_PRINC=options.KRB5_PRINC
        afs.defaultConfig.KRB5_REALM=options.KRB5_REALM
       
        # setup DB_CACHE if required
        if options.DB_CACHE.upper() == "TRUE" :  
            afs.defaultConfig.DB_CACHE = True
        else :
            afs.defaultConfig.DB_CACHE = False
        logger.debug("DB_CACHE='%s'" %afs.defaultConfig.DB_CACHE )
       
        if afs.defaultConfig.DB_CACHE :
            afs.defaultConfig.DB_LogLevel=options.DB_LogLevel
            afs.defaultConfig.DB_TYPE=options.DB_TYPE
            afs.defaultConfig.DB_SID=options.DB_SID
            afs.defaultConfig.DB_HOST=options.DB_HOST
            afs.defaultConfig.DB_PORT=options.DB_PORT
            afs.defaultConfig.DB_USER=options.DB_USER
            afs.defaultConfig.DB_PASSWD=options.DB_PASSWD
            afs.defaultConfig.DB_FLUSH=options.DB_FLUSH
            afs.defaultConfig.DB_ENGINE=afs.orm.DbMapper.createDbEngine(afs.defaultConfig)
            afs.orm.DbMapper.setupDbMappers(afs.defaultConfig)
            afs.DbSessionFactory=sqlalchemy.orm.sessionmaker(bind=afs.defaultConfig.DB_ENGINE)
        return


class AfsConfig(object):
    """
    Representation of config.
    For a secondary configuration object, do
    not parse the config files, but
    set the attributes directly
    """
    
    def __init__(self,useDefaults=True):
        # define defaults here
        if useDefaults :
            self.CRED_TYPE="TokenFromPAG"
            self.DB_CACHE=False
            self.CELL_NAME="beolink.org"
            self.DB_FLUSH=100
            self.LogLevel="info"
            self.Token=None
        return
    
    def load(self, conf_file):
        try :
            afs.util.options.parse_config_file(conf_file) 
        except afs.util.options.Error :
            print "Error: " , sys.exc_info()[1]
            sys.exit()
        return

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
