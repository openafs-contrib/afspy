"""
dao : direct  access object.
used for filling up objects from a live afs-cell
"""
from afs.dao import BNodeDAO,  CacheManagerDAO, FileServerDAO,  FileSystemDAO, \
    PTDBDAO, RXPeerDAO,  UbikPeerDAO,  VLDBDAO,  VolumeDAO

# Init
__all__ = ["BNodeDAO", "CacheManagerDAO", "FileServerDAO", "FileSystemDAO", \
     "PTDBDAO", "RXPeerDAO", "UbikPeerDAO", "VLDBDAO", "VolumeDAO"]

def setup_options():
    """
    add logging options to cmd-line,
    but surpress them, so that they don't clobber up the help-messages
    """
    import argparse
    my_argparser = argparse.ArgumentParser(add_help = False)
    my_argparser.add_argument("--LogLevel_DAO", default = "", \
        help = argparse.SUPPRESS)
    for submodule in __all__ :
        my_argparser.add_argument("--LogLevel_%s" % submodule, default = "", \
            help = argparse.SUPPRESS)
    return my_argparser
