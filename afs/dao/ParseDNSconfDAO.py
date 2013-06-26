"""
parsing methods for DMSConf DAO.
"""
from afs.exceptions.AfsError import AfsError

def get_db_serverlist(ret, output, outerr, parse_parameterlist, logger) :
    """parse output and return list of hostnames of the database-servers"""
    if ret :
        raise AfsError("failed to query DNS for db servers. outerr=%s" % outerr)
    # parse "This workstation belongs to cell 'beolink.org'"
    db_servers = []
    in_answer_section = False
    for line in output :
        if not in_answer_section :
            if line == ";; ANSWER SECTION:" :
                in_answer_section = True
            continue
        if line[:3] == ";; " : # out of ANSWER SECTION
            break
        if line[:2] == ";;" : 
            continue
        srv = line.split()[-1:][0]
        # remove trailing dot, not required and may cause confusion
        if srv[len(srv)-1] == "." : 
            srv = srv[:len(srv)-1]
        db_servers.append(srv)
        logger.debug("Returning: %s" % db_servers)
    return db_servers
