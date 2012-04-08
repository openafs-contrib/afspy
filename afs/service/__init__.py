# Init 
__all__=["AuthService","BaseService","CellService","FsService","PtService","QueryVol","VolService",]

def setupOptions():   
        import argparse
        argParser=argparse.ArgumentParser(add_help=False)
        argParser.add_argument("--LogLevel_Service", default="", help="loglevel fo all serivces")
        for d in __all__ :
            argParser.add_argument("--LogLevel_%s" %d , default="", help="loglevel of class %s" % (d))
        return argParser
