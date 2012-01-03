import re,string,os,sys, datetime
import afs.dao.bin
from afs.util import afsutil
from afs.exceptions.VolError import VolError

class FileServerDAO() :
    """
    low level access to the FileServer/VolServer pair
    """
    def __init__(self) :
        pass
    
    def getVolList(self, serv, part,  cellname, token) :
        """
        List Volume entry via vos listvol from vol-server. 
        return list of dictionaries
        """
        part = afsutil.canonicalizePartition(part)
        CmdList = [afs.dao.bin.VOSBIN,"listvol", "-server", "%s"  % serv , "-part", "%s"  % part ,"-format","-cell", "%s" %  cellname]
        
        rc,output,outerr=afs.dao.bin.execute(CmdList)
        if rc :
            raise FSError("Error",outerror)
        
        line_no = 0
        line = output[line_no]
       
       
        # first line gives Name, ID, Type, Used and Status 
        volList = [] 
        dateT=datetime.datetime(1970, 1, 1)
        for i in range(0, len(output)):
            splits = output[i].split()
            #Beginnig block
            if splits[0] == "BEGIN_OF_ENTRY":
                    vol = {}
                    splits = output[i+1].split()
                    vol['name']     = splits[1]
                    splits = output[i+2].split()
                    vol['vid']      = int(splits[1])
                    splits = output[i+3].split()
                    vol['serv']     = splits[1]
                    if len(splits) > 2:
                        vol['servername']     = splits[2]
                    splits = output[i+4].split()
                    vol['part']     = afsutil.canonicalizePartition(splits[1])
                    splits = output[i+5].split()
                    vol['status']     = splits[1]
                    splits = output[i+6].split()
                    vol['backupID'] = int(splits[1])
                    splits = output[i+7].split()
                    vol['parentID'] = int(splits[1])
                    splits = output[i+8].split()
                    vol['cloneID']  = int(splits[1])
                    splits = output[i+9].split()
                    vol['inUse']    = splits[1]
                    splits = output[i+10].split()
                    vol['needsSalvaged'] = splits[1]
                    splits = output[i+11].split()
                    vol['destroyMe']     = splits[1]
                    splits = output[i+12].split()
                    vol['type']          = splits[1]
                    splits = output[i+13].split()
                    vol['creationDate']  =  dateT.fromtimestamp(float(splits[1]))
                    splits = output[i+14].split()
                    vol['accessDate']    = dateT.fromtimestamp(float(splits[1]))
                    splits = output[i+15].split()
                    vol['updateDate']    = dateT.fromtimestamp(float(splits[1]))
                    splits = output[i+16].split()
                    vol['backupDate']     = dateT.fromtimestamp(float(splits[1]))
                    splits = output[i+17].split()
                    vol['copyDate']      = dateT.fromtimestamp(float(splits[1]))
                    splits = output[i+18].split()
                    vol['flags']         = splits[1]
                    splits = output[i+19].split()
                    vol['diskused']      = int(splits[1])
                    splits = output[i+20].split()
                    vol['maxquota']      = int(splits[1])
                    splits = output[i+21].split()
                    vol['minquota']      = int(splits[1])
                    splits = output[i+22].split()
                    vol['filecount']     = int(splits[1])
                    splits = output[i+23].split()
                    vol['dayUse']        = int(splits[1])
                    splits = output[i+24].split()
                    vol['weekUse']       = int(splits[1])
                    splits = output[i+25].split()
                    vol['spare2']        = splits[1]
                    splits = output[i+26].split()
                    vol['spare3']        = splits[1]
                    volList.append(vol)
                    i = i+26
              
        return volList
        
    def getIdVolList(self, server, part, cell, token):
            """
            return  Volumes in partition
            """
            part = afsutil.canonicalizePartition(part)
            RX=re.compile("^(\d+)")
            CmdList=[afs.dao.bin.VOSBIN,"listvol", "-server", "%s" % server, "-partition", "%s" % part ,"-fast" , "-cell","%s" % cell]
 
            rc,output,outerr=afs.dao.bin.execute(CmdList)
            if rc :
                 raise VolError("Error", outerr)
            volIds = []
            
            for line in output [1:]:
                m=RX.match(line)
                if not m :
                    raise VolError("Error parsing output :%s " % line)
                if m :
                   volIds.append(m.groups()[0]) 
                
            return volIds

    def getPartList(self,  serv, cellname, token) :
            """
            return dict of  Partitions
            """
            RX=re.compile("Free space on partition /vicep(\S+): (\d+) K blocks out of total (\d+)")
            CmdList=[afs.dao.bin.VOSBIN,"partinfo", "%s" % serv, "-cell","%s" % cellname]
            rc,output,outerr=afs.dao.bin.execute(CmdList)
            if rc :
                 raise VolError("Error", outerr)
            
            partitions= []
            for line in output :
                m=RX.match(line)
                if not m :
                    raise VolError("Error parsing output" , line)

                part, free, size=m.groups()
                used = long(size)-long(free)
                if size != 0:
                    perc = (used/long(size))*100
                perc= 0
                partitions.append({"serv":serv, "part":afsutil.canonicalizePartition(part), "size" : long(size),  "used" : long(used),  "free" : long(free), "perc": perc})
            
            return partitions
