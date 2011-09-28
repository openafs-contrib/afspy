import sys
import afs.util.options
from afs.util.options import define, options
   
from sqlalchemy     import create_engine
from sqlalchemy.orm import sessionmaker, mapper
from sqlalchemy     import Table, Column, Integer, String, MetaData, DateTime, Boolean, Text
from sqlalchemy     import ForeignKey, UniqueConstraint

def DbMapper(tblList):
    
    driver = ""
    define("DB_DEBUG", default="False", help="")
    define("DB_SID" , default="db/afspy", help="")
    define("DB_TYPE" , default="sqlite", help="")
    
    if options.DB_TYPE == "mysql":
        define("DB_HOST", default="", help="")
        define("DB_PORT", default="", help="", type=int)
        define("DB_USER", default="", help="")
        define("DB_PASSWD" , default="", help="")
        
        # read conf file again
        afs.util.options.parse_config_file(options.CONF_FILE)
            
        host   = options.DB_HOST
        port   = options.DB_PORT 
        sid    = options.DB_SID
        user   = options.DB_USER 
        passwd = options.DB_PASSWD
        driver = 'mysql://%s:%s@%s:%s/%s' % (user, passwd, host, port, sid)
         
    elif options.DB_TYPE == "sqlite":    
        afs.util.options.parse_config_file(options.CONF_FILE)
        driver = 'sqlite:///'+options.DB_SID
    
    debug = eval(options.DB_DEBUG)
        
    engine = create_engine(driver, echo=debug)
    metadata = MetaData()
   
   
    # Scheduler
    ##################################################
    #FIXME ADD INDEX 
    if "Volume" in tblList:
        tbl_volume = Table('tbl_volume', metadata,
          Column('id', Integer, primary_key=True),
          Column('name', String(255)),
          Column('vid', Integer ),
          Column('serv',String(255)),
          Column('part',String(2)),
          Column('parantID', Integer ),
          Column('backupID', Integer ),
          Column('cloneID',  Integer ),
          Column('inUse',String(2)),
          Column('needsSalvaged',String(1)),
          Column('destroyMe',String(1)),
          Column('type',String(2)),
          Column('creationDate',DateTime),
          Column('updateDate',DateTime),
          Column('backupDate',DateTime),
          Column('copyDate',DateTime),
          Column('flags',  Integer ),
          Column('diskused',  Integer ),
          Column('maxquota',  Integer ),
          Column('minquota',  Integer ),
          Column('status',String(2)),
          Column('filecount',  Integer ),
          Column('dayUse',  Integer ),
          Column('weekUse',  Integer ),
          Column('spare2',  Integer ),
          Column('spare3',  Integer ),
          Column('cdate',DateTime),
          Column('udate',DateTime),
          Column('sync',  Integer ),
          UniqueConstraint('name', 'serv', 'part', name='uix_1'),
          sqlite_autoincrement=True
          )
        
        
        #Mapping Table
        from afs.model.Volume import Volume
        mapper(Volume,tbl_volume) 
    
    
    try  :
        metadata.create_all(engine) 
    except :
        sys.stderr.write("Cannot connect to %s-Database.\n" % options.DB_TYPE)
        if options.DB_TYPE == "mysql":
            sys.stderr.write("Are the MySQL parameters correct and the DB-Server up and running ?\n")
        elif options.DB_TYPE == "sqlite":
            sys.stderr.write("Is the path \"%s\" to the sqlite-DB accessible ?\n" % options.DB_SID)
        sys.exit(1)
           
        
    return sessionmaker(bind=engine)
