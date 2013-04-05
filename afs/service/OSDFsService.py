from afs.service.BaseService import BaseService
from afs.service.FsService import FsService
from afs.model.FileServer import FileServer
from afs.exceptions.AfsError import AfsError
from afs.model.ExtendedVolumeAttributes import ExtVolAttr
from afs.model.ExtendedPartitionAttributes import ExtPartAttr
from afs.model.Volume import Volume
from afs.model.Partition import Partition
import afs
import datetime
import sqlalchemy.exc 


class OSDFsService (FsService):
    """
    Provides Service about a FileServer
    """
    
    _CFG    = None
    
    def __init__(self,conf=None):
        BaseService.__init__(self, conf, DAOList=["fs","osdfs", "bnode", "vol", "osdvol", "vl","rx"])

    ###############################################
    # Volume Section
    ###############################################    
    
    def getVolList(self,servername, partname=None, _user="", cached=False):
        """
        Retrieve Volume List
        """
        vols = []
            
        if partname:    
            vols = self._osdfsDAO.getVolList( servername,partname, _cfg=self._CFG, _user=_user)
        else:
            parts = self.getPartitions(servername,cached=cached)
            for part in parts:
                vols += self._osdfsDAO.getVolList(servername,parts[part]["name"], _cfg=self._CFG, _user=_user)
        return vols

    ############################################### 
    # bulk updates
    ############################################### 

    def bulk_cacheVolumes(self,name_or_ip,part="",_user="") :
        """
        store information about all volumes in DBCache
        This intentionally bypasses DBManager. 
        This is probably sql-engine specific (locking!?)
        """
        self.Logger.debug("bulk_cacheVolumes: Entering with name_or_ip=%s,part=%s" % (name_or_ip,part) )
        serv_uuid=afs.LookupUtil[self._CFG.CELL_NAME].getFSUUID(name_or_ip,self._CFG,cached=True)
        if not self._CFG.DB_CACHE :
            raise AfsError("No DB_Cache defined.")

        retry=[]
        vids=[]
        # get (preliminary) list of volumes
        _vols=self.getVolList(name_or_ip,part,_user=_user,cached=False)
        # final list of volumes (including retries)
        vols=[]
        # generate list of vids
        vids=[]
        
        for v in _vols :
            if v['status'] != "OK" : 
                retry.append(v['vid'])
                self.Logger.info("bulk_cacheVolumes: serv=%s, part=%s, vol %s returned as %s. Retrying later." % (name_or_ip,part,v["vid"],v['status']) )
                continue
            vids.append(v["vid"])
            vols.append(v)

        # refetch busy volumes
        # don't know if this can return BUSY as well.
        for r in retry :
            try :
                vol=self._osdvolDAO.getVolume(r,name_or_ip,part,_user=_user,_cfg=self._CFG)
                vids.append(r)
                vols.append(vol)
            except :
                self.Logger.error("Cannot get information about serv=%s, part=%s, vol %s. Skipping." % (name_or_ip,part,r))

        # fixed DB-entries
        cdate = udate = datetime.datetime(1970, 1, 1).now()
        spare2 = spare3 = minquota = -1

        conn = self._CFG.DB_ENGINE.connect()
        t = conn.begin()
        # this should be atomic
        #rawsql='UNLOCK TABLES'
        #rawsql='LOCK TABLES tbl_volume WRITE;'
        #res = conn.execute(rawsql)
        # scan  server/partition for volids to insert/update
        # delete all entries of this server-partition, then recreate them. 
        rawsql = 'SELECT vid FROM tbl_volume WHERE serv_uuid="%s" AND part="%s"' % (serv_uuid,part)
        for vid in conn.execute(rawsql).fetchall() :
            rawsql='DELETE FROM tbl_extvolattr WHERE vid="%s"' % (vid[0])
            res = conn.execute(rawsql)
            rawsql='DELETE FROM tbl_extvolattr_osd WHERE vid="%s"' % (vid[0])
            res = conn.execute(rawsql)
            rawsql='DELETE FROM tbl_volume WHERE serv_uuid="%s" AND part="%s" AND vid="%s"' % (serv_uuid,part,vid[0])
            self.Logger.debug("rawsql=%s" % rawsql)
            res = conn.execute(rawsql)

        for v in vols :
            self.Logger.debug("processing v=%s" %v)
            if v == None : 
                self.Logger.warn("got a None in vols=%s" % vols)
                continue
            rawsql='INSERT INTO tbl_volume (vid,name,serv_uuid,part,servername,parentID,backupID,cloneID,inUse,needsSalvaged,destroyMe,type,creationDate,accessDate,updateDate,backupDate,copyDate,flags,diskused,maxquota,minquota,status,filecount,dayUse,weekUse,spare2,spare3, udate, cdate) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s");' % (v['vid'], v['name'],serv_uuid, part, v['servername'], v['parentID'], v['backupID'],v['cloneID'], v['inUse'], v['needsSalvaged'], v['destroyMe'], v['type'], v['creationDate'], v['accessDate'], v['updateDate'], v['backupDate'], v['copyDate'], v['flags'], v['diskused'], v['maxquota'], minquota, v['status'], v['filecount'], v['dayUse'], v['weekUse'], spare2, spare3, udate, cdate)
            self.Logger.debug("rawsql=%s" % rawsql)
            res = conn.execute(rawsql)
            self.Logger.debug("res=%s" % res)
        rawsql='UNLOCK TABLES'
        res = conn.execute(rawsql)
      
        #
        # osd-info for osd-volumes
        #


        # XXX GC cannot be done here on server_partition basis, no such information in tbl_extvolattr_osd.
        # write global GC for that

        updates={}
        rawsql = 'SELECT vid,cdate FROM tbl_extvolattr_osd' 
        for _vid in conn.execute(rawsql).fetchall() :
            if _vid[0] in vids :
                updates[_vid[0]]=_vid[1]

        for v in vols :
            if v == None : 
                self.Logger.warn("got a None in vols=%s" % vols)
                continue
            if v["osdPolicy"] == 0 : continue
            self.Logger.debug("processing OSD_Volume v=%s" %v)
            odict=self._osdvolDAO.traverse(name_or_ip,v['vid'],_user=_user,_cfg=self._CFG)
            self.Logger.debug("odict=%s" % odict)
            files_fs=odict["storageUsage"]["fileserver"]["numFiles"]
            files_osd=odict["storageUsage"]["online"]["numFiles"] + odict["storageUsage"]["archival"]["numFiles"]
            blocks_fs=odict["storageUsage"]["fileserver"]["Data"] 
            blocks_osd_on=odict["storageUsage"]["online"]["Data"] 
            blocks_osd_off=odict["storageUsage"]["archival"]["Data"] 
            self.Logger.debug("got odict=%s" % odict)
            if v["vid"] in updates :
                rawsql='UPDATE tbl_extvolattr_osd SET vid="%s", filequota="%s", files_fs="%s", files_osd="%s", blocks_fs="%s", blocks_osd_on="%s", blocks_osd_off="%s", osdPolicy="%s", udate="%s", cdate="%s" WHERE vid = "%s"' % (v['vid'], v['filequota'], files_fs,files_osd,blocks_fs,blocks_osd_on,blocks_osd_off,v['osdPolicy'],udate, updates[v['vid']],v['vid'])
            else :
                rawsql='INSERT into tbl_extvolattr_osd (vid, filequota, files_fs, files_osd, blocks_fs, blocks_osd_on, blocks_osd_off, osdPolicy, udate, cdate) VALUES("%s", "%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (v['vid'], v['filequota'], files_fs,files_osd,blocks_fs,blocks_osd_on,blocks_osd_off,v['osdPolicy'],udate, cdate)
            self.Logger.debug("Executing rawsql: %s" % rawsql)
            res = conn.execute(rawsql)

        t.commit()
        conn.close()

        return True
