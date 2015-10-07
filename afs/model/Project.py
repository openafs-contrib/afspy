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
        initialize an empty object.
        The app-representation of compley attributes must be initialized to its type here.
        """

        # declare db-internal attributes
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
        ## Projects are organized in trees. db_id of a parent project.
        ## -1 means that this is the root project
        self.parent_db_id = -1
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
        ## list of "server-uuid, partition" pairs for RO-Volumes, json encoded
        self.ro_serverparts_js = "[]"
        self.ro_serverparts = []
        ## free form description
        self.description = ""
        ## minimum number of RO-replicas
        self.num_min_ro = 1
        ## list of attributes not to put into the DB
        self.unmapped_attributes_list =  []
