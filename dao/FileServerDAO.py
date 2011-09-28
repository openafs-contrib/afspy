import re,string,os,sys
import afs.dao.bin

from afs.model.FileServer import FileServer
from afs.model.Partition import Partition
from afs.util import afsutil


class FileServerDAO() :
        """
        Provides Information about a FileServer
        """
        def __init__(self) :
            pass
        
        def getServer(self,servername,cellname):
            """
            List of Servers
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
        
        def getServerList(self, cellname):
            """
            List of Servers
            """
            
            CmdList=[afs.dao.bin.VOSBIN,"listaddrs", "-printuuid", "-cell","%s" % cellname ]
            rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=0,lethal=1)
            if rc :
                return rc,output,outerr
            serverList = []
            for i in range (0,len(output)) :
                if output[i].startswith("UUID:"):
                    server = FileServer()
                    splits = output[i].split()
                    server.uuid = splits[1]
                    i = i +1
                    server.name = output[i]                 
                    serverList.append(server)
                    
            return serverList

   
        def getPartList(self,  servername, cellname) :
            """
            return attribute Partitions
            """
            RX=re.compile("Free space on partition /vicep(\S+): (\d+) K blocks out of total (\d+)")
            CmdList=[afs.dao.bin.VOSBIN,"partinfo", "%s" % servername, "-cell","%s" % cellname]
            rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=0,lethal=1)
            if rc :
                return rc,output,outerr
            partitions= []
            for line in output :
                m=RX.match(line)
                if not m :
                    return rc,"Error parsing output %s" % line
                part = Partition()
                part.name, part.free, part.total=m.groups()
                part.name = afsutil.canonicalizePartition(part.name)
                part.used = long(part.total)-long(part.free)
                partitions.append(part)
                
            return partitions
        
        def getVolIdList(self, part, server, cell):
            """
            return  Volumes in partitions
            """
            RX=re.compile("^(\d+)")
            if part:
                CmdList=[afs.dao.bin.VOSBIN,"listvol", "-server", "%s" % server, "-partition", "%s" % part ,"-fast" , "-cell","%s" % cell]
 
            rc,output,outerr=afs.dao.bin.execute(CmdList,dryrun=0,lethal=1)
            if rc :
                return rc,output,outerr
            volIds = {}
            
            for line in output :
                m=RX.match(line)
                if m :
                   vid = m.groups()
                   volIds[vid] = vid 
                
            return volIds
        
        
        def getServerByName(self, name, cell):
            pass
        
        def getServerByUUID(self, uuid, cell):
            pass
        
        def getServerByIP(self, ip, cell):
            pass
        
