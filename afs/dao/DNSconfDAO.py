"""
get configuration about AFS-cell from DNS
"""
from afs.dao.BaseDAO import BaseDAO, exec_wrapper
import afs.dao.ParseDNSconfDAO as PM

class DNSconfDAO(BaseDAO):
    """
    get Cellinformation from DNS Records
    """

    def __init__(self) :
        BaseDAO.__init__(self)
        return

    @exec_wrapper
    def get_db_serverlist(self, _cfg = None) :
        """
        Returns the dbservers from AFSDB records
        """
        cmd_list = [_cfg.binaries["dig"], "AFSDB", _cfg.cell]
        return cmd_list, PM.get_db_serverlist
