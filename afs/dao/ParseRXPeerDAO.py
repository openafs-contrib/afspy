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
            build_date=""
        else :
            version=M.groups()[0].strip()
            build_date=M.groups()[1].strip()
    return version, build_date
