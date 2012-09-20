import re
from afs.dao.BaseDAO import BaseDAO
import afs.dao.bin
from afs.exceptions.AfsError import AfsError



class RxDAO(BaseDAO) :
    """
    Direct Access to RX Debug
    """
    def __init__(self) :
        BaseDAO.__init__(self)
        return

    def getVersion(self,servername,port) :
        CmdList=[afs.dao.bin.RXDEBUGBIN,"-server", "%s"  % servername, "-port", "%s" % port,  "-v"]
        rc,output,outerr=self.execute(CmdList)
        if rc :
            raise AfsError(rc)
        if len(output) != 2 :
            raise AfsError(-1)
        RX=re.compile("AFS version:\W+(.*) built.*")
        MObj=RX.match(output[1])
        if MObj :
            return MObj.groups()[0] 
        else :
            return None
 
