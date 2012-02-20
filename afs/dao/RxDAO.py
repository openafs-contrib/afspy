import re,string,os,sys
import afs.dao.bin

from afs.util import afsutil
from afs.dao.BaseDAO import BaseDAO


class RxDAO(BaseDAO) :
    """
    Direct Access to RX Debug
    """
    def __init__(self) :
        BaseDAO.__init__(self)
        return
