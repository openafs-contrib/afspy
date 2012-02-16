import afs.util.options
import socket, string

from afs.util.AfsConfig import AfsConfig
from afs.exceptions.VLDbError import VLDbError
from afs.exceptions.VolError import VolError
from afs.exceptions.ORMError import  ORMError
from afs.model.Server import Server
from afs.model.Partition import Partition
from afs.util import afsutil
from afs.service.BaseService import BaseService
import afs

class PtService(BaseService):
    """
    Provides Service about a Cell global information.
    The cellname is set in the configuration passed to constructor.
    Thus one instance works only for cell, or you
    need to change self._CFG
    """
    def __init__(self,conf=None):
        BaseService.__init__(self, conf, DAOList=["fs",  ])
