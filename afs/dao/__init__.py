# Init 
__all__=["BNodeDAO","CacheManagerDAO","FileServerDAO","FileSystemDAO","krb5DAO","OsdDbDAO","PAGDAO","PTDbDAO","RxDAO","RxOsdDAO","RXPeerDAO","UbikPeerDAO","VLDbDAO","VolumeDAO","OSDVolumeDAO","OSDFileServerDAO"]

def setupOptions():   
        import argparse
        argParser=argparse.ArgumentParser(add_help=False)
        argParser.add_argument("--LogLevel_DAO", default="", help="loglevel fo all daos")
        for d in __all__ :
            argParser.add_argument("--LogLevel_%s" %d , default="", help="loglevel of class %s" % (d))
        return argParser
