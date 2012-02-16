# Init 

__all__=["dao","exceptions","factory","model","orm","service","util"]

# setup options for command-line and configuration files

import util.AfsConfig
global defaultConfig
defaultConfig=util.AfsConfig.AfsConfig()
util.AfsConfig.setupOptions()

global DbSessionFactory
DbSessionFactory = None

#
# __all__ of submodules created by
# ls *.py | grep -v init| sed 's/.py//'| awk 'BEGIN{printf("__all__=[")} {printf("\"%s\",",$NF)} END{print "]"}' >> __init__.py

