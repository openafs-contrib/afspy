from afs.exceptions.AfsError import AfsError

def getDBServList(rc,output,outerr,parseParamList,Logger) :
    if rc :
        raise AfsError
    # parse "This workstation belongs to cell 'beolink.org'"
    DBServers = []
    inAnswerSection=False
    for line in output :
        if not inAnswerSection :
            if line == ";; ANSWER SECTION:" :
                inAnswerSection=True
            continue
        if line[:3] == ";; " : # out of ANSWER SECTION
             break
        if line[:2] == ";;" : continue
        srv=line.split()[-1:][0]
        # remove trailing dot, not required and may cause confusion
        if srv[len(srv)-1] == "." : srv=srv[:len(srv)-1]
        DBServers.append(srv)
    return DBServers
