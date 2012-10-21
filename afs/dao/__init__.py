# Init 
__all__=["BNodeDAO","CacheManagerDAO","FileServerDAO","FileSystemDAO","OsdDbDAO","PTDbDAO","RxDAO","RxOsdDAO","RXPeerDAO","UbikPeerDAO","VLDbDAO","VolumeDAO","OSDVolumeDAO","OSDFileServerDAO"]

def setupOptions():   
    """
    add logging options to cmd-line,
    but surpress them, so that they don't clobber up the help-messages
    """
    import argparse
    argParser=argparse.ArgumentParser(add_help=False)
    argParser.add_argument("--LogLevel_DAO", default="", help=argparse.SUPPRESS)
    for d in __all__ :
        argParser.add_argument("--LogLevel_%s" %d , default="", help=argparse.SUPPRESS)
    return argParser
