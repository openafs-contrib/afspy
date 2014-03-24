#
# afspy configuration file.
#

#
# All options mentionend here
# can be overridden on the commandline
# using exactly the same options-name, prefixed by "--".
#


# general 
cell=ipp-garching.mpg.de

# database options
DB_CACHE=true
DB_TYPE=mysql
DB_SID=afspy_new_design
DB_HOST=localhost
DB_PORT=3306
DB_USER=afspy

# dns and networking 
# ip-addresses published by servers to ignore.
# may be given more than once
ignoreIP=

#
# hostnames to use for given IP-addresses.
# useful for silly hostaliases.
hostmap=afs-hgw1.ipp-hgw.mpg.de=194.94.214.4
hostmap=afs-db-hgw.ipp-hgw.mpg.de=194.94.214.140


#
# DAO 

# how afs-coomands should be executed.
# possible values : childprocs, detached
DAOImplementation=

#
# logging
# the argument must be one of the standard python loglevels.
globalLogLevel=warn

#
# detailed logging
# if you want to debug, you can set the LogLevel of a 
# specific module.
# available options are:

# loglevel for all DAOs:
# LogLevel_DAO=warn
# loglevel for a specific DAO, %s=classname of DAO, e.g. LogLeveL=UbikPeerDAO
# LogLevel_%s

# loglevel for Model-class operations
# LogLevel_Model

# loglevel for sqlalchemy
# LogLevel_sqlalchemy

# loglevel for DBCache-operations
# LogLevel_DB_CACHE

# loglevel for all services
# LogLevel_Service

# loglevel for a specific service, %s=classname of service, e.g. LogLeveL=LogLevel_FsService
# LogLevel_%s

# loglevel for methods in util
# LogLevel_util

# loglevel for lookup cache
# LogLevel_LookupUtil

# loglevel for setting up  orm
# LogLevel_DBManager

