"""
module dealing with the object-realational mapping
"""
__all__ = ["DbMapper", ]

from afs.orm import DBMapper

def setup_options():   
    """
    add logging options to cmd-line,
    but surpress them, so that they don't clobber up the help-messages
    """
    import argparse
    my_argparser = argparse.ArgumentParser(add_help = False)
    # setup DB_CACHE options
    my_argparser.add_argument("--DB_CACHE",  default = "", \
        help = argparse.SUPPRESS)
    my_argparser.add_argument("--DB_SID" , default = "", \
         help = argparse.SUPPRESS)
    my_argparser.add_argument("--DB_TYPE" , default = "", \
        help = argparse.SUPPRESS)
    # mysql options
    my_argparser.add_argument("--DB_HOST", default = "", \
        help = argparse.SUPPRESS)
    my_argparser.add_argument("--DB_PORT", default = "", \
        help = argparse.SUPPRESS)
    my_argparser.add_argument("--DB_USER", default = "", \
        help = argparse.SUPPRESS)
    my_argparser.add_argument("--DB_PASSWD" , default = "", \
        help = argparse.SUPPRESS)
    my_argparser.add_argument("--DB_FLUSH", default = "", \
        help = argparse.SUPPRESS)
    # for logging, but don't show up in --help
    my_argparser.add_argument("--LogLevel_sqlalchemy", default = "", \
        help = argparse.SUPPRESS)
    my_argparser.add_argument("--LogLevel_DB_CACHE", default = "", \
        help = argparse.SUPPRESS)
    return my_argparser

