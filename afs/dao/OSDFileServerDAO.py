import re, datetime
import afs.dao.bin
from afs.util import afsutil
from afs.exceptions.FServError import FServError
from afs.dao.BaseDAO import BaseDAO

class OSDFileServerDAO(BaseDAO) :
    """
    low level access to the FileServer/VolServer pair
    """

    def __init__(self) :
        BaseDAO.__init__(self)
        return
    
    def getVolList(self, serv, part,  cellname, token) :
        """
        List Volume entry via vos listvol from vol-server. 
        return list of dictionaries
        """
        part = afsutil.canonicalizePartition(part)
        CmdList = [afs.dao.bin.VOSBIN,"listvol", "-server", "%s"  % serv , "-part", "%s"  % part ,"-format","-cell", "%s" %  cellname]
        
        rc,output,outerr=self.execute(CmdList)
        if rc :
            raise FServError("Error",outerr)
        
        # first line gives Name, ID, Type, Used and Status 
        volList = [] 
        dateT=datetime.datetime(1970, 1, 1)
        i = 0
        while i < len(output):
            while output[i] != "BEGIN_OF_ENTRY":
                 i = i+1  
                 if i >= len(output): break
            if i >= len(output): break
            #Beginnig block
            splits = output[i].split()
            if splits[0] == "BEGIN_OF_ENTRY":
                    vol = {}
                    splits = output[i+1].split()
                    # Invalid volume, something wrong
                    if splits[0] != 'name':
                        #vol['valid'] = False 
                        if  splits[0] == 'id':
                            vol['vid']      = int(splits[1])
                        
                        splits = output[i+2].split()
                        if  splits[0] == 'serv':
                            vol['servername']     = splits[1] 
                        
                        splits = output[i+3].split()   
                        if  splits[0] == 'part':
                             vol['part']     = afsutil.canonicalizePartition(splits[1]) 
                             
                        splits = output[i+4].split()
                        if  splits[0] == 'status':
                            vol['status']     = splits[1] 
                        
                        while output[i] != "END_OF_ENTRY":
                            i = i+1  
                            
                    # Valid volume                           
                    else:  
                        vol['vid'] = "UNSET"
                        try: 
                          vol['name']     = splits[1]
                          splits = output[i+2].split()
                          vol['vid']      = int(splits[1])
                          splits = output[i+3].split()
                        except :
                            # XXX Here we need a flag to show that parsing was not complete
                            # or a list of Volumes which need to be reparsed.
                            # this will be in the return-code
                            while output[i] != "END_OF_ENTRY":
                                i = i+1
                            self.Logger.error("Cannot parse name of volume with id=%s! Skipping." % vol['vid'])
                            continue
                        
                        if len(splits) > 2:
                           vol['servername']     = splits[2]
                        else:
                           #Only ip is available 
                           vol['servername']     = splits[1] 
                        splits = output[i+4].split()
                        vol['part']     = afsutil.canonicalizePartition(splits[1])
                        splits = output[i+5].split()
                        vol['status']     = splits[1]
                        if vol['status'] != "OK" : 
                            while output[i] != "END_OF_ENTRY":
                                i = i+1
                            continue
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
                        vol['filecount']     = int(splits[1])
                        splits = output[i+22].split()
                        vol['dayUse']        = int(splits[1])
                        splits = output[i+23].split()
                        vol['weekUse']       = int(splits[1])
                        splits = output[i+24].split()
                        vol['osdPolicy']        = int(splits[1])
                        splits = output[i+25].split()
                        vol['filequota']        = splits[1]
                        i = i+26
                    
                    volList.append(vol)
        return volList
        
    def getIdVolList(self, server, part, cell, token):
            """
            return  Volumes in partition
            """
            part = afsutil.canonicalizePartition(part)
            RX=re.compile("^(\d+)")
            CmdList=[afs.dao.bin.VOSBIN,"listvol", "-server", "%s" % server, "-partition", "%s" % part ,"-fast" , "-cell","%s" % cell]
 
            rc,output,outerr=self.execute(CmdList)
            if rc :
                 raise FServError("Error", outerr)
            volIds = []
            
            for line in output [1:]:
                m=RX.match(line)
                if not m :
                    raise FServError("Error parsing output :%s " % line)
                if m :
                   volIds.append(m.groups()[0]) 
                
            return volIds

    def getPartList(self,  serv, cellname, token) :
        """
        return list  of  Partitions-dicts
        """       
        RX=re.compile("Free space on partition /vicep(\S+): (\d+) K blocks out of total (\d+)")
        CmdList=[afs.dao.bin.VOSBIN,"partinfo", "%s" % serv, "-cell","%s" % cellname]
        rc,output,outerr=self.execute(CmdList)
        if rc :
                raise FServError("Error", outerr)
        partitions= []
        for line in output :
            m=RX.match(line)
            if not m :
                raise FServError("Error parsing output" , line)

            part, free, size=m.groups()
            size=long(size)
            free=long(free)
            used = size-free
            partitions.append({ "name" : afsutil.canonicalizePartition(part), "size" : size,  "used" : used,  "free" : free})
        self.Logger.debug("getPartList: returning %s" % partitions)
        return partitions
