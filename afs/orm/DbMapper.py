import sys
import afs.util.options
from afs.util.options import define, options
   

def setupOptions():
    """
    Only to be called from AfsConfig
    """
    define("DB_DEBUG", default="False", help="")
    define("DB_SID" , default="db/afspy", help="")
    define("DB_TYPE" , default="sqlite", help="")
    # mysql options
    define("DB_HOST", default="", help="")
    define("DB_PORT", default="", help="", type=int)
    define("DB_USER", default="", help="")
    define("DB_PASSWD" , default="", help="")

def createDbEngine(conf):
    """
    using conf, setup the core DB-engine
    and return it.
    The returned engine must be incorporated in the 
    used AfsConfig object
    """
    from sqlalchemy     import create_engine
    # Option definition
    ###########################################
    driver = ""
    
    # Connection
    ###########################################
    engine = 0
    if conf.DB_TYPE == "mysql":
        driver = 'mysql+pymysql://%s:%s@%s:%s/%s' % (conf.DB_USER,  conf.DB_PASSWD,conf.DB_HOST, conf.DB_PORT, conf.DB_SID)
        engine = create_engine(driver,pool_size=20, max_overflow=30, pool_recycle=3600, echo=debug)         
    elif options.DB_TYPE == "sqlite":    
        driver = 'sqlite:///'+options.DB_SID
        engine = create_engine(driver, echo=conf.DB_DEBUG)
    return engine

