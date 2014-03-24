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


def get_historic(obj) :
    """
    return a historic object from given model object.
    Ths historic object is like the model object, but mapped to another table
    """
    import copy
    import Historic
    from BaseModel import BaseModel

    base_model_attrs = dir(BaseModel())
    historic_object = eval("Historic.historic_%s()\n" % (obj.__class__.__name__))
    model_attributes = dir(obj)
    for attr in model_attributes :
        if attr[0] == "_" : continue
        if attr in base_model_attrs : 
            if not attr.startswith("db_") :
                continue
        if attr == obj : continue
        if attr == "db_id" :
            setattr(historic_object, "real_db_id", eval("copy.deepcopy(obj.%s)" % attr))
            continue
        if not attr in obj.unmapped_attributes_list : 
            setattr(historic_object, attr, eval("copy.deepcopy(obj.%s)" % attr))
    return historic_object


# __all__ created with 
# ls afs/model/  |grep \.py\$ |grep -v __init__ | sort | \
# awk 'BEGIN {printf("__all__ = [")} {printf("\"%s\", ",$1)} \
# END {printf("]\n")}'
