import sys
from afs.util.options import define, options
import afs.exceptions.ORMError as  ORMError
from afs.orm import logger

def setupOptions():
    """
    Only to be called from AfsConfig
    """
    define("DB_SID" , default="db/afspy", help="Database name or for sqlite path to DB file")
    define("DB_TYPE" , default="sqlite", help="Type of DB. [mysql|sqlite]")
    # mysql options
    define("DB_HOST", default="", help="Database host")
    define("DB_PORT", default="", help="Database port", type=int)
    define("DB_USER", default="", help="Database user")
    define("DB_PASSWD" , default="", help="Database password")
    define("DB_FLUSH", default=100, help="Max Number of elements in Buffer")

    
def createDbEngine(conf):
    """
    using conf, setup the core DB-engine
    and return it.
    The returned engine must be incorporated in the 
    used AfsConfig object
    """
    from sqlalchemy import create_engine

    # Option definition
    ###########################################
    driver = ""
    
    # Connection
    ###########################################
    engine = 0
    if conf.DB_TYPE == "mysql":
        driver = 'mysql+pymysql://%s:%s@%s:%s/%s' % (conf.DB_USER,  conf.DB_PASSWD,conf.DB_HOST, conf.DB_PORT, conf.DB_SID)
        logger.debug("creating engine with driver :'%s'" % driver)
        try: 
            engine = create_engine(driver,pool_size=20, max_overflow=30, pool_recycle=3600, echo=False)         
        except :
            raise ORMError.createEngineError(conf)
    elif options.DB_TYPE == "sqlite":    
        driver = 'sqlite:///'+options.DB_SID
        logger.debug("creating engine with driver :'%s'" % driver)
        try:
            engine = create_engine(driver, echo=False)
        except :
            raise ORMError.createEngineError(conf)
    return engine

def setupDbMappers(conf):
    from sqlalchemy.orm import mapper
    from sqlalchemy     import Table, Column, Integer, String, MetaData, DateTime, Boolean, TEXT, Float
    from sqlalchemy     import  UniqueConstraint
    from sqlalchemy     import  PickleType

    logger.debug("Entering setupDbMappers")
    metadata = MetaData()
   
    # Scheduler
    ##################################################
    
    #  Servers
    ##################################################
    tbl_server = Table('tbl_server', metadata,
          Column('id'           , Integer, primary_key=True),
          Column('uuid'         , String(255), index=True),
          Column('servernames'         , PickleType(mutable=True)),
          Column('ipaddrs'         , PickleType(mutable=True)),
          Column('fileserver'   , Boolean),
          Column('dbserver'     , Boolean ),
          Column('clonedbserver'     , Boolean ),
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
          Column('serv_uuid'         , String(255), index=True),
          Column('name'         , String(2)),
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
  
  
    #  BOS
    ##################################################
    tbl_bos = Table('tbl_bos', metadata,
          Column('id'           , Integer, primary_key=True),
          Column('serv'         , String(255)),
          Column('generalRestartTime' , DateTime),
          Column('binaryRestartTime'  , DateTime),
          Column('cdate'        , DateTime),
          Column('udate'        , DateTime),
          Column('sync'         , Integer ),
          sqlite_autoincrement=True
          ) 
    #Mapping Table
    from afs.model.Bos import Bos
    mapper(Bos,tbl_bos) 
  
    #  BNodes (Server Processes)
    ##################################################
    tbl_bnode = Table('tbl_bnode', metadata,
          Column('id'           , Integer, primary_key=True),
          Column('bos_id'       , Integer),
          Column('type'         , String(2)),
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
    from afs.model.BNode import BNode
    mapper(BNode,tbl_bnode) 

    #  Volume
    ##################################################
    tbl_volume = Table('tbl_volume', metadata,
          Column('id'           , Integer, primary_key=True),
          Column('name'         , String(255)),
          Column('vid'          , Integer,     index=True ),
          Column('serv_uuid'         , String(255), index=True),
          Column('part'         , String(2),   index=True),
          Column('servername' , String(255 )), 
          Column('parentID'     , Integer ),
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
          UniqueConstraint('vid', 'serv_uuid', 'part', name='uix_1'),
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
          Column('project'      , String(255)),
          Column('edate'        , Integer),
          Column('category'     , String(2)),
          Column('cdate'        , DateTime),
          Column('udate'        , DateTime),
          Column('sync'         , Integer )
          ) 
    #Mapping Table
    from afs.model.VolumeExtra import VolumeExtra
    mapper(VolumeExtra,tbl_volume_extra) 
   
    #  Project Table
    ##################################################
    tbl_project =  Table('tbl_project',metadata,
          Column('id'           , Integer, primary_key=True),
          Column('name'        , String(255)),
          Column('contact'        , String(255)),
          Column('owner'        , String(255)),
          Column('rw_locations',  PickleType), 
          Column('ro_locations',  PickleType), 
          Column('rw_serverparts',  PickleType), 
          Column('ro_serverparts',  PickleType), 
          Column('volnameRegEx',  PickleType),
          Column('additionalVolnames',  PickleType), 
          Column('excludedVolnames',  PickleType), 
          Column('minSize_kB'         , Integer ), 
          Column('maxSize_kB'         , Integer ), 
          Column('minnum_ro'      , Integer),
          Column('cdate'        , DateTime),
          Column('udate'        , DateTime),
          Column('sync'         , Integer )
          )

    #Map Table to object
    from afs.model.Project import Project
    mapper(Project,tbl_project) 

    #  Cell Table
    ##################################################
    tbl_cell =  Table('tbl_cell',metadata,
        Column('id'           , Integer, primary_key=True),
        Column('name'        , String(255), index=True ),
        Column('DBServers'        , String(512)),
        Column('VLDBSyncSite'        , String(50)),
        Column('PTDBSyncSite'        , String(50)),
        Column('VLDBVersion'        , String(20)),
        Column('PTDBVersion'        , String(20)),
        Column('FileServers'         , PickleType(mutable=True)),
        Column('DBServers'         , PickleType(mutable=True)),
        Column('cdate'        , DateTime),
        Column('udate'        , DateTime),
        )
        
    #Map Table to object
    from afs.model.Cell import Cell
    mapper(Cell,tbl_cell) 

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
    
