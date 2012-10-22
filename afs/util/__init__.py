# Init 

def setupOptions():   
    """
    add logging options to cmd-line,
    but surpress them, so that they don't clobber up the help-messages
    """
    import argparse
    argParser=argparse.ArgumentParser(add_help=False)
    for d in ["util","DBManager","LookupUtil"]:
        argParser.add_argument("--LogLevel_%s" %d , default="", help=argparse.SUPPRESS)
    return argParser
