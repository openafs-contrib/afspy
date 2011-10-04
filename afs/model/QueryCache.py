


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
        self.dir    = None
        self.filter = filter
       
        
        
    def getQuery(self):
        
        query = "query(%s)" % self._tbl
        
        # Filter Section
        query += self.createFilter()
        
        # Sort Section
        if len(sort) > 0:
            if dir:
                query += ".order_by(%s("
            else:
                query += "order_by("
        #FIXME CHECK sqlAlchemy syntax for order !!!!!
            for el in sort:
                query += "%s.%s" % (self._tbl, sort)  
            
            query += ")"
        
        if offset:  
            query += ".offset(%s).limit(%s)" % ( offset, limit) 
            
        return query
    
    def getQueryCount(self):
        query = "query(%s)" % self._tbl
        
         # Filter Section
        query += self.createFilter() + ".count()"
        
        return query
    
    def _createFilter(self):
        query = ""
        for el in self.filter:
                
            query += ".filter(%s.%s %s %s)" % (self._tbl, el['field'], el['match'],el['value'])
            
        return query