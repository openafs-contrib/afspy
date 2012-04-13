import sys
from afs.exceptions.ORMError import ORMError
import afs
import logging

logger=logging.getLogger("afs.DB_CACHE")

def createDbEngine(conf=None):
    """
    using conf, setup the core DB-engine
    and return it.
    The returned engine must be incorporated in the 
    used AfsConfig object
    """
    from sqlalchemy import create_engine
    if conf:
        _CFG = conf
    else:
        _CFG = afs.defaultConfig

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
            raise ORMError("Cannot create DB Engine for type mysql using driver %s" % driver )
    elif _CFG.DB_TYPE == "sqlite":    
        driver = 'sqlite:///'+_CFG.DB_SID
        logger.debug("creating engine with driver :'%s'" % driver)
        try:
            engine = create_engine(driver, echo=False)
        except :
            raise ORMError("Cannot create DB Engine for type sqlite using driver %s " % driver )
    return engine

def safeMapping( ModelClass, TableDef):
    from afs.model.BaseModel import BaseModel
    from sqlalchemy.orm import mapper
    
    ModelObj=ModelClass()
    ModelAttributes=dir(ModelObj)
    BaseModelAttributes=dir(BaseModel())
    m=mapper(ModelClass, TableDef)
    mappedColumns=m.columns.keys()
    
    for k in ModelAttributes :
        # ignore private sqlalchemy methods
        if k[0] == "_" : continue
        # ignore stuff defined in BaseModel (includes all general private methods of an obj.)
        if k in BaseModelAttributes : continue
        if not k in mappedColumns :
            raise ORMError("Mapping of model Object '%s' not correct. Attribute '%s' not mapped." % (ModelObj.__class__.__name__,k) )
    
    for c in mappedColumns :
        if not c in ModelAttributes :
            raise ORMError("Mapping of model Object '%s' not correct. Mapped attribute '%s' not in Objectmodel." % (ModelObj.__class__.__name__, c))
    
