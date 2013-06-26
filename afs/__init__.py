"""
The module afs provides high- and low-level acess to openAFS.
It mostly deals with the server-side (volumes).
A database can be used as transparent cache towards the live system.
"""
__all__ = ["dao", "exceptions", "model", "orm", "service", "util"]
import afs.orm as orm
import afs.exceptions as exceptions
import afs.dao as dao
import afs.service as service
import afs.util as util
import afs.model as model
import argparse

# define and setup cmdline argument parser here
# so that it can be used in all linked-in modules

ARGPARSER = argparse.ArgumentParser(\
   parents=[orm.setup_options(), dao.setup_options(), \
       service.setup_options(), util.setup_options(), \
       model.setup_options()], \
   epilog="For more options, see documentation and example config-files")

ARGPARSER.add_argument("--config","-c" , default = "", \
    help = "path to afspy-configuration file" )
ARGPARSER.add_argument("--cell", default = "", \
    help = "default afs-cell")
ARGPARSER.add_argument("--globalLogLevel", default = "", \
    help = argparse.SUPPRESS)
ARGPARSER.add_argument("--DAOImplementation", default = "", \
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
