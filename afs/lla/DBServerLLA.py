from afs.lla.BaseLLA import BaseLLA, exec_wrapper
import DBServerLLAParse as PM
from afs.util import misc
from afs.model import DBServer

class DBServerLLA(BaseLLA) :
    """
    low level access to the FileServer/VolServer pair
    """

    def __init__(self) :
        BaseLLA.__init__(self)
        return
