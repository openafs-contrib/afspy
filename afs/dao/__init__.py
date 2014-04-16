""" 
low-level interface
used for filling up objects from a live afs-cell
and other direct access of the afs-cell
"""

# Init 
__all__ = ["BosServerDAO", "CacheManagerDAO", "FileServerDAO", \
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
    my_argparser.add_argument("--SpoolDirBase", default = "/tmp/afspy", \
    help = argparse.SUPPRESS)
    my_argparser.add_argument("--AsyncTimeout", default = 60, type=int, \
        help = argparse.SUPPRESS)
    return my_argparser
