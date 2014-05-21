from afs.lla.BaseLLA import BaseLLA
from afs.util.Executor import exec_wrapper
import CellLLAParse as PM
from afs.model import Cell

class CellLLA(BaseLLA):
    """
    summary class about a cell
    """
    def __init__(self) :
        BaseLLA.__init__(self)
        return
