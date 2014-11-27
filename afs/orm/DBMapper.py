"""
declare and handle object relational mapping of the model objects
"""
import sys
from afs.orm.ORMError import ORMError
import afs
import logging, datetime

LOGGER = logging.getLogger("afs.DB_CACHE")

def create_db_engine(conf=None):
    """
    using conf, setup the core DB-engine
    and return it.
    The returned engine must be incorporated in the
    used AfsConfig object
    """
    from sqlalchemy import create_engine
    if conf:
        _cfg = conf
    else:
        _cfg = afs.CONFIG

    # Option definition
    ###########################################
    driver = ""

    # Connection
    ###########################################
    engine = 0
    if conf.DB_TYPE == "mysql":
        driver = 'mysql://%s:%s@%s:%s/%s' % (conf.DB_USER,  conf.DB_PASSWD, \
            conf.DB_HOST, conf.DB_PORT, conf.DB_SID)
        LOGGER.debug("creating engine with driver :'%s'" % driver)
        try:
            engine = create_engine(driver, pool_size = 20,  max_overflow = 30, \
                pool_recycle = 3600, echo = False)
        except :
            raise ORMError("Cannot create DB Engine for mysql using driver %s" \
                % driver )
    elif _cfg.DB_TYPE == "sqlite":
        driver = 'sqlite:///' + _cfg.DB_SID
        LOGGER.debug("creating engine with driver :'%s'" % driver)
        try:
            engine = create_engine(driver, echo = False)
        except :
            raise ORMError("Cannot create DB Engine for sqlite " +
                "using driver %s"  % driver)
    return engine

def safe_mapping(model_class, table_definition) :
    """
    function to safely map object to db-tables.
    Ensures that the conventions about objects
    are followed.
    """
    from afs.model.BaseModel import BaseModel
    from sqlalchemy.orm import mapper

    model_object = model_class()
    model_attributes = dir(model_object)
    base_model_attributes = dir(BaseModel())
    _mapper = mapper(model_class, table_definition)
    mapped_columns = _mapper.columns.keys()

    for k in model_attributes :
        # ignore private sqlalchemy methods
        if k[0] == "_" : continue
        # a python-only attribute to define
        # which other attributes should not put into the DB
        if k == "unmapped_attributes_list" : continue
        # ignore stuff defined in BaseModel
        # (includes all general private methods of an obj.)
        if k in base_model_attributes : continue
        if not k in mapped_columns :
            # ignore fields which are json encoded in DB
            if "%s_js" % k in mapped_columns : continue
            raise ORMError("Mapping of model Object '%s' not correct. " % \
                ( model_object.__class__.__name__) + \
                "Attribute '%s' not mapped." % k )

    for column in mapped_columns :
        if not column in model_attributes :
            raise ORMError("Mapping of model Object '%s' not correct. " % \
                (model_object.__class__.__name__) + \
                "Mapped attribute '%s' not in Objectmodel." % column )

