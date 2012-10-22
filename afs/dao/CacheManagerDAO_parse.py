from afs.exceptions.CMError import CMError

def parse_newCellAlias(rc,output,outerr,parseParamList,Logger) :
    if rc :
        raise CMError("error: %s" % outerr)
    return

def parse_getWsCell(rc,output,outerr,parseParamList,Logger) :
    if rc :
        raise CMError("error: %s" % outerr)

    # parse "This workstation belongs to cell 'beolink.org'"
    # remove ' 
    cellname=output[0].split()[5].replace("'","")
    return cellname


def parse_flushall(rc,output,outerr,parseParamList,Logger) :
    if rc :
        raise CMError("error: %s" % outerr)
    return

def parse_flushvolume(rc,output,outerr,parseParamList,Logger) :
    if rc :
        raise CMError("error: %s" % outerr)
    return

def parse_flushmount(rc,output,outerr,parseParamList,Logger) :
    if rc :
        raise CMError("error: %s" % outerr)
    return

def parse_flush(rc,output,outerr,parseParamList,Logger) :
    if rc :
        raise CMError("error: %s" % outerr)
    return


def parse_getCellAliases(rc,output,outerr,parseParamList,Logger) :
    if rc :
        raise CMError("error: %s" % outerr)
    return
