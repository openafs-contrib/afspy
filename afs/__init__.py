"""
The module afs provides high-level acess to openAFS.
It mostly deals with the server-side (volumes).
A database can be used as transparent cache towards the live system.
"""
__all__ = ["service"]


#
# internal usages
#

from afs.orm import setup_options as orm_setup_options
from afs.dao import setup_options as dao_setup_options
from afs.service import setup_options as service_setup_options
from afs.util import setup_options as util_setup_options
from afs.model import setup_options as model_setup_options
import argparse 


#
# external usage 
#

from afs.service import *
from afs.util.AFSConfig import parse_configs

# define and setup cmdline argument parser here
# so that it can be used in all linked-in modules

ARGPARSER = argparse.ArgumentParser(\
   parents=[orm_setup_options(), dao_setup_options(), \
       service_setup_options(), util_setup_options(), \
       model_setup_options()], \
   epilog="For more options, see documentation and example config-files")

ARGPARSER.add_argument("--config","-c" , default = "", \
    help = "path to afspy-configuration file" )
ARGPARSER.add_argument("--cell", default = "", \
    help = "default afs-cell")
ARGPARSER.add_argument("--globalLogLevel", default = "", \
    help = argparse.SUPPRESS)
ARGPARSER.add_argument("--ignoreIP",  default = [], action = "append", \
    help = argparse.SUPPRESS)
ARGPARSER.add_argument("--hostmap",  default = [], action = "append", \
    help = argparse.SUPPRESS)
ARGPARSER.add_argument("--binconfig", default = "", \
    help = argparse.SUPPRESS )

# a Namespace Object to be created from __argparser__
CONFIG = None

# factory to create SQLAlchemy Sessions
DB_SESSION_FACTORY = None

# dict containing lookup_util objects for different AFS-Cells
LOOKUP_UTIL = {}
