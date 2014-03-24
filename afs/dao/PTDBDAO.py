from afs.dao.BaseDAO import BaseDAO
from afs.util.Executor import exec_wrapper
import PTDBDAOParse as PM
from afs.model import PTDB

class PTDBDAO(BaseDAO) :
    """
    Provides low-level acces to the Protection Database
    """
    def __init__(self) :
        BaseDAO.__init__(self)
        return
