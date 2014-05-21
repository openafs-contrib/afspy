from afs.lla.BaseLLA import BaseLLA
from afs.util.Executor import exec_wrapper
import PTDBLLAParse as PM
from afs.model import PTDB

class PTDBLLA(BaseLLA) :
    """
    Provides low-level acces to the Protection Database
    """
    def __init__(self) :
        BaseLLA.__init__(self)
        return
