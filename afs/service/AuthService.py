import afs.model.Token
from afs.dao import PAGDAO


class TokenService():
    """
    Provides Service about  Token Management.
    TokenDAO is not trivial yet.
    ...
    """
    
    def __init__(self,conf=None):
        """
        """
        if conf:
            self._CFG = conf
        else:
            self._CFG = afs.defaultConfig

    def get_artificial_Token(self,AFSID,AFSCell):
        token = afs.model.Token.Token(AFSID, AFSCell)
        return token
    
    def getToken(self):
        """
        XXX : Move to Authservice
        """
        if self._CFG.CRED_TYPE == "ShellToken" :
            pagdao = PAGDAO.PAGDAO()
            AFSID, Cellname = pagdao.getTokeninPAG(cellname=self._CFG.AFSCell)
            Cellname=Cellname.lower()
            token=afs.model.Token.Token(AFSID, Cellname)
        return token
