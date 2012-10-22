from afs.dao.BaseDAO import BaseDAO,execwrapper
import PTDbDAO_parse as PM

class PTDbDAO(BaseDAO) :
    """
    Provides low-level acces to the Protection Database
    """
    def __init__(self) :
        BaseDAO.__init__(self)
        return
