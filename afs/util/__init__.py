# Init 

def setupOptions():   
        import argparse
        argParser=argparse.ArgumentParser(add_help=False)
        for d in ["util","DBManager"]:
            argParser.add_argument("--LogLevel_%s" %d , default="", help="loglevel of class %s" % (d))
        return argParser
