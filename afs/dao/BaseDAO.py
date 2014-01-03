"""
base class for all DAOs :
initializes logging.
and Executor-class
deals with actual execution of commands
"""
from afs.util.Executor import Executor
import afs
import inspect
import logging

class BaseDAO(Executor) :
    """
    The mother of all DAOs
    """
    
    def __init__(self) :
        """initializes logger and sets implementation"""

        afs.util.Executor.Executor.__init__(self)
        class_loglevel = getattr(afs.CONFIG,"LogLevel_%s" \
            % self.__class__.__name__, "").upper()
        numeric_loglevel = getattr(logging, class_loglevel, 0)
        self.logger = logging.getLogger("afs.dao.%s" % self.__class__.__name__)
        self.logger.setLevel(numeric_loglevel)
        self.logger.debug("initializing %s-Object" % (self.__class__.__name__))
        return
        
