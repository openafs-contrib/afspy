import afs.util.options


from afs.util.AfsConfig import AfsConfig





class BaseService(object):
    """
    Provides implementation for basic mathods for all Service.
.
    """
    
    def __init__(self,conf=None):
        
               
        # LOAD Configuration from file if exist
        # FIXME Move in decorator
        if conf:
            self._CFG = conf
        else:
            self._CFG = afs.defaultConfig
        
        # DB INIT 
        if self._CFG.DB_CACHE :
            import sqlalchemy.orm
            from sqlalchemy import func, or_
            
            self.DbSession = sqlalchemy.orm.sessionmaker(bind=self._CFG.DB_ENGINE)
            self.or_ = or_
    
    def execQuery(self, query):
        conn = self._CFG.DB_ENGINE.connect()
        res = conn.execute(query)
        conn.close()
        
        return res
    
    def execOrmQuery(self,orm):
        session = self.DbSession()
        
        res = eval(orm)
            
        session.commit()
        session.close()
        
        return res