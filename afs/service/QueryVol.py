class QueryVol(object):
    """
    Query the DB or live data
    """
    limit  = -1
    offset = -1
    field  = "name"
    value  = ""
    order  = ""
    dir    = ""
    
    
    def __init__(self):
        pass
    
    def getQuery(self):
        pass
    
    """
    Retrieve Volume List
    """
    def getVolList(self,volQuery,**kwargs):
        pass
