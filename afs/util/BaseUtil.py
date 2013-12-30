"""
Base class for all Util classes
"""

import logging
import afs
from afs.util.Executor import Executor

class BaseUtil(Executor) :
    """
    The mother of all Utils
    """
    
    def __init__(self) :
        """initializes logger and sets implementation"""

        Executor.__init__(self)
        class_loglevel = getattr(afs.CONFIG,"loglevel_%s" \
            % self.__class__.__name__, "").upper()
        numeric_loglevel = getattr(logging, class_loglevel, 0)
        self.logger = logging.getLogger("afs.dao.%s" % self.__class__.__name__)
        self.logger.setLevel(numeric_loglevel)
        self.logger.debug("initializing %s-Object" % (self.__class__.__name__))
        return
        
