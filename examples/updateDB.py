#!/usr/bin/python


import cProfile
import time,logging
import argparse, string,datetime,sys
import afs
from afs.util.AfsConfig import parseDefaultConfig
from afs.util.DBManager import DBManager
from afs.service.OSDVolService import OSDVolService
from afs.service.OSDCellService import OSDCellService
from afs.service.OSDFsService import OSDFsService
from afs.service.DBsService import DBsService
from afs.service.ProjectService import ProjectService
from afs.model.Volume import Volume
from afs.model.Partition import Partition
from afs.model.ExtendedPartitionAttributes import ExtPartAttr
from afs.dao.UbikPeerDAO import UbikPeerDAO
from afs.dao.OSDVolumeDAO import OSDVolumeDAO

myParser=argparse.ArgumentParser(parents=[afs.argParser], add_help=False)
myParser.add_argument("--force", action='store_true',default=False, help="force re-check")
myParser.add_argument("--create", action='store_true',default=False, help="create new DB.")
myParser.add_argument("--onlySP", default="", help="check only server_partition")
myParser.add_argument("--stat", action='store_true', default=False, help="do not query live-system, but only update DB-internal sums")

parseDefaultConfig(myParser)
VDAO=OSDVolumeDAO()
CS=OSDCellService()
FS=OSDFsService()
VS=OSDVolService()
DBsS=DBsService()
DBM=DBManager()
PS=ProjectService()
UDAO=UbikPeerDAO()

def main() :

    if afs.defaultConfig.create :
        use_cache=False
    else :
        use_cache=True
    
    VLDBup2date=False


    # if we have a specified partition, do only just hat.    
 
    if afs.defaultConfig.onlySP != "" :
        # full update
        f,p=afs.defaultConfig.onlySP.split("_")
        print "Server: {0}".format(f)
        FileServer=FS.getFileServer(name_or_ip=f,cached=use_cache)
        if p == "*" :
            partnames=FileServer.parts.keys()
            partnames.sort()
        else :
            partnames=[p,]
        for part in partnames :
            print "part: {0}".format(part) 
            do_updatePartition(FileServer,f,part,use_cache)
        sys.exit(0)

    # update DB-internal sums only

    if afs.defaultConfig.stat :
        cachedCell=CS.getCellInfo(cached=True)
        for f in cachedCell.FileServers :
            print "Server: {0}".format(f)
            FileServer=FS.getFileServer(name_or_ip=f,cached=True)
            partnames=FileServer.parts.keys()
            for part in partnames :
                print "part: {0}".format(part) 
                do_update_ExtPartAttr(FileServer,part)
        sys.exit(0)




    if not afs.defaultConfig.create :
        cachedCell=CS.getCellInfo(cached=True)
        liveCell=CS.getCellInfo(cached=False)
        # live_VLDBVersion=UDAO.getShortInfo(cachedCell.DBServers[0],7003,None,None)["SyncSiteDBVersion"]
        # update if required
        if cachedCell :
            if "%s" % cachedCell.VLDBVersion == "%s" % liveCell.VLDBVersion :
                print "VLDB Versions considered equal (cached: '{0}',live:'{1}').".format(cachedCell.VLDBVersion,liveCell.VLDBVersion)
                VLDBup2date = True
            else :
                print "VLDB Versions differ ('{0}' != '{1}').".format(cachedCell.VLDBVersion,liveCell.VLDBVersion)
                VLDBup2date = False
        else :
            VLDBup2date = True
    else :
        liveCell=CS.getCellInfo(cached=False)
  
    # first update DBServer
    for db in liveCell.DBServers :
        print "Server: {0}".format(db)
        VLDBServer=DBsS.getDBServer(db,"vldb")
        PTDBServer=DBsS.getDBServer(db,"ptdb")
    ignoreFS=[]
    #  then FileServer
    for f in liveCell.FileServers :
        print "Server: {0}".format(f)
        try :
           FileServer=FS.getFileServer(name_or_ip=f)
        except: 
           ignoreFS.append(f) 


    if not afs.defaultConfig.force : 
        if  afs.defaultConfig.create :
            print "Re-creation of Database forced." 
        else :
            if VLDBup2date :
                print "Don't update"
                sys.exit(0)
    else :
        if  afs.defaultConfig.create :
            print "Re-creation of Database forced." 
        else :
            print "Update forced."
  
    if not afs.defaultConfig.create : 
        # check volume-list of all sever partitions and compare live and db-lists
        # to see what has changed
        for f in liveCell.FileServers :
            print "Server: {0}".format(f)
            if f in ignoreFS : 
                print "ignored because of previous error."
                continue
            FileServer=FS.getFileServer(name_or_ip=f)
            partnames=FileServer.parts.keys()
            partnames.sort()
            for part in partnames :
                print "part: {0}...".format(part),
                vols_live=FS.getVolumeIDs(f,part=part,cached=False)
                vols_live.sort()
                vols_cached=[]
                for v in DBM.executeRaw('SELECT vid FROM tbl_volume WHERE serv_uuid="%s" AND part="%s";' % (FileServer.uuid,part)).fetchall() :
                    vols_cached.append(v[0])
                vols_cached.sort()
                if vols_cached != vols_live :
                    print "modified, updating..."
                    # XXX here, we should just update the volumes which changed
                    do_updatePartition(FileServer,f,part,use_cache)
                else :
                    print "OK"
    else : # do full update of all volumes
        # full update
        for f in liveCell.FileServers :
            print "Server: {0}".format(f)
            if f in ignoreFS : 
                print "ignored because of previous error."
                continue
            FileServer=FS.getFileServer(name_or_ip=f,cached=use_cache)
            partnames=FileServer.parts.keys()
            partnames.sort()
            for part in partnames :
                print "part: {0}".format(part) 
                do_updatePartition(FileServer,f,part,use_cache)
    sys.exit(0)

