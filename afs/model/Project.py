"""
Declares model object of  a project
"""
from afs.model.BaseModel import BaseModel

class Project(BaseModel):
    """
    Model object of  a Project :
    A project is a group of Volumes defined by the Volume names
    and size.
    A project then defines other attributes such as  (geographical) location,
    contact person, owner(organisation), on which server partition-pairs
    the volumes should reside.
    """

    ## name
    name = ""
    ## list of regexes, json encoded
    volname_regex_js = "[]"
    volname_regex = []
    ## list of additional Volumenames, json encoded
    additional_volnames_js = "[]"
    additional_volnames = []
    ## list of excluded Volumenames , json encoded
    excluded_volnames_js = "[]"
    excluded_volnames = []
    ## minimum Size for a Volume
    min_size_kb = -1
    ## maximum Size for a volume
    max_size_kb = -1
    ## specificity can be used for project hierachies
    specificity = 0
    ## contact
    contact = ""
    ## owner
    owner = ""
    ## list of locationIDs for RW-Volumes, json encoded
    rw_locations_js = "[]"
    rw_locations = []
    ## list of locationIDs for RO-Volumes, json encoded
    ro_locations_js = "[]"
    ro_locations = []
    ## list of "server-uuid,partition" pairs for RW-Volumes, json encoded
    rw_serverparts_js = "[]"
    rw_serverparts = []
    ## list of "server-uuid,partition" pairs for RO-Volumes, json encoded
    ro_serverparts_js = ""
    ro_serverparts = []
    ## free form description
    description = ""
    ## minimum number of RO-replicas
    num_min_ro = 1

    def __init__(self) :
        """
        initialize an empty object
        """
        BaseModel.__init__(self)
