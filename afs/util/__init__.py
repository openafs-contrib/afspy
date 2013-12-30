"""
provides utility functions useful for all other submodules
"""

__all__ = ["DNSconfUtil"]

def setup_options():   
    """
    add logging options to cmd-line,
    but surpress them, so that they don't clobber up the help-messages
    """
    import argparse
    my_argparser = argparse.ArgumentParser(add_help = False)
    for submodule in ["util", "DBManager", "LookupUtil"]:
        my_argparser.add_argument("--LogLevel_%s" % submodule, default = "", help = argparse.SUPPRESS)
    return my_argparser
