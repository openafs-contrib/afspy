# Init 
__all__=["AuthService","BaseService","CellService","FsService","PtService","ProjectService","QueryVol","VolService","OSDVolService","OSDFsService","OSDCellService","DBsService","BsService"]

def setupOptions():   
    """
    add logging options to cmd-line,
    but surpress them, so that they don't clobber up the help-messages
    """
    import argparse
    argParser=argparse.ArgumentParser(add_help=False)
    argParser.add_argument("--LogLevel_Service", default="", help=argparse.SUPPRESS)
    for d in __all__ :
        argParser.add_argument("--LogLevel_%s" %d , default="", help=argparse.SUPPRESS)
    return argParser
