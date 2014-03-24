"""
collection of services for the different entities within
an AFS-cell.
A service provides methods to create objects from the live 
AFS-cell or the database cache 
"""
__all__ = [ "BaseService",  "BosService", "CellService", "DBsService", \
  "FSService", "ProjectService", "PTDBService", "VLDBService", "VolumeService"
]

def setup_options():   
    """
    add logging options to cmd-line,
    but surpress them, so that they don't clobber up the help-messages
    """
    import argparse
    my_argparser = argparse.ArgumentParser(add_help = False)
    my_argparser.add_argument("--LogLevel_Service", default = "", \
        help = argparse.SUPPRESS)
    for service in __all__ :
        my_argparser.add_argument("--LogLevel_%s" % service, \
            default = "", help = argparse.SUPPRESS)
    return my_argparser
