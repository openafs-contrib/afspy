"""
Declares the mother of all model-objects.
"""
import datetime, json, logging, decimal, sys
from types import StringType, IntType, LongType,  FloatType,  BooleanType,  \
    UnicodeType, ListType, DictType, NoneType

# log-level is set in AfsConfig
LOGGER = logging.getLogger("afs.model")

class BaseModel(object):
    """
    The mother of all model-objects
    """

    ## DB - ID
    db_id = None
    ## creation date of this db-entry
    db_creation_date = datetime.datetime.now()
    ## update date of this db-entry
    db_update_date = datetime.datetime.now()
    ## list of attributes not to put into the DB
    ## overwrite in model definition if not empty
    unmapped_attributes_list = []

    def __init__(self) :
        """
        set attributes known to all models
        """
        self.update_app_repr()
        return 

    def update_app_repr(self) :
        """
        update Complex attributes from their json encoded counterparts
        """
        complex_attrs = {}
        for attr, value in self.__dict__.iteritems() :
            LOGGER.debug("update_app_repr: attr=%s, value=%s" % (attr, value))
            if attr[-3:] == "_js" :
                try :
                    if len(value) == 0 :
                        complex_attrs[attr[:-3]] = '""'
                    else :
                        complex_attrs[attr[:-3]] = json.loads(value)
                except:
                    complex_attrs[attr[:-3]] = '""'
                LOGGER.debug("update_app_repr: complex_attr=%s" %\
                                  (complex_attrs[attr[:-3]]))
        for attr, value in complex_attrs.iteritems() :
            LOGGER.debug("update_app_repr: setting %s=%s, type=%s" %\
                              (attr, value, type(value)))
            setattr(self, attr, value)
        return

    def update_db_repr(self) :
        """
        update the all attributes holding json represenations of complex attributes
        """
        json_reprs = {}
        LOGGER.debug("in update_db_repr" )
        for attr, value in self.__dict__.iteritems() :
            LOGGER.debug("update_db_repr: attr=%s, value=%s" % (attr, value))
            ignore = False
            if attr[0] == "_" : continue
            if isinstance(value, datetime.datetime) :
                ignore = True
            elif isinstance(value, decimal.Decimal) :
                ignore = True
            elif type(value) in [ StringType, IntType, LongType, \
            FloatType, BooleanType, NoneType ] :
                ignore = True
            elif attr == "unmapped_attributes_list" or \
            attr in self.unmapped_attributes_list :
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
            if attr in base_model_attrs : 
                if not attr.startswith("db_") :
                    continue
            if attr == self : continue
            if attr in self.unmapped_attributes_list : 
                repr += "(%s=%s,), "  % (attr, eval("self.%s" % attr))
            else :
                repr += "%s=%s, " % (attr, eval("self.%s" % attr))
        repr += ")>"
        return repr

    def __setattr__(self, name, value):
        """
        Raise an exception if attempting to assign to an atribute which does not exist in the model.
        We're not checking if the attribute is an SQLAlchemy-mapped column because we also want it to work with properties etc.
        See http://stackoverflow.com/questions/12032260/ for more details.
        This is activated after the initialization in the models __init__ - method
        """ 
        if name != "_sa_instance_state" and not hasattr(self, name) and not name in self.unmapped_attributes_list :
            raise ValueError("Attribute %s is not a mapped column of object %s" % (name, self))
        super(BaseModel, self).__setattr__(name, value) 