def setupDbMappers(conf=None):
    from sqlalchemy     import Table, Column, Integer, String, MetaData, DateTime, Boolean, TEXT, Float
    from sqlalchemy     import  ForeignKeyConstraint
    from sqlalchemy     import  PickleType
    
    if conf:
        _CFG = conf
    else:
        _CFG = afs.defaultConfig
   
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
          Column('status'       , String(2)),
          Column('id_location'  , Integer ),
          Column('description'  , TEXT ),
          Column('cdate'        , DateTime),
          Column('udate'        , DateTime),
          Column('sync'         , Integer ),
          Column('isComplete'   , Boolean ),
          sqlite_autoincrement=True
          )
    #Mapping Table
    from afs.model.Server import Server
    safeMapping(Server,tbl_server)
      
    #  Partition
    ##################################################
    tbl_partition = Table('tbl_partition', metadata,
          Column('id'           , Integer, primary_key=True),
          Column('serv_uuid'         , String(255), index=True),
          Column('name'         , String(2)),
          Column('device'       , String(255)),
          Column('size'         , Integer ),
          Column('free'         , Integer ),
          Column('used'         , Integer ),
          Column('usedPerc'         , Float ),
          Column('projectIDs'      , PickleType),
          Column('status'       , String(2)),
          Column('description'  , TEXT ),
          Column('cdate'        , DateTime),
          Column('udate'        , DateTime),
          Column('sync'         , Integer ),
          Column('isComplete'   , Boolean ),
          sqlite_autoincrement=True
          ) 
    #Mapping Table
    from afs.model.Partition import Partition
    safeMapping(Partition,tbl_partition)
  
  
    #  BOS
    ##################################################
    tbl_bos = Table('tbl_bos', metadata,
          Column('id'           , Integer, primary_key=True),
          Column('servername'         , String(255)),
          Column('generalRestartTime' , DateTime),
          Column('binaryRestartTime'  , DateTime),
          Column('cdate'        , DateTime),
          Column('udate'        , DateTime),
          Column('sync'         , Integer ),
          sqlite_autoincrement=True
          ) 
    #Mapping Table
    from afs.model.Bos import Bos
    safeMapping(Bos,tbl_bos)
  
    #  BNodes (Server Processes)
    ##################################################
    tbl_bnode = Table('tbl_bnode', metadata,
          Column('id'           , Integer, primary_key=True),
          Column('bos_id'       , Integer),
          Column('BNodeType'         , String(2)),
          Column('status'       , String(2)),
          Column('Commands'    , String(255)),
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
    safeMapping(BNode,tbl_bnode) 

    #  Volume
    ##################################################
    tbl_volume = Table('tbl_volume', metadata,
          Column('id'           , Integer, primary_key=True),
          Column('name'         , String(255)),
          Column('vid'          , Integer,     index=True ),
          Column('serv_uuid'    , String(255), index=True),
          Column('part'         , String(2),   index=True),
          Column('servername'   , String(255 )), 
          Column('parentID'     , Integer ),
          Column('backupID'     , Integer ),
          Column('cloneID'      , Integer ),
          Column('inUse'        , String(1)),
          Column('needsSalvaged', String(1)),
          Column('destroyMe'    , String(1)),
          Column('type'         , String(2)),
          Column('creationDate' , DateTime),
          Column('accessDate'   , DateTime),
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
          # old installation
          #UniqueConstraint('vid', 'servername', 'part','name',  name='uix_1'),
          sqlite_autoincrement=True
          )
             
    #Mapping Table
    from afs.model.Volume import Volume
    safeMapping(Volume,tbl_volume)
    
    #  Volume Ext Param
    ##################################################
    tbl_extvolattr= Table('tbl_extvolattr', metadata,
          Column('vid', Integer, primary_key=True ), 
          Column('mincopy'      , Integer),
          Column('owner'        , String(255)),
          Column('projectID'      , Integer),
          Column('pinnedOnServer'       , Integer),
          Column('cdate'        , DateTime),
          Column('udate'        , DateTime),
          Column('sync'         , Integer ), 
          ForeignKeyConstraint(['vid'], ['tbl_volume.vid'])
          ) 
    #Mapping Table
    from afs.model.ExtendedVolumeAttributes import ExtVolAttr
    safeMapping(ExtVolAttr,tbl_extvolattr)
   
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
    safeMapping(Project,tbl_project)

    #  Cell Table
    ##################################################
    tbl_cell =  Table('tbl_cell',metadata,
        Column('id'           , Integer, primary_key=True),
        Column('Name'        , String(255), index=True ),
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
    safeMapping(Cell,tbl_cell)

    #  Volume OSD Param
    ##################################################
    tbl_extvolattr_osd= Table('tbl_extvolattr_osd', metadata,
          Column('vid'           , Integer, primary_key=True),
          Column('fquota'       , Integer),
          Column('blockfs'      , Integer),
          Column('block_osd_on' , Integer),
          Column('block_osd_off', Integer),
          Column('osdpolicy'    , Integer),
          Column('cdate'        , DateTime),
          Column('udate'        , DateTime),
          Column('sync'         , Integer ), 
          ForeignKeyConstraint(['vid'], ['tbl_volume.vid'])
          )   
    #Mapping Table
    from afs.model.ExtendedVolumeAttributes_OSD import ExtVolAttr_OSD
    safeMapping(ExtVolAttr_OSD,tbl_extvolattr_osd) 


    metadata.create_all(conf.DB_ENGINE) 
    try  :
        metadata.create_all(conf.DB_ENGINE) 
    except :
        sys.stderr.write("Cannot connect to %s-Database.\n" % _CFG.DB_TYPE)
        if _CFG.DB_TYPE == "mysql":
            sys.stderr.write("Are the MySQL parameters correct and the DB-Server up and running ?\n")
        elif _CFG.DB_TYPE == "sqlite":
            sys.stderr.write("Is the path \"%s\" to the sqlite-DB accessible ?\n" % _CFG.DB_SID)
        sys.exit(1)
    return
    
