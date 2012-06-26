import afs.dao.bin
from afs.exceptions.AfsError import AfsError
from afs.dao.BaseDAO import BaseDAO

class DNSconfDAO(BaseDAO):
    """
    get Cellinformation from DNS Records
    """

    def __init__(self) :
        BaseDAO.__init__(self)
        return

    def getDBServList(self,cellname):
        """
        Returns the dbservers from AFSDB records
        """
        CmdList=[afs.dao.bin.DIGBIN , "AFSDB", cellname]
        rc,output,outerr=self.execute(CmdList)
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
