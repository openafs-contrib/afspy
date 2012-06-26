# Init 
__all__=["BaseModel","BNode","Bos","Cell","Partition","PTDb","QueryCache","Server","Token","VLDb","VolumeExtra","VolumeGroup","VolumeOSD","Volume",]

def setupOptions():   
        import argparse
        argParser=argparse.ArgumentParser(add_help=False)
        argParser.add_argument("--LogLevel_Model", default="", help="loglevel of model object manipulations" )
        return argParser
