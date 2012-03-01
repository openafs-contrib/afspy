class QueryCache(object):
    
    limit  = None
    offset = None
    sort   = []
    dir    = None
    filter = []
    _tbl   = None
    
    def __init__(self, filter=[], sort=[], dir=None, offset=None,limit=None):
        self.limit  = limit
        self.offset = offset
        self.sort   = sort
        if dir:
            self.dir    =  dir.lower()
        self.filter = filter
       
        
        
    def getQuery(self):
        
        query = "session.query(%s)" % self._tbl
        
        # Filter Section
        query += self._createFilter()
        
        # Sort Section
        if len(self.sort) > 0:
            if dir:
                query += ".order_by(%s(" % self.dir
            else:
                query += "order_by("
        
            #FIXME CHECK sqlAlchemy syntax for order !!!!!
            for el in self.sort:
                query += "%s.%s" % (self._tbl, el)  
            
            if dir:
                query += ")"
            else:
                query += "))"
        
        if self.offset:  
            query += ".offset(%s).limit(%s)" % ( self.offset, self.limit) 
            
        return query
    
    def getQueryCount(self):
        query = "session.query(%s)" % self._tbl
        
        # Filter Section
        query += self._createFilter() + ".count()"
        
        return query
    
    def _createFilter(self):
        query = ""
        for el in self.filter:
                
            query += ".filter(%s.%s %s %s)" % (self._tbl, el['field'], el['match'],el['value'])
            
        return query
