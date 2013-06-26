from afs.dao.BaseDAO import BaseDAO, exec_wrapper
import ParsePTDBDAO as PM

class PTDBDAO(BaseDAO) :
    """
    Provides low-level acces to the Protection Database
    """
    def __init__(self) :
        BaseDAO.__init__(self)
        return
