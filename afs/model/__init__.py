# Init 
__all__=["BaseModel","BNode","Bos","Cell","Partition","PTDb","QueryCache","Server","Token","VLDb","VolumeExtra","VolumeGroup","VolumeOSD","Volume",]

def setupOptions():       
    """
    add logging options to cmd-line,
    but surpress them, so that they don't clobber up the help-messages
    """
    import argparse
    argParser=argparse.ArgumentParser(add_help=False)
    argParser.add_argument("--LogLevel_Model", default="", help=argparse.SUPPRESS )
    return argParser
