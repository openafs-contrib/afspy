import string,re,sys,time
import afs.dao.bin

class KrbD5AO() :
    
    """
    low-level Kerberos stuff 
    """
    
    def __init__(self):
        return

    def listTicket(self, KRB5CCNAME=""):
        CmdList=[afs.dao.bin.KLISTBIN ]
        rc,output,outerr=afs.dao.bin.execute(CmdList)
        if rc :
            raise KrbError
        return KRB5CCNAME

    def getTicketbyPasswd(self,principal,realm) :
        """
        Obtain Krb5Ticket by prompting for password.
        """ 
        # need to create save tmp-filename to store ticket
        CmdList=[afs.dao.bin.KINITBIN,"-c" , "%s" % KRB55CCNAME, "%s@%s" % (principal,realm) ]
        rc,output,outerr=afs.dao.bin.execute(CmdList)
        if rc :
            raise KrbError
        return KRB5CCNAME

    
    def getTicketbyKeytab(self,principal,realm,keytab) :
        """
        Obtain Krb5Ticket by using a given keytab
        """ 
        CmdList=[afs.dao.bin.KINITBIN,"-k","-t","%s" % keytab, "%s@%s" % (principal,realm) ]
        rc,output,outerr=afs.dao.bin.execute(CmdList)
        if rc :
            raise KrbError
        return KRB5CCNAME

    
