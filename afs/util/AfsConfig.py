import sys, os, atexit
import afs.util.options
import logging
import sqlalchemy
import tempfile
from types import IntType, StringType, LongType,  UnicodeType
#import module-wide logger
from afs.util import  logger
from afs.exceptions import AfsError
from afs.util.options import define, options   
import afs
import afs.orm.DbMapper
import datetime


def setupOptions():
    """
    setup all available options
    """
    define("conf", default="",help="path to configuration file")
    define("DB_CACHE",  default="False", help="use DB cache")
    define("DAOImplementation", default="childprocs", help="Implementation of how to access AFS-Cell" )
    define("DAO_SPOOL_PARENTDIR", default="/tmp/afspy/", help="If using 'childprocs'-DAO,  use spool dir under this path")
    define("globalLogLevel", default="info", help="global python Loglevel")
    define("classLogLevels", default="info", help="CSV list of 'class=LogLevel', to turn logging on and off for specific classes")
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

        # setup the different loglevel
        afs.defaultConfig.givenClassLogLevels=options.classLogLevels
        afs.defaultConfig.classLogLevels={}
        for i in afs.defaultConfig.givenClassLogLevels.split(",") :
            Name, Level=i.split("=")
            afs.defaultConfig.classLogLevels[Name] = Level
        afs.defaultConfig.globalLogLevel=options.globalLogLevel
        numeric_level = getattr(logging,afs.defaultConfig.globalLogLevel.upper() , None)
        logger.setLevel(numeric_level)
        
        afs.defaultConfig.CELL_NAME = options.CELL_NAME
        afs.defaultConfig.KRB5_PRINC=options.KRB5_PRINC
        afs.defaultConfig.KRB5_REALM=options.KRB5_REALM
        
        # setup DAO
        if options.DAOImplementation != "childprocs" :
            raise AfsError.AfsError("Only childprocs are implemented yet.")
        
        afs.defaultConfig.DAOImplementation=options.DAOImplementation
        afs.defaultConfig.DAO_SPOOL_PARENTDIR = options.DAO_SPOOL_PARENTDIR
        # create Spooldir itself
        if not os.path.isdir(afs.defaultConfig.DAO_SPOOL_PARENTDIR) :
            raise AfsError.AfsError("Given SpoolParentDir '%s' for DAO does not exists or is no directory. Fix this yourself." %afs.defaultConfig.DAO_SPOOL_PARENTDIR)
        afs.defaultConfig.DAOSpoolDir=tempfile.mkdtemp(prefix=afs.defaultConfig.DAO_SPOOL_PARENTDIR)
        # register deletion of TempDir at program exit
        atexit.register(os.rmdir, afs.defaultConfig.DAOSpoolDir)
        
        # setup DB_CACHE if required
        if options.DB_CACHE.upper() == "TRUE" :  
            afs.defaultConfig.DB_CACHE = True
        else :
            afs.defaultConfig.DB_CACHE = False
        logger.debug("DB_CACHE='%s'" %afs.defaultConfig.DB_CACHE )
        sqlalchemyLogLevel=afs.defaultConfig.classLogLevels.get("sqlalchemy", None)
        if sqlalchemyLogLevel != None :
            sqlalchemyLogger=logging.getLogger("sqlalchemy")
            sqlalchemyLogger.setLevel(getattr(logging, afs.defaultConfig.classLogLevels["sqlalchemy"].upper()))
        
        if afs.defaultConfig.DB_CACHE :
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

