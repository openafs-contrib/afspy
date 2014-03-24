from afs.dao.BaseDAO import BaseDAO
from afs.util.Executor import exec_wrapper
import DBServerDAOParse as PM
from afs.util import misc
from afs.model import DBServer

class DBServerDAO(BaseDAO) :
    """
    low level access to the FileServer/VolServer pair
    """

    def __init__(self) :
        BaseDAO.__init__(self)
        return
