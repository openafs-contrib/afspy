"""
Declares the mother of all model-objects.
"""
import datetime, json, logging, decimal
from types import StringType, IntType, LongType,  FloatType,  BooleanType,  \
    UnicodeType, ListType, DictType, NoneType

# log-level is set in AfsConfig
LOGGER = logging.getLogger("afs.model")

class BaseModel(object):
    """
    The mother of all model-objects
    """

    def __init__(self) :
        """
        set attributes known to all models
        """
        ## DB - ID
        self.db_id = None
        ## creation date of this db-entry
        self.db_creation_date = datetime.datetime.now()
        ## update date of this db-entry
        self.db_update_date = datetime.datetime.now()
        ## list of attributes not to put into the DB
        ## overwrite in model definition if not empty
        self.unmapped_attributes_list = []
        return 

    def update_app_repr(self) :
        """
        update Complex attributes from their json encoded counterparts
        """
        complex_attrs = {}
        for attr, value in self.__dict__.iteritems() :
            LOGGER.debug("updateAppRepr: attr=%s, value=%s" % (attr, value))
            if attr[-3:] == "_js" :
                if len(value) == 0 :
                    complex_attrs[attr[:-3]] = '""'
                else :
                    complex_attrs[attr[:-3]] = json.loads(value)
                LOGGER.debug("updateAppRepr: complxAttr=%s" %\
                                  (complex_attrs[attr[:-3]]))
        for attr, value in complex_attrs.iteritems() :
            LOGGER.debug("updateAppRepr: setting %s=%s, type=%s" %\
                              (attr, value, type(value)))
            setattr(self, attr, value)
        return

    def update_db_repr(self) :
        """
        update the all attributes holding json represenations of complex attributes
        """
        json_reprs = {}
        LOGGER.debug("in updateDBRepr" )
        for attr, value in self.__dict__.iteritems() :
            ignore = False
            if attr[0] == "_" : continue
            if isinstance(value, datetime.datetime) :
                ignore = True
            elif isinstance(value, decimal.Decimal) :
                ignore = True
            elif type(value) in [ StringType, IntType, LongType, \
            FloatType, BooleanType, NoneType ] :
                ignore = True
            if not ignore :
                LOGGER.debug("attr=%s type(value)=%s" % (attr, type(value)))
                json_reprs["%s_js" % attr] = json.dumps(value)
            else :
                LOGGER.debug("Ignoring attr=%s type(value)=%s" % \
                    (attr, type(value)))
        for attr, value in json_reprs.iteritems() :
            LOGGER.debug("setting json rep %s to '%s'" % (attr, value) )
            setattr(self, attr, value)
        return

    def get_json_repr(self):
        """
        Get a json representation of the model object.
        ignore db and private attributes.
        """
        res = {}
        for attr, value in self. __dict__.iteritems() :
            if attr[0] == "_" : continue
            if attr[-3:] == "_js" : continue
            if isinstance(value, datetime.datetime):
                res[attr] = json.dumps(value.isoformat('-'))
            elif type(value) in [ StringType, IntType, UnicodeType, ListType, \
                DictType, NoneType ] :
                res[attr] = json.dumps(value)
        return res

    def __repr__(self):
        """
        Get a string representation of the model object.
        no python built-ins nor BaseModel stuff
        """
        base_model_attrs = dir(BaseModel())
        repr = "<%s(" % self.__class__.__name__
        model_attributes = dir(self)
        for attr in model_attributes :
            if attr in base_model_attrs : continue
            repr += "%s=%s, " % (attr, eval("self.%s" % attr))
        repr += ")>"
        return repr
