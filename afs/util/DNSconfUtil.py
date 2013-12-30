"""
get configuration about AFS-cell from DNS
"""
from afs.util.Executor import exec_wrapper
import DNSconfDAOParse as PM
from BaseUtil import BaseUtil

class DNSconfUtil(BaseUtil) :
    """
    get Cellinformation from DNS Records
    """

    def __init__(self) :
        BaseUtil.__init__(self)
        return

    @exec_wrapper
    def get_db_serverlist(self, cellinfo, _cfg = None) :
        """
        Returns the dbservers from AFSDB records
        """
        cmd_list = [_cfg.binaries["dig"], "AFSDB", _cfg.cell]
        return cmd_list, PM.get_db_serverlist
