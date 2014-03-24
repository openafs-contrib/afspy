from afs.dao.BaseDAO import BaseDAO
from afs.util.Executor import exec_wrapper
import CellDAOParse as PM
from afs.model import Cell

class CellDAO(BaseDAO):
    """
    summary class about a cell
    """
    def __init__(self) :
        BaseDAO.__init__(self)
        return
