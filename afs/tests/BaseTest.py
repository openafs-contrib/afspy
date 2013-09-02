"""
Base class for other unit-test.
Deals with reading the configuration
and setting up some variables.
"""
import sys, os, argparse
from ConfigParser import ConfigParser

from afs.util.AFSConfig import parse_configs
import afs


class BasicTestSetup :
    """
    super class for all unit-tests here.  
    """

<<<<<<< Updated upstream
    def setUp(self) :
=======
    def __init__(self) :
>>>>>>> Stashed changes
        """parse test.configuration file"""
        self.test_config = ConfigParser()
        self.test_config.read(afs.CONFIG.setup)
        self.afs_cell = self.test_config.get("general", "cell")
        self.all_dbservers = self.test_config.get("general", \
            "allDBServs").split(",")
        self.all_dbservers.sort()
        afs.CONFIG.afs_cell = self.afs_cell
        self.user = self.test_config.get("general", "user")
        self.password = self.test_config.get("general", "password")
        self.min_ubikdb_version = self.test_config.get(\
            "general", "min_ubikdb_version")
        if afs.CONFIG.DB_CACHE :
            from sqlalchemy.orm import sessionmaker
            self.db_session = sessionmaker(\
                bind = afs.CONFIG.DB_ENGINE)
        return

def parse_commandline():
    """
    general function for parsing command line args given to the unit-test.
    """
    my_parser = argparse.ArgumentParser(parents = [afs.ARGPARSER], \
        add_help = False,epilog = afs.ARGPARSER.epilog)
    my_parser.add_argument("--setup", default="./Test.cfg", \
        help="path to Testconfig")
    parse_configs(my_parser)
    if not os.path.exists(afs.CONFIG.setup) :
        sys.stderr.write("Test setup file %s does not exist.\n" % \
            afs.CONFIG.setup)
        sys.exit(2)
    return

