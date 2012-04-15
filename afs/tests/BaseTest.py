import sys, os,argparse
from ConfigParser import ConfigParser

from afs.util.AfsConfig import parseDefaultConfig
import afs


class basicTestSetup :
    """
    class to read in Test.cfg 
    and set up the general options
    """
    
    def setUp(self):
        self.TestCfg=ConfigParser()
        self.TestCfg.read(afs.defaultConfig.setup)
        self.Cell=self.TestCfg.get("general", "Cell")
        afs.defaultConfig.AFSCell=self.Cell
        self.User=self.TestCfg.get("general", "User")
        self.Pass=self.TestCfg.get("general", "Pass")
        self.minUbikDBVersion=self.TestCfg.get("general","minUbikDBVersion")
        if afs.defaultConfig.DB_CACHE :
            from sqlalchemy.orm import sessionmaker
            self.DbSession= sessionmaker(bind=afs.defaultConfig.DB_ENGINE)
        return
    


class TestDataBaseSetup :
    
    def __init__(self):
        
        return
        
class TestDataBaseTearDown :
    
    def __init__(self):
        return

def parseCMDLine():
    myParser=argparse.ArgumentParser(parents=[afs.argParser], add_help=False)
    myParser.add_argument("--setup", default="./Test.cfg", help="path to Testconfig")
    parseDefaultConfig(myParser)
    if not os.path.exists(afs.defaultConfig.setup) :
        sys.stderr.write("Test setup file %s does not exist.\n" %afs.defaultConfig.setup)
        sys.exit(2)
    return

