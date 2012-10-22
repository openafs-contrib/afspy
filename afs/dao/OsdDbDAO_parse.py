import re,string,os,sys
from afs.exceptions.OsdDbError import OsdDbError

def getStatistics(rc,output,outerr,parseParamList,Logger) :
    if rc:
        raise OsdDbError("Error", outerr)

    statDict={}
    return statDict
