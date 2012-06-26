from datetime import datetime
from afs.model.BaseModel import BaseModel


class Location(BaseModel):
    """
    Model object of a location of a server
    """
       
    def __init__(self, name="", building="", postcode="",street="",city="",state="",country="",contact="",description="",GPS=""):
        """
        initialize an empty object
        """
        ## DB - ID
        self.id = None
        ## canonicalized partition name e.g "ad" for "/vicepad"
        self.name   = name
        ## building
        self.building = building
        ## postcode
        self.postcode = postcode
        ## street + number
        self.street = street
        ## city 
        self.city = city
        ## state
        self.state = state
        ## country
        self.country = country
        ## GPS data
        self.GPS = GPS
        ## contact
        self.contact = contact
        ## description
        self.description = description
        self.cdate   = datetime.now()
        self.udate   = datetime.now()
        ## list of attributes not to put into the DB
        self.ignAttrList= []
