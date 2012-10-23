from afs.exceptions.AfsError import AfsError
from afs.dao.BaseDAO import BaseDAO,execwrapper
import DNSconfDAO_parse as PM

class DNSconfDAO(BaseDAO):
    """
    get Cellinformation from DNS Records
    """

    def __init__(self) :
        BaseDAO.__init__(self)
        return

    @execwrapper
    def getDBServList(self, _cfg=None):
        """
        Returns the dbservers from AFSDB records
        """
        CmdList=[_cfg.binaries["dig"], "AFSDB", _cfg.CELL_NAME]
        return CmdList,PM.getDBServList
