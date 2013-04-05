"""
The module afs provides high- and low-level acess to openAFS.
It mostly deals with the server-side (volumes).
A database can be used as transparent cache towards the live system.
"""
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
argParser=argparse.ArgumentParser(parents=[orm_argParser, dao_argParser, service_argParser, util_argParser,model_argParser],epilog="For more options, see documentation and example config-files")

argParser.add_argument("--config","-c" ,  default="", help="path to configuration file" )
argParser.add_argument("--CELL_NAME", default="", help="Default Cell")
argParser.add_argument("--globalLogLevel", default="", help=argparse.SUPPRESS)
argParser.add_argument("--DAOImplementation", default="", help=argparse.SUPPRESS )
argParser.add_argument("--DAO_SPOOL_PARENTDIR", default="", help=argparse.SUPPRESS)
argParser.add_argument("--ignoreIP",  default=[],action="append",  help=argparse.SUPPRESS)
argParser.add_argument("--hostmap",  default=[],action="append",  help=argparse.SUPPRESS)
argParser.add_argument("--binconfig", default="", help=argparse.SUPPRESS )

# a Namespace Object to be created from argParser
global defaultConfig
defaultConfig=None

# 
#
global DbSessionFactory
DbSessionFactory = None

#
#
global LookupUtil
LookupUtil={}

#
# __all__ of submodules created by
# ls *.py | grep -v init| sed 's/.py//'| awk 'BEGIN{printf("__all__=[")} {printf("\"%s\",",$NF)} END{print "]"}' >> __init__.py

