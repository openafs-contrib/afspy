import re
import afs.dao.bin
from afs.exceptions.krb5Error import krb5Error
from afs.exceptions.AfsError import AfsError
from afs.dao.BaseDAO import BaseDAO

class PAGDAO(BaseDAO) :
    
    """
    Access to a pag, like getting information about  tokens
    """
    
    TokenRegEx1=re.compile("User's \(AFS ID (\d+)\) tokens for (\S+)@(\S+) \[Expires (.*)\]")
    TokenRegEx2=re.compile("User's \(AFS ID (\d+)\) (\S+) tokens for (\S+) \[Expires (.*)\]")
    
    def __init__(self) :
        BaseDAO.__init__(self)
        return

    def getTokeninPAG(self, cellname=""):
        CmdList=[afs.dao.bin.TOKENBIN ]
        rc,output,outerr=self.execute(CmdList)
        if rc :
            raise AfsError()
        line_no = output.index("Tokens held by the Cache Manager:")
        while 1 :
            if "--End of list--"  in output[line_no] : break
            M=self.TokenRegEx1.match(output[line_no])
            if M :
                # parse M
                this_AFSID = M.groups()[0]
                this_cellname = M.groups()[2]
                if cellname.lower() == this_cellname.lower()  or cellname == "" :
                    return this_AFSID, this_cellname
            else :
                M=self.TokenRegEx2.match(output[line_no])
                if M :
                    # parse here
                    this_AFSID = M.groups()[0]
                    this_cellname = M.groups()[2]
                    if cellname.lower() == this_cellname.lower() or cellname == ""  :
                        return this_AFSID, this_cellname
            line_no += 1
        return "",""
    
    def obtainTokenFromTicket(self, krb5CCName, realm="", cellname=""):
        CmdList=[afs.dao.bin.AKLOGBIN]
        if realm != "" and cellname == "" :
            raise krb5Error
        if cellname != "" :
            CmdList += ["-c", "%s" % cellname]
            if realm != "" :
                CmdList += ["-k","%s" % realm]
        rc,output,outerr=self.execute(CmdList, env={"KRB5CCNAME":krb5CCName})
        if rc :
            raise krb5Error
        return self.getTokeninPAG()