def setup_db_mappings(conf = None) :
    """
    function to setup the objects-database mappings
    """
    from sqlalchemy import Table, Column, Integer, BigInteger, String, \
        MetaData, DateTime, Boolean, TEXT
    from sqlalchemy import ForeignKeyConstraint, ForeignKey, UniqueConstraint

    if conf:
        _cfg = conf
    else:
        _cfg = afs.CONFIG

    LOGGER.debug("Entering setupDbMappers")
    metadata = MetaData()

    #  Servers
    ##################################################
    tbl_fileserver = Table('tbl_fileserver', metadata,
        Column('db_id', Integer, primary_key = True),
        Column('uuid', String(255), index = True),
        Column('servernames_js', TEXT),
        Column('ipaddrs_js', TEXT),
        Column('version', String(32) ),
        Column('build_date', String(32) ),
        Column('db_creation_date', DateTime),
        Column('db_update_date', DateTime),
        )
    # create mapping table
    from afs.model.FileServer import FileServer
    safe_mapping(FileServer, tbl_fileserver)

    tbl_extfileservattr = Table('tbl_extfileservattr', metadata,
        Column('db_id', Integer, primary_key = True),
        Column('server_db_id', Integer),
        Column('location', String(32) ),
        Column('owner', String(32) ),
        Column('description', TEXT ),
        Column('db_creation_date', DateTime),
        Column('db_update_date', DateTime),
        )

    # create mapping table
    from afs.model.ExtendedFileServerAttributes import ExtFileServAttr
    safe_mapping(ExtFileServAttr, tbl_extfileservattr)

    tbl_dbserver = Table('tbl_dbserver', metadata,
        Column('db_id', Integer, primary_key = True),
        Column('servernames_js', TEXT),
        Column('ipaddr', String(32)),
        Column('afsdb_type', String(32) ),
        Column('local_afsdb_version', String(32) ),
        Column('is_clone', Boolean ),
        Column('version', String(32) ),
        Column('build_date', String(32) ),
        Column('db_creation_date', DateTime),
        Column('db_update_date', DateTime),
        )

    #Mapping Table
    from afs.model.DBServer import DBServer
    safe_mapping(DBServer, tbl_dbserver)

    tbl_extdbservattr = Table('tbl_extdbservattr', metadata,
        Column('db_id', Integer, primary_key = True),
        Column('server_db_id', Integer),
        Column('location', String(32) ),
        Column('owner', String(32) ),
        Column('description', TEXT ),
        Column('db_creation_date', DateTime),
        Column('db_update_date', DateTime),
        )

    #Mapping Table
    from afs.model.ExtendedDBServerAttributes import ExtDBServAttr
    safe_mapping(ExtDBServAttr, tbl_extdbservattr)

    #
    # BosServer
    #

    tbl_bosserver = Table('tbl_bosserver', metadata,
        Column('db_id', Integer, primary_key = True),
        Column('servernames_js', TEXT),
        Column('ipaddrs_js', TEXT),
        Column('superusers_js', TEXT),
        Column('db_servers_js', TEXT),
        Column('restart_times_js', String(256) ),
        Column('version', String(32) ),
        Column('build_date', String(32) ),
        Column('db_creation_date', DateTime),
        Column('db_update_date', DateTime),
        )

    #Mapping Table
    from afs.model.BosServer import BosServer
    safe_mapping(BosServer, tbl_bosserver)


    #
    #  BNodes (Server Processes)
    #

    tbl_bnode = Table('tbl_bnode', metadata,
        Column('db_id', Integer, primary_key = True),
        Column('bos_db_id', Integer),
        Column('bnode_type', String(6)),
        Column('instance_name', String(255)),
        Column('status', String(10)),
        Column('commands_js', TEXT),
        Column('start_date', DateTime),
        Column('start_count', String(255)),
        Column('last_exit_date', DateTime),
        Column('notifier', String(255)),
        Column('error_stop', String(255) ),
        Column('core', String(255)),
        Column('error_exit_date', DateTime ),
        Column('error_exit_due', String(255) ),
        Column('error_exit_signal', String(255) ),
        Column('error_exit_code', String(255) ),
        Column('db_creation_date', DateTime),
        Column('db_update_date', DateTime),
        )

    #Mapping Table
    from afs.model.BNode import BNode
    safe_mapping(BNode, tbl_bnode)

    #  Partition
    ##################################################
    tbl_partition = Table('tbl_partition', metadata,
        Column('db_id', Integer, primary_key = True),
        Column('fileserver_uuid', String(255), index = True),
        Column('name', String(2),index=True),
        Column('size_kb', BigInteger ),
        Column('free_kb', BigInteger ),
        Column('used_kb', BigInteger ),
        Column('db_creation_date', DateTime),
        Column('db_update_date', DateTime),
        )
    #Mapping Table
    from afs.model.Partition import Partition
    safe_mapping(Partition, tbl_partition)

    tbl_extpartattr = Table('tbl_extpartattr', metadata,
        Column('db_id', Integer, primary_key = True),
        Column('fileserver_uuid', String(255), ForeignKey("tbl_partition.fileserver_uuid"),\
            nullable = False),
        Column('name', String(2), ForeignKey("tbl_partition.name"),\
            nullable = False),
        Column('project_ids_js', TEXT),
        Column('allocated', BigInteger ),
        Column('allocated_stale', BigInteger ),
        Column('owner', String(255)),
        Column('unlimited_volumes', Integer ),
        Column('num_vol_rw', Integer, nullable = False, default = 0),
        Column('num_vol_ro', Integer, nullable = False, default = 0),
        Column('num_vol_bk', Integer, nullable = False, default = 0),
        Column('num_vol_offline', Integer, nullable = False, default = 0),
        Column('db_creation_date', DateTime),
        Column('db_update_date', DateTime),
        )

    #Mapping Table
    from afs.model.ExtendedPartitionAttributes import ExtPartAttr
    safe_mapping(ExtPartAttr, tbl_extpartattr)

    #  Volume
    ##################################################
    tbl_volume = Table('tbl_volume', metadata,
        Column('db_id', Integer, primary_key = True),
        Column('name', String(255)),
        Column('vid', Integer, index = True ),
        Column('fileserver_uuid', String(255), index = True),
        Column('partition', String(2), index = True),
        Column('servername', String(255)),
        Column('parent_id', Integer ),
        Column('readonly_id', Integer ),
        Column('backup_id', Integer ),
        Column('clone_id', Integer ),
        Column('in_use', String(1)),
        Column('needs_salvage', String(1)),
        Column('destroy_me', String(1)),
        Column('type', String(2)),
        Column('creation_date', DateTime),
        Column('access_date', DateTime),
        Column('backup_date', DateTime),
        Column('update_date', DateTime),
        Column('copy_date', DateTime),
        Column('flags', Integer ),
        Column('diskused', Integer ),
        Column('maxquota', Integer ),
        Column('minquota', Integer ),
        Column('status', String(2)),
        Column('filecount', Integer ),
        Column('day_use', Integer ),
        Column('week_use', Integer ),
        Column('spare2', Integer ),
        Column('spare3', Integer ),
        Column('db_creation_date', DateTime),
        Column('db_update_date', DateTime),
        )

    #Mapping Table
    from afs.model.Volume import Volume
    safe_mapping(Volume, tbl_volume)

    #  Volume Ext Param
    ##################################################
    tbl_extvolattr = Table('tbl_extvolattr', metadata,
        Column('vid', Integer, primary_key = True),
        Column('num_min_copy', Integer),
        Column('owner', String(255)),
        Column('project_ids_js', TEXT),
        Column('pinned_on_server', Integer),
        Column('db_creation_date', DateTime),
        Column('db_update_date', DateTime),
        ForeignKeyConstraint(['vid'], ['tbl_volume.vid'])
        )
    #Mapping Table
    from afs.model.ExtendedVolumeAttributes import ExtVolAttr
    safe_mapping(ExtVolAttr, tbl_extvolattr)


    #  Project Table
    ##################################################
    tbl_project =  Table('tbl_project', metadata,
        Column('db_id', Integer, primary_key = True),
        Column('name', String(255)),
        Column('contact', String(255)),
        Column('owner', String(255)),
        Column('specificity', Integer),
        Column('description', String(1023)),
        Column('rw_locations_js', TEXT),
        Column('ro_locations_js', TEXT),
        Column('rw_serverparts_js', TEXT),
        Column('ro_serverparts_js', TEXT),
        Column('volname_regex_js', TEXT),
        Column('additional_volnames_js', TEXT),
        Column('excluded_volnames_js', TEXT),
        Column('min_size_kb', Integer ),
        Column('max_size_kb', Integer ),
        Column('num_min_ro', Integer),
        Column('db_creation_date', DateTime),
        Column('db_update_date', DateTime),
        )

    #Map Table to object
    from afs.model.Project import Project
    safe_mapping(Project, tbl_project)

    #  Project Spread
    ##################################################
    tbl_project_spread = Table('tbl_project_spread', metadata,
        Column('db_id', Integer, primary_key = True),
        Column('project_id', Integer),
        Column('fileserver_uuid',  String(255)),
        Column('part', String(2)),
        Column('blocks_fs', BigInteger),
        Column('blocks_osd_on' , BigInteger),
        Column('blocks_osd_off', BigInteger),
        Column('vol_type', String(2)),
        Column('used_kb', BigInteger),
        Column('num_vol', Integer ),
        Column('db_creation_date', DateTime),
        Column('db_update_date', DateTime),
            UniqueConstraint('project_id', 'fileserver_uuid', 'part', 'vol_type',\
            name='uix_1')
        )

    #Map Table to object
    from afs.model.ProjectSpread import ProjectSpread
    safe_mapping(ProjectSpread, tbl_project_spread)

    #  Cell Table
    ##################################################
    tbl_cell =  Table('tbl_cell', metadata,
        Column('db_id', Integer, primary_key = True),
        Column('name', String(255), index = True ),
        Column('vldb_sync_site', String(50), nullable = False, default = ""),
        Column('ptdb_sync_site', String(50), nullable = False, default = ""),
        Column('vldb_version', String(20), nullable = False, default = ""),
        Column('ptdb_version', String(20), nullable = False, default = ""),
        Column('vldb_state', String(20), nullable = False, default = ""),
        Column('ptdb_state', String(20), nullable = False, default = ""),
        Column('file_servers_js', TEXT),
        Column('db_servers_js', TEXT),
        Column('projects_js', TEXT),
        Column('size_kb', BigInteger,  nullable = False, default = 0),
        Column('used_kb', BigInteger,  nullable = False, default = 0),
        Column('free_kb', BigInteger,  nullable = False, default = 0),
        Column('allocated_kb', BigInteger, nullable = False, default = 0),
        Column('allocated_stale_kb', BigInteger, nullable = False, default = 0),
        Column('num_vol_rw', Integer, nullable = False, default = 0),
        Column('num_vol_ro', Integer, nullable = False, default = 0),
        Column('num_vol_bk', Integer, nullable = False, default = 0),
        Column('num_vol_offline', Integer, nullable = False, default = 0),
        Column('num_users', Integer, nullable = False, default = 0),
        Column('num_groups', Integer, nullable = False, default = 0),
        Column('db_creation_date', DateTime),
        Column('db_update_date', DateTime, onupdate = datetime.datetime.now)
        )

    #Map Table to object
    from afs.model.Cell import Cell
    safe_mapping(Cell, tbl_cell)

    metadata.create_all(conf.DB_ENGINE)
    try  :
        metadata.create_all(conf.DB_ENGINE)
    except :
        sys.stderr.write("Cannot connect to %s-Database.\n" % _cfg.DB_TYPE)
        if _cfg.DB_TYPE == "mysql":
            sys.stderr.write("Are the MySQL parameters correct and the " +\
            "DB-Server up and running ?\n")
        elif _cfg.DB_TYPE == "sqlite":
            sys.stderr.write("Is the path \"%s\" to the sqlite-DB " + \
            "accessible ?\n" % _cfg.DB_SID)
        sys.exit(1)
    return
