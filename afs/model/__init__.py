"""
collection of all model objects for entitite within an AFS-cell
"""

__all__ = ["BaseModel.py", "BNode.py", "Bos.py", "BosServer.py", \
"Cell_OSD.py", "Cell.py", "DBServer.py", \
"ExtendedDBServerAttributes.py", "ExtendedFileServerAttributes.py", \
"ExtendedPartitionAttributes_OSD.py", "ExtendedPartitionAttributes.py", \
"ExtendedVolumeAttributes_OSD.py", "ExtendedVolumeAttributes.py", \
"FileServer.py", "Partition.py", "Project.py", "ProjectSpread.py", \
"PTDb.py", "VLDb.py", "Volume.py", ]


def setup_options():       
    """
    add logging options to cmd-line,
    but surpress them, so that they don't clobber up the help-messages
    """
    import argparse
    my_argparser = argparse.ArgumentParser(add_help=False)
    my_argparser.add_argument("--LogLevel_Model", default = "", \
         help = argparse.SUPPRESS )
    return my_argparser

# __all__ created with 
# ls afs/model/  |grep \.py\$ |grep -v __init__ | sort | \
# awk 'BEGIN {printf("__all__ = [")} {printf("\"%s\", ",$1)} \
# END {printf("]\n")}'
