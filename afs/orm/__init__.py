# Init 
__all__=["DbMapper",]

def setupOptions():   
    """
    add logging options to cmd-line,
    but surpress them, so that they don't clobber up the help-messages
    """
    import argparse
    argParser=argparse.ArgumentParser(add_help=False)
    # setup DB_CACHE options
    argParser.add_argument("--DB_CACHE",  default="", help=argparse.SUPPRESS)
    argParser.add_argument("--DB_SID" , default="", help=argparse.SUPPRESS)
    argParser.add_argument("--DB_TYPE" , default="", help=argparse.SUPPRESS)
    # mysql options
    argParser.add_argument("--DB_HOST", default="", help=argparse.SUPPRESS)
    argParser.add_argument("--DB_PORT", default="", help=argparse.SUPPRESS)
    argParser.add_argument("--DB_USER", default="", help=argparse.SUPPRESS)
    argParser.add_argument("--DB_PASSWD" , default="", help=argparse.SUPPRESS)
    argParser.add_argument("--DB_FLUSH", default="", help=argparse.SUPPRESS)
    # for logging, but don't show up in --help
    argParser.add_argument("--LogLevel_sqlalchemy", default="", help=argparse.SUPPRESS)
    argParser.add_argument("--LogLevel_DB_CACHE", default="", help=argparse.SUPPRESS)
    return argParser


