import string,re,sys,time, tempfile, os
import afs.dao.bin
from afs.exceptions.krb5Error import krb5Error
from afs.dao.BaseDAO import BaseDAO

class krb5DAO(BaseDAO) :
    
    """
    low-level Kerberos stuff 
    """
    
    def __init__(self) :
        BaseDAO.__init__(self)
        return
        
    def getKRB5CCNAME(self):
        handle, KRB5CCNAME=tempfile.mkstemp()
        os.close(handle)
        return KRB5CCNAME

    def listTicket(self, KRB5CCNAME):
        CmdList=[afs.dao.bin.KLISTBIN ]
        rc,output,outerr=self.execute(CmdList, env={"KRB5CCNAME":KRB5CCNAME})
        if rc :
            raise KrbError
        return KRB5CCNAME

    def destroyTicket(self, KRB5CCNAME):
        CmdList=[afs.dao.bin.KDESTROYBIN, "-c","%s" % KRB5CCNAME ]
        rc,output,outerr=self.execute(CmdList, env={"KRB5CCNAME":KRB5CCNAME})
        if rc :
            raise KrbError
        return

    def getTicketbyPassword(self,password, principal="",realm="", KRB5CCNAME="") :
        """
        Obtain Krb5Ticket by prompting for password.
        """ 
        # need to create save tmp-filename to store ticket
        if KRB5CCNAME == "" :
            KRB5CCNAME=self.getKRB5CCNAME()
        CmdList=[afs.dao.bin.KINITBIN,"-c" , "%s" % KRB5CCNAME]
        if principal != "" :
            if realm != "" :
                CmdList += ["%s@%s" % (principal,realm)]
            else :
                CmdList += ["%s" % principal]
        rc,output,outerr=self.execute(CmdList, Input=password)
        if rc :
            raise KrbError
        return KRB5CCNAME

    
    def getTicketbyKeytab(self,keytab, principal="",realm="", KRB5CCNAME="") :
        """
        Obtain Krb5Ticket by using a given keytab
        """ 
        if KRB5CCNAME == "" :
            KRB5CCNAME=self.getKRB5CCNAME()
        CmdList=[afs.dao.bin.KINITBIN,"-c" , "%s" % KRB5CCNAME,"-k","-t","%s" % keytab ]
        if principal != "" :
            if realm != "" :
                CmdList += ["%s@%s" % (principal,realm)]
            else :
                CmdList += ["%s" % principal]
        rc,output,outerr=self.execute(CmdList)
        if rc :
            raise KrbError
        return KRB5CCNAME
