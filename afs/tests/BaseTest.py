"""
Base class for other unit-test.
Deals with reading the configuration
and setting up some variables.
"""
import sys
import os
import  argparse
import inspect
from ConfigParser import ConfigParser

from afs.util.AFSConfig import parse_configs
import afs

class BasicTestSetup :
    """
    super class for all unit-tests here.  
    """

    def __init__(self, tested_class, ignore_methods = [], ignore_classes = [], multi_tests = {}) :
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
        self.tested_class = tested_class
        # the tested class can be inherit some other class,
        # whose methods should be ignored. e.g. BaseLLA
        self.ignore_classes = ignore_classes
        self.ignore_methods = ignore_methods
        self.multi_tests = multi_tests
        self.destructive = afs.CONFIG.destructive
        return

    def test_test_completeness(self) :
        # setup list of test_methods 
        self.test_methods = []
        for name, impl in inspect.getmembers(self, predicate = inspect.ismethod) :
            if name.startswith("test_") :
                self.test_methods.append(name[5:])
        self.test_methods.remove("test_completeness")
        # setup list of to be tested methods in class 
        self.to_be_tested_methods = []
        for name, impl in inspect.getmembers(self.tested_class, predicate = inspect.ismethod) :
            self.to_be_tested_methods.append(name)
        # extend ignore_methods by ignore_classes
        for _class in self.ignore_classes :
            for name, impl in inspect.getmembers(_class, predicate = inspect.ismethod) :
                try :
                    self.ignore_methods.append(name)
                except :
                    pass
        #sys.stderr.write("ignore_methods : %s\n" % self.ignore_methods)
        for name in self.ignore_methods :
            try :
                self.to_be_tested_methods.remove(name)
            except :
                pass
        # account for multi-test methods 
        for mt in self.multi_tests :
            self.test_methods += self.multi_tests[mt]
            #sys.stderr.write("%s: %s\n" % (mt,self.multi_tests[mt]))
            #sys.stderr.write("removing %s from %s\n" % (mt,self.test_methods))
            self.test_methods.remove(mt)

        self.test_methods.sort()
        self.to_be_tested_methods.sort()
        #sys.stderr.write("test_methods :%s \n" % self.test_methods)
        #sys.stderr.write("to_be_tested_methods: %s\n" % self.to_be_tested_methods)
        self.assertEqual(self.test_methods, self.to_be_tested_methods)
        return

def parse_commandline():
    """
    general function for parsing command line args given to the unit-test.
    """
    my_parser = argparse.ArgumentParser(parents = [afs.ARGPARSER], \
        add_help = False,epilog = afs.ARGPARSER.epilog)
    my_parser.add_argument("--setup", default="./Test.cfg", \
        help="path to Testconfig")
    my_parser.add_argument("--harmless_auth", dest="enable_harmless_auth_tests", action='store_const', const=True, \
      default=False, help="enable harmless tests requiring authentication")
    my_parser.add_argument("--destructive", dest="enable_destructive_tests", action='store_const', const=True, \
      default=False, help="enable destructive tests")
    my_parser.add_argument("--modifying", dest="enable_modifying_tests", action='store_const', const=True, \
      default=False, help="enable modifying tests")
    my_parser.add_argument("--interrupting", dest="enable_interrupting_tests", action='store_const', const=True, \
      default=False, help="enable interrupting tests")
    parse_configs(my_parser)
    if not os.path.exists(afs.CONFIG.setup) :
        sys.stderr.write("Test setup file %s does not exist.\n" % \
            afs.CONFIG.setup)
        sys.exit(2)
    return

