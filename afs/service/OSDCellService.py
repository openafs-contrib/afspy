import socket,sys

from afs.exceptions.AfsError import AfsError
from afs.model.Cell import Cell
from afs.model.ExtendedPartitionAttributes import ExtPartAttr
from afs.service.BaseService import BaseService
from afs.service.CellService import CellService
from afs.service.FsService import FsService
from afs.service.ProjectService import ProjectService
from afs.util import afsutil


class OSDCellService(CellService):
    """
    Provides Service about a Cell global information.
    The cellname is set in the configuration passed to constructor.
    Thus one instance works only for cell.
    """
    def __init__(self, conf=None):
        BaseService.__init__(self, conf, DAOList=["osdfs", "bnode","vl", "vol", "rx", "ubik", "dns"])
        self.FS=FsService()
        self.PS=ProjectService()
        return

    def getRXOSDServers(self) :
        RXOSDServers = []
        return RXOSDServers
