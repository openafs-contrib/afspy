import re,string,os,sys
import afs.dao.bin

from afs.exceptions.PtError import PtError
from afs.dao.BaseDAO import BaseDAO

class PTDbDAO(BaseDAO) :
    """
    Provides low-level acces to the Protection Database
    """
    def __init__(self) :
        BaseDAO.__init__(self)
        return