def setupDbMappers(conf):
    from sqlalchemy.orm import mapper
    from sqlalchemy     import Table, Column, Integer, String, MetaData, DateTime, Boolean, TEXT, Float
    from sqlalchemy     import ForeignKey, UniqueConstraint
    metadata = MetaData()
   
    # Scheduler
    ##################################################
    #FIXME ADD INDEX 
    #  Servers
    ##################################################
    tbl_server = Table('tbl_server', metadata,
          Column('id'           , Integer, primary_key=True),
          Column('uuid'         , String(255), index=True),
          Column('afsip'        , String(15),  index=True),
          Column('serv'         , String(255)),
          Column('fileserver'   , Integer),
          Column('dbserver'     , Integer ),
          Column('confserver'   , Integer ),
          Column('distserver'   , Integer ),
          Column('version'      , String(32) ),
          Column('class'        , String(2)),
          Column('status'       , String(2)),
          Column('id_location'  , Integer ),
          Column('description'  , TEXT ),
          Column('cdate'        , DateTime),
          Column('udate'        , DateTime),
          Column('sync'         , Integer ),
          sqlite_autoincrement=True
          )
    #Mapping Table
    from afs.model.Server import Server
    mapper(Server,tbl_server)  
      
    #  Partition
    ##################################################
    tbl_partition = Table('tbl_partition', metadata,
          Column('id'           , Integer, primary_key=True),
          Column('serv'         , String(255), index=True),
          Column('part'         , String(2)),
          Column('device'       , String(255)),
          Column('fstype'       , String(12)),
          Column('category'        , String(2)),
          Column('size'         , Integer ),
          Column('free'         , Integer ),
          Column('used'         , Integer ),
          Column('perc'         , Float ),
          Column('status'       , String(2)),
          Column('description'  , TEXT ),
          Column('cdate'        , DateTime),
          Column('udate'        , DateTime),
          Column('sync'         , Integer ),
          sqlite_autoincrement=True
          ) 
    #Mapping Table
    from afs.model.Partition import Partition
    mapper(Partition,tbl_partition) 
  
  
    #  Process
    ##################################################
    tbl_process = Table('tbl_process', metadata,
          Column('id'           , Integer, primary_key=True),
          Column('name'         , String(2)),
          Column('status'       , String(2)),
          Column('startdate'    , String(255)),
          Column('startcount'   , String(255)),
          Column('exitdate'     , String(255)),
          Column('notifier'     , String(255)),
          Column('state'        , String(255)),
          Column('errorstop'    , String(255) ),
          Column('core'         , String(255)),
          Column('errorexitdate', String(255) ),
          Column('errorexitdue' , String(255) ),
          Column('errorexitsignal' , String(255) ),
          Column('errorexitcode' , String(255) ),
          Column('cdate'        , DateTime),
          Column('udate'        , DateTime),
          Column('sync'         , Integer ),
          sqlite_autoincrement=True
          ) 
    #Mapping Table
    from afs.model.Process import Process
    mapper(Process,tbl_process) 

    #  Volume
    ##################################################
    tbl_volume = Table('tbl_volume', metadata,
          Column('id'           , Integer, primary_key=True),
          Column('name'         , String(255),),
          Column('vid'          , Integer,     index=True ),
          Column('serv'         , String(255), index=True),
          Column('part'         , String(2),   index=True),
          Column('parantID'     , Integer ),
          Column('backupID'     , Integer ),
          Column('cloneID'      , Integer ),
          Column('inUse'        , String(1)),
          Column('needsSalvaged', String(1)),
          Column('destroyMe'    , String(1)),
          Column('type'         , String(2)),
          Column('creationDate' , DateTime),
          Column('updateDate'   , DateTime),
          Column('backupDate'   , DateTime),
          Column('copyDate'     , DateTime),
          Column('flags'        , Integer ),
          Column('diskused'     , Integer ),
          Column('maxquota'     , Integer ),
          Column('minquota'     , Integer ),
          Column('status'       , String(2)),
          Column('filecount'    , Integer ),
          Column('dayUse'       , Integer ),
          Column('weekUse'      , Integer ),
          Column('spare2'       , Integer ),
          Column('spare3'       , Integer ),
          Column('cdate'        , DateTime),
          Column('udate'        , DateTime),
          Column('sync'         , Integer ),
          UniqueConstraint('vid', 'serv', 'part', name='uix_1'),
          sqlite_autoincrement=True
          )
             
    #Mapping Table
    from afs.model.Volume import Volume
    mapper(Volume,tbl_volume) 

    #  Volume OSD Param
    ##################################################
    tbl_volume_osd = Table('tbl_volume_osd', metadata,
          Column('id'           , Integer, primary_key=True),
          Column('fquota'       , Integer),
          Column('blockfs'      , Integer),
          Column('block_osd_on' , Integer),
          Column('block_osd_off', Integer),
          Column('pinned'       , Integer),
          Column('osdpolicy'    , Integer),
          Column('cdate'        , DateTime),
          Column('udate'        , DateTime),
          Column('sync'         , Integer )
          )   
    #Mapping Table
    from afs.model.VolumeOSD import VolumeOSD
    mapper(VolumeOSD,tbl_volume_osd) 
    
    #  Volume Ext Param
    ##################################################
    tbl_volume_extra= Table('tbl_volume_extra', metadata,
          Column('id'           , Integer, primary_key=True),
          Column('mincopy'      , Integer),
          Column('owner'        , String(255)),
          Column('project'        , String(255)),
          Column('edate'        , Integer),
          Column('category'     , String(2)),
          Column('cdate'        , DateTime),
          Column('udate'        , DateTime),
          Column('sync'         , Integer )
          ) 
    #Mapping Table
    from afs.model.VolumeExtra import VolumeExtra
    mapper(VolumeExtra,tbl_volume_extra) 
    
    try  :
        metadata.create_all(conf.DB_ENGINE) 
    except :
        sys.stderr.write("Cannot connect to %s-Database.\n" % options.DB_TYPE)
        if options.DB_TYPE == "mysql":
            sys.stderr.write("Are the MySQL parameters correct and the DB-Server up and running ?\n")
        elif options.DB_TYPE == "sqlite":
            sys.stderr.write("Is the path \"%s\" to the sqlite-DB accessible ?\n" % options.DB_SID)
        sys.exit(1)
    return
    
