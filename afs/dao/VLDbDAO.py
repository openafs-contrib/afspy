import re,string,os,sys
import afs.dao.bin

class VLDbDAO() :
        """
        Provides low-level acces to the Volume Location Database
        """
        def __init__(self) :
            return
        
        def getFsServerList(self,servername,cellname):
            """
            get Information about a single Server
            """
            
            CmdList=[afs.dao.bin.VOSBIN,"listaddrs", "-host","%s" % servername, "-printuuid", "-cell","%s" % cellname ]
            rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=0,lethal=1)
            if rc :
                return rc,output,outerr
           
            server = FileServer()
            for i in range (0,len(output)) :
                if output[i].startswith("UUID:"):
                    splits = output[i].split()
                    server.uuid = splits[1]
                    i = i +1
                    server.name = output[i]                                   
            return server