def do_updatePartition(FileServer,f,part,use_cache) :
    # update all Volume information in DB
    # this includes ExtVolAttr and ExtVolAttr_OSD
    FS.bulk_cacheVolumes(f,part)
    do_update_ExtPartAttr(FileServer,part)
    return 

def do_update_ExtPartAttr(FileServer,part) :
    # get time 6 Months ago
    StaleDate=datetime.timedelta(days=-183)
    dateStale=datetime.datetime(1970, 1, 1).now()+StaleDate
    # allocated is tricky, we want to use single ROs, but not accompanying RO's.
     
    # get stats for RW 
    #FS.DBManager.Logger.setLevel(logging.DEBUG)
    SQL='SELECT SUM(maxquota) FROM tbl_volume WHERE updateDate < "%s" AND type="RW" AND serv_uuid="%s" AND part="%s"' % (dateStale,FileServer.uuid,part)
    allocated_stale=FS.DBManager.executeRaw(SQL).fetchone()[0]
    if allocated_stale == None :
        allocated_stale = 0
    #FS.DBManager.Logger.setLevel(logging.WARN)
    SQL='SELECT SUM(maxquota) FROM tbl_volume WHERE type="RW" AND serv_uuid="%s" AND part="%s"' % (FileServer.uuid,part)
    allocated=FS.DBManager.executeRaw(SQL).fetchone()[0]
    if allocated == None :
        allocated = 0
    SQL='SELECT COUNT(maxquota) FROM tbl_volume WHERE type="RW" AND serv_uuid="%s" AND part="%s" AND maxquota="0"' % (FileServer.uuid,part)
    unLimitedVolumes=FS.DBManager.executeRaw(SQL).fetchone()[0]

    # get stats for single RO
    SQL='SELECT SUM(maxquota) FROM (SELECT  type,parentID,maxquota FROM tbl_volume WHERE updateDate < "%s" AND serv_uuid="%s" AND part="%s" GROUP BY parentID HAVING COUNT(parentID) = 1) as T1 WHERE T1.type="RO";' % (dateStale,FileServer.uuid,part)
    _allo=FS.DBManager.executeRaw(SQL).fetchone()[0]
    if _allo == None : _allo = 0
    allocated_stale += _allo
    SQL='SELECT SUM(maxquota) FROM (SELECT  type,parentID,maxquota FROM tbl_volume WHERE serv_uuid="%s" AND part="%s" GROUP BY parentID HAVING COUNT(parentID) = 1) as T1 WHERE T1.type="RO";' % (FileServer.uuid,part)
    _allo=FS.DBManager.executeRaw(SQL).fetchone()[0]
    if _allo == None : _allo = 0
    allocated += _allo
    SQL='SELECT COUNT(maxquota) FROM (SELECT type,parentID,maxquota FROM tbl_volume WHERE serv_uuid="%s" AND part="%s" AND maxquota ="0" GROUP BY parentID HAVING COUNT(parentID) = 1) as T1 WHERE T1.type="RO";' % (FileServer.uuid,part)
    unLimitedVolumes=FS.DBManager.executeRaw(SQL).fetchone()[0]

    numRW,numRO,numBK,numOffline=FS.getNumVolumes(name_or_ip=FileServer.servernames[0],part=part,cached=True)
    projectIDs={}
    ExtPart=ExtPartAttr(FileServer.uuid,part)
    ExtPart.allocated=allocated
    ExtPart.allocated_stale=allocated_stale
    ExtPart.unLimitedVolumes=unLimitedVolumes
    #FS.Logger.setLevel(logging.DEBUG)
    #FS.DBManager.Logger.setLevel(logging.DEBUG)
    #FS.Logger.setLevel(logging.WARN)
    #FS.DBManager.Logger.setLevel(logging.WARN)
    ExtPart.numRW=numRW
    ExtPart.numRO=numRO
    ExtPart.numBK=numBK
    ExtPart.numOffline=numOffline
    ExtPart.projectIDs=projectIDs
    FS.DBManager.setIntoCache(ExtPartAttr,ExtPart,serv_uuid=FileServer.uuid,name=part)
    print "server %s part %s: numRW=%s, numRO=%s,numBK=%s,numOffline=%s,allocated=%s,allocated_stale=%s" % (FileServer.servernames[0],part,numRW,numRO,numBK,numOffline,allocated,allocated_stale)
    return


if __name__=="__main__" :
    #cProfile.run('main()',"updateDB.prof")
    main()

