import afs.model.Token
from afs.dao import PAGDAO


class TokenService():
    """
    Provides Service about  Token Management.
    TokenDAO is not trivial yet.
    ...
    """
    
    def __init__(self,conf=None):
        # CONF INIT 
        if conf:
            self._CFG = conf
        else:
            self._CFG = afs.defaultConfig

        # LOG INIT
        self.Logger=logging.getLogger("afs").getChild(self.__class__.__name__)
        self.Logger.debug("initializing %s-Object with conf=%s" % (self.__class__.__name__,conf))

        # DAO INIT
        self._pagDAO=PAGDAO.PAGDAO()

    def get_artificial_Token(self,AFSID,AFSCell):
        token = afs.model.Token.Token(AFSID, AFSCell)
        return token
    
    def getToken(self):
        """
        return token object 
        mech is depending on Config.CRED_TYPE 
        ShellToken : from token available in this PAG
        """
        if self._CFG.CRED_TYPE == "ShellToken" :
            AFSID, Cellname = self._pagDAO.getTokeninPAG(cellname=self._CFG.AFSCell)
            Cellname=Cellname.lower()
            token=afs.model.Token.Token(AFSID, Cellname)
        return token
