# Init 

__all__=["dao","exceptions","factory","model","orm","service","util"]
import orm
import dao
import service
import util
import model

# define and setup argParser here so that it can be used in all linked-in modules
import argparse

# get module-local parsers:
orm_argParser=orm.setupOptions()
dao_argParser=dao.setupOptions()
service_argParser=service.setupOptions()
util_argParser=util.setupOptions()
model_argParser=model.setupOptions()

global argParser
argParser=argparse.ArgumentParser(parents=[orm_argParser, dao_argParser, service_argParser, util_argParser,model_argParser])

argParser.add_argument("--config","-c" ,  default="", help="path to configuration file" )
argParser.add_argument("--DAOImplementation", default="", help="Implementation of how to access AFS-Cell" )
argParser.add_argument("--DAO_SPOOL_PARENTDIR", default="", help="If using 'childprocs'-DAO,  use spool dir under this path")
argParser.add_argument("--globalLogLevel", default="", help="global python Loglevel")
argParser.add_argument("--CELL_NAME", default="", help="Default Cell")
argParser.add_argument("--KRB5_PRINC",  default="", help="Kerberos5 Principal to use")
argParser.add_argument("--KRB5_REALM",  default="", help="Kerberos5 REALM to use")
argParser.add_argument("--ignoreIPList",  default=[],action="append",  help="list of IPs to ignore for active polling. May be user more than once. Useful for multi-homed servers and complex network-topologies")
argParser.add_argument("--hostmap",  default=[],action="append",  help="hostname,IP-pairs to override complex DNS-setups with aliases.")

# a Namespace Object to be created from argParser
global defaultConfig
defaultConfig=None

# 
global DbSessionFactory
DbSessionFactory = None

#
# __all__ of submodules created by
# ls *.py | grep -v init| sed 's/.py//'| awk 'BEGIN{printf("__all__=[")} {printf("\"%s\",",$NF)} END{print "]"}' >> __init__.py

