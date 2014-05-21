from afs.lla.BaseLLA import BaseLLA, exec_wrapper
import CellLLAParse as PM
from afs.model import Cell

class CellLLA(BaseLLA):
    """
    summary class about a cell
    """
    def __init__(self) :
        BaseLLA.__init__(self)
        return
