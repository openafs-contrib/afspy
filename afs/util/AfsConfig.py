import os, atexit, string
import types
import logging
import sqlalchemy
import tempfile
from afs.exceptions.AfsError import AfsError
import afs
import afs.orm.DbMapper

def parseDefaultConfig(myParser=None):
    """
    setup all available options
    """
    HOME=os.environ.get("HOME","")
    ## module-wide Configuration file
    BASE_CFG_FILE="%s/etc/afspy.cfg" % os.path.dirname(afs.__file__)
    if not myParser :
        myParser = afs.argParser
    
    # mix commandline parsing with giving options in files :
    # 
    # parse most specific first, default is empty sting for all.
    # latter ones do not overwrite earlier ones.
    # add hard-coded defaults to options still being
    # an empty-string
    
    afs.defaultConfig=myParser.parse_args()
    if afs.defaultConfig.config  :
        afs.defaultConfig=loadAfsConfig(afs.defaultConfig, afs.defaultConfig.config)
    if os.path.exists("./afspy.cfg") :
        afs.defaultConfig=loadAfsConfig(afs.defaultConfig,"./afspy.cfg")
    if HOME :
        if os.path.exists("%s/.config/afspy.cfg") :
            afs.defaultConfig=loadAfsConfig(afs.defaultConfig,"%s/.config/afspy.cfg")
    if os.path.exists(BASE_CFG_FILE) :
        afs.defaultConfig=loadAfsConfig(afs.defaultConfig, BASE_CFG_FILE)
    # we need to deal with that one later
    afs.defaultConfig.Token=None

    # cast  DB_CACHE  to Boolean
    if afs.defaultConfig.DB_CACHE.upper() == "TRUE" :  
        afs.defaultConfig.DB_CACHE = True
    else :
        afs.defaultConfig.DB_CACHE= False

    # setup mandatory defaultoptions after all the parsing
    if afs.defaultConfig.DAOImplementation == "" :
        afs.defaultConfig.DAOImplementation="childprocs"
    if afs.defaultConfig.DAO_SPOOL_PARENTDIR== "" :
        afs.defaultConfig.DAO_SPOOL_PARENTDIR="/tmp/afspy"
    if afs.defaultConfig.globalLogLevel == "" :
        afs.defaultConfig.globalLogLevel = "warn"

    # LogLevels
    # don't do any logging with globalLogLevel == off
    # if empty loglevel, set to NOTSET
    
    rootLogger=logging.getLogger("afs")
    if afs.defaultConfig.globalLogLevel.upper() != "OFF" :
        LogHandler=logging.StreamHandler()
        LogHandler.setFormatter(logging.Formatter("[%(levelname)8s %(asctime)-15s  %(name)s in %(module)s:%(lineno)d]: %(message)s "))
        rootLogger.addHandler(LogHandler)
        rootLogger.setLevel(getNumericLogLevel(afs.defaultConfig.globalLogLevel))
        #
        # setup non-DAO and non-Service loggers
        #
        if afs.defaultConfig.DB_CACHE :
            # setup DB_CACHE Logging
            if afs.defaultConfig.LogLevel_sqlalchemy.upper() != "OFF" :
                _logger=logging.getLogger("sqlalchemy")
                numericLevel=getNumericLogLevel(afs.defaultConfig.LogLevel_sqlalchemy)
                if numericLevel == 0 :
                    numericLevel=getNumericLogLevel(afs.defaultConfig.globalLogLevel)
                _logger.setLevel(numericLevel)
                _logger.addHandler(LogHandler)
            if afs.defaultConfig.LogLevel_DB_CACHE.upper() != "OFF" :
                DB_CACHELogger=logging.getLogger("afs.DB_CACHE") 
                DB_CACHELogger.setLevel(getNumericLogLevel(afs.defaultConfig.LogLevel_DB_CACHE))
        if afs.defaultConfig.LogLevel_util.upper() != "OFF" :
            utilLogger=logging.getLogger("afs.util") 
            utilLogger.setLevel(getNumericLogLevel(afs.defaultConfig.LogLevel_util))
        if afs.defaultConfig.LogLevel_Model.upper() != "OFF" :
            modelLogger=logging.getLogger("afs.model") 
            modelLogger.setLevel(getNumericLogLevel(afs.defaultConfig.LogLevel_Model))
        #
        # setup intermediate level loggers
        #
        if afs.defaultConfig.LogLevel_Service != "" :
            serviceLogger=logging.getLogger("afs.service") 
            serviceLogger.setLevel(getNumericLogLevel(afs.defaultConfig.LogLevel_Service))
        if  afs.defaultConfig.LogLevel_DAO != "" :
            DAOLogger=logging.getLogger("afs.dao") 
            DAOLogger.setLevel(getNumericLogLevel(afs.defaultConfig.LogLevel_DAO))
    else :
        rootLogger.addHandler(logging.NullHandler())

    # setup DAO
    if afs.defaultConfig.DAOImplementation != "childprocs" :
        raise AfsError("Only childprocs are implemented yet.")
    
    # setup stuff necessary for detached DAO
    if afs.defaultConfig.DAOImplementation == "detached" :
        if not os.path.isdir(afs.defaultConfig.DAO_SPOOL_PARENTDIR) :
            raise  AfsError("Given SpoolParentDir '%s' for DAO does not exists or is no directory. Fix this yourself." %afs.defaultConfig.DAO_SPOOL_PARENTDIR)
        afs.defaultConfig.DAOSpoolDir=tempfile.mkdtemp(prefix=afs.defaultConfig.DAO_SPOOL_PARENTDIR)
        # register deletion of TempDir at program exit
        atexit.register(os.rmdir, afs.defaultConfig.DAOSpoolDir)
    
    # setup DB_CACHE
    if afs.defaultConfig.DB_CACHE :
        afs.defaultConfig.DB_ENGINE=afs.orm.DbMapper.createDbEngine(afs.defaultConfig)
        afs.orm.DbMapper.setupDbMappers(afs.defaultConfig)
        afs.DbSessionFactory=sqlalchemy.orm.sessionmaker(bind=afs.defaultConfig.DB_ENGINE)
    return

def loadAfsConfig(NameSpaceObj,  conf_file):
    """
    load config from a file.
    Do not overwrite any already existing options.
    On lists, append new options
    """
    f=file(conf_file, "r")
    while 1 :
        line = f.readline()
        if not line : break
        line=line.strip()
        if line[0] == "#" : continue
        key=line.split("=")[0]
        value=string.join(line.split("=")[1:], "=")
        if hasattr(NameSpaceObj, key) :
            presetValue=NameSpaceObj.__getattribute__(key)
            if type(presetValue) == types.ListType :
                if not key in  presetValue :
                    presetValue.append(value)
                    NameSpaceObj.__setattr__(key, presetValue)
            else :
                if  presetValue == "" :
                    NameSpaceObj.__setattr__(key, value)
        else :
            raise AfsError("%s: unknown option : %s " % (conf_file, key))
    f.close()
    return NameSpaceObj

#
# Logger specific functions
#

def getNumericLogLevel(StringLogLevel):
    """
    return NOTSET if unknown level is given
    """
    return getattr(logging,StringLogLevel.upper() , 0)
