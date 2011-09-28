import sys
import afs.util.options
from afs.util.options import define, options

class AfsConfig(object):

	CONF_FILE = "./afspy.cfg"
	DB_CACHE = False

	def __init__(self,opt=None):
		if opt:
			self.load()
	
	def load(self):
		define("DB_CACHE",  default="False", help="")
		define("CONF_FILE", default=self.CONF_FILE, help="")

		try :
			afs.util.options.parse_config_file(self.CONF_FILE) 
		except afs.util.options.Error :
			print "Error: " , sys.exc_info()[1]
			sys.exit()
		except:
			return       
		
		self.DB_CACHE = eval(options.DB_CACHE)

