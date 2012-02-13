from afs.exceptions.AfsError import AfsError


class ORMError(AfsError):
        # No specific Method now
        pass
    
class createEngineError(AfsError):
    def __init__(self, conf):
        self.message = """Cannot create an engine (connect to DB) using following options : DB_USER='%s',DB_HOST='%s',DB_PORT='%s',DB_TYPE='%s',DB_SID='%s'
        """ % (conf.DB_USER,conf.DB_HOST,  conf.DB_PORT, conf.DB_TYPE, conf.DB_SID)
        return
