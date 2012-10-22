import re

def parse_getVersionandBuildDate(rc,output,outerr,parseParamList,Logger):
    RXVerRegEx=re.compile("AFS version:  OpenAFS(.*)built (.*)")
    if len(output) != 2 :
        version="Not readable."
        return ""
    else :
        M=RXVerRegEx.match(output[1])
        if not M :
            version=""
            builddate=""
        else :
            version=M.groups()[0].strip()
            builddate=M.groups()[1].strip()
    return version, builddate
