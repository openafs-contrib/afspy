import logging
import afs.model.Token
from afs.dao import PAGDAO
from afs.dao import krb5DAO
import getpass


class TokenService(object):
    """
    Provides Service for Token Management.
    Multiple methods of acquiring a token are included
    """
    
    def __init__(self,conf=None):
        # CONF INIT 
        if conf:
            self._CFG = conf
        else:
            self._CFG = afs.defaultConfig

        # LOG INIT
        self.Logger=logging.getLogger("afs.%s" % self.__class__.__name__)
        self.Logger.debug("initializing %s-Object with conf=%s" % (self.__class__.__name__,conf))

        # DAO INIT
        self._pagDAO=PAGDAO.PAGDAO()
        self._krb5DAO=krb5DAO.krb5DAO()

    def get_artificial_Token(self,AFSID,CELL_NAME):
        token = afs.model.Token.Token(AFSID, CELL_NAME)
        return token
    
    def getToken(self):
        """
        return token object 
        mech is depending on Config.CRED_TYPE 
        PAG : from token available in this PAG
        Keytab:<filename> from keytab
        """
        tokens=self._CFG.CRED_TYPE.split(":")
        CredType=tokens[0].lower()
        if len(tokens) > 1 :
            CredArgs=self._CFG.CRED_TYPE[len(CredType)+1:]
        else :
            CredArgs = ""
        # acquire token, if required 
        if CredType == "pag" :
            pass
        elif CredType == "krb5_keytab" :
            KRB5CCNAME=self._krb5DAO.getTicketbyKeytab(CredArgs, self._CFG.KRB5_PRINC,self._CFG.KRB5_REALM)
            self._pagDAO.obtainTokenFromTicket(KRB5CCNAME, self._CFG.KRB5_REALM, self._CFG.CELL_NAME)
            self._krb5DAO.destroyTicket(KRB5CCNAME)
        elif CredType == "krb5_password" :
            if CredArgs != "" :
                passwd=CredArgs
            else :
                passwd = getpass.getpass()
            KRB5CCNAME=self._krb5DAO.getTicketbyPassword(passwd, self._CFG.KRB5_PRINC,self._CFG.KRB5_REALM)
            self._pagDAO.obtainTokenFromTicket(KRB5CCNAME, self._CFG.KRB5_REALM, self._CFG.CELL_NAME)
            self._krb5DAO.destroyTicket(KRB5CCNAME)
        # get token-info from pag
        AFSID, Cellname = self._pagDAO.getTokeninPAG(cellname=self._CFG.CELL_NAME)
        Cellname=Cellname.lower()
        token=afs.model.Token.Token(AFSID, Cellname)
        return token
