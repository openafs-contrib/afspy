# Init 
__all__=["DbMapper",]

def setupOptions():   
    import argparse
    argParser=argparse.ArgumentParser(add_help=False)
    # setup DB_CACHE options
    argParser.add_argument("--DB_CACHE",  default="", help="use DB cache")
    argParser.add_argument("--DB_SID" , default="", help="Database name or for sqlite path to DB file")
    argParser.add_argument("--DB_TYPE" , default="", help="Type of DB. [mysql|sqlite]")
    # mysql options
    argParser.add_argument("--DB_HOST", default="", help="Database host")
    argParser.add_argument("--DB_PORT", default="", help="Database port")
    argParser.add_argument("--DB_USER", default="", help="Database user")
    argParser.add_argument("--DB_PASSWD" , default="", help="Database password")
    argParser.add_argument("--DB_FLUSH", default="", help="Max Number of elements in Buffer")
    # for logging sqlalchmy
    argParser.add_argument("--LogLevel_sqlalchemy", default="", help="loglevel of module sqlalchemy")
    argParser.add_argument("--LogLevel_DB_CACHE", default="", help="loglevel of DB_CACHE")
    return argParser


