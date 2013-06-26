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

    def __init__(self) :
        """
        initialize an empty object
        """
        BaseModel.__init__(self)

        ## name
        self.name = ""
        ## list of regexes, json encoded
        self.volname_regex_js = "[]"
        self.volname_regex = []
        ## list of additional Volumenames, json encoded
        self.additional_volnames_js = "[]"
        self.additional_volnames = []
        ## list of excluded Volumenames , json encoded
        self.excluded_volnames_js = "[]"
        self.excluded_volnames = []
        ## minimum Size for a Volume
        self.min_size_kb = -1
        ## maximum Size for a volume
        self.max_size_kb = -1
        ## specificity can be used for project hierachies
        self.specificity = 0
        ## contact
        self.contact = ""
        ## owner
        self.owner = ""
        ## list of locationIDs for RW-Volumes, json encoded
        self.rw_locations_js = "[]"
        self.rw_locations = []
        ## list of locationIDs for RO-Volumes, json encoded
        self.ro_locations_js = "[]"
        self.ro_locations = []
        ## list of "server-uuid,partition" pairs for RW-Volumes, json encoded
        self.rw_serverparts_js = "[]"
        self.rw_serverparts = []
        ## list of "server-uuid,partition" pairs for RO-Volumes, json encoded
        self.ro_serverparts_js = ""
        self.ro_serverparts = []
        ## free form description
        self.description = ""
        ## minimum number of RO-replicas
        self.min_num_ro = 1
