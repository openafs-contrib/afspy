#!/usr/bin/python

import re
import time,logging
import argparse, string,datetime,sys
import afs
from afs.util.AfsConfig import parseDefaultConfig
from afs.util.afsutil import parseHumanWriteableSize
from afs.service.OSDVolService import OSDVolService
from afs.service.OSDCellService import OSDCellService
from afs.service.OSDFsService import OSDFsService
from afs.service.ProjectService import ProjectService
from afs.model.Volume import Volume
from afs.dao.VolumeDAO import VolumeDAO
from afs.dao.VLDbDAO import VLDbDAO

global FS,PS,VS,VD,VlD

myParser=argparse.ArgumentParser(parents=[afs.argParser], add_help=False)
myParser.add_argument("--ssrv", required=True, help="server to empty")
myParser.add_argument("--spart", help="partition on server to empty. defaults to all")
myParser.add_argument("--dsrv" , help="force server to be filled. Otherwise chosen automatically by project.")
myParser.add_argument("--dpart" , help="force partition on server to be filled. Otherwise chosen automatically by project.")
group = myParser.add_mutually_exclusive_group()
group.add_argument("--ignorerx", dest="ignoreRX", action="append",  help="regEx for volumenames to ignore. All volumes not matching this will be moved.")
group.add_argument("--onlyrx", dest="onlyRX", action="append", help="regEx for volumenames to include all volumes not matching this will be ignored.")
group.add_argument("--ignoreproject", dest="ignoreProjects", action="append", help="ignore volumes of given project.")
group.add_argument("--onlyproject", dest="onlyProjects", action="append", help="only move volumes of given project.")
myParser.add_argument("--dryrun",action="store_true", help="Just print out what would be done, but don't do it.")
myParser.add_argument("--maxnum", default = 0, type=int, help="max number of Volumes to move.")
myParser.add_argument("--untilfree", default = "0", help="move until # is free on spart.")
myParser.add_argument("--rwvols", dest="moveRWVols", default=False, action="store_true", help="move rwvols with their accompanying ROs.")
myParser.add_argument("--solitaryrovols", dest="moveSolitaryROVols", default=False, action="store_true", help="move solitary rovols.")
myParser.add_argument("--minsize", dest="minVolumeUsage", default="0", help="only move volumes with minimalsize of")
myParser.add_argument("--osdvolumes", dest="moveOSDVOlumes", default=False, action="store_true", help="also move OSD-Volumes")


parseDefaultConfig(myParser)
FS=OSDFsService()
PS=ProjectService()
VS=OSDVolService()
VD=VolumeDAO()
VlD=VLDbDAO()

if not afs.defaultConfig.moveRWVols and not afs.defaultConfig.moveSolitaryROVols :
    sys.stderr.write("If you want to nmake me do anything, specify --rwvols and/or --solitaryrovols\n")
    sys.exit(1)

if afs.defaultConfig.ignoreRX != None :
    ignoreRX=[]
    for rx in afs.defaultConfig.ignoreRX :
        try :
            ignoreRX.append(re.compile(rx))
        except :
            sys.stderr.write("Cannot compile regular expression: '%s'\n" % rx)
            sys.exit(1)
elif afs.defaultConfig.onlyRX != None :
    onlyRX=[]
    for rx in afs.defaultConfig.onlyRX :
        try :
            onlyRX.append(re.compile(rx))
        except :
            sys.stderr.write("Cannot compile regular expression: '%s'\n" % rx)
            sys.exit(1)
srcFS=FS.getFileServer(afs.defaultConfig.ssrv)

if srcFS == None :
    sys.stderr.write("src server %s does not exist." % srcFS)
    sys.exit(2)
if afs.defaultConfig.spart != None :
    if not afs.defaultConfig.spart in srcFS.parts : 
        sys.stderr.write("Partition %s does not exist on server %s\n" % (afs.defaultConfig.spart, afs.defaultConfig.ssrv))
        sys.exit(2)
    # we cycle thorugh this list later
    srcParts=[afs.defaultConfig.spart]
else :
    srcParts=srcFS.parts


if afs.defaultConfig.dsrv != None :
    dstFS=FS.getFileServer(afs.defaultConfig.dsrv)
    if dstFS == None :
        sys.stderr.write("destination server %s does not exist.\n" % srcFS)
        sys.exit(2)

    if afs.defaultConfig.dpart != None :
        if not afs.defaultConfig.dpart in dstFS.parts : 
            sys.stderr.write("Partition %s does not exist on server %s\n" % (afs.defaultConfig.dpart, afs.defaultConfig.dsrv))
            sys.exit(2)
        else :
            reqDstPart=afs.defaultConfig.dpart  
    else :
        reqDstPart=None
else :
    dstFS=None
    if afs.defaultConfig.dpart != None :
        sys.stderr.write("Warning: ignoring given dpart=%s, because no dsrv has been specified.\n" % afs.defaultConfig.dpart)

# XXX we should handle everything internally with bytes
untilFree=parseHumanWriteableSize(afs.defaultConfig.untilfree)/1024
minUsage=parseHumanWriteableSize(afs.defaultConfig.minVolumeUsage)/1024
VolObj = Volume()
movedVolcount=0
for srcP in srcParts :
    print "Processing Partition %s...." % srcP
    # check if partition is freed enough
    parts=FS.getPartitions(afs.defaultConfig.ssrv)
    if parts[srcP]["free"] > untilFree and untilFree > 0 :
        print "already %s Bytes free on spart %s." % (afs.util.afsutil.humanReadableSize(parts[srcP]["free"]),srcP )
        continue
    # get list of volumes to move
    srcVolList=FS.getVolList(srcFS.servernames[0],srcP,cached=False)
    # get RW Volumes :
    RWVols=[]
    solitaryROVols=[]
    for v in srcVolList : 
        if "type" in v.keys() :
            if v["type"] == "RW" : RWVols.append(v)
    for v in srcVolList :
        if "type" in v.keys() :
            isSolitary = True  
            if v["type"] == "RO" :
                for rw in RWVols :
                    if rw["name"] == v["name"][:-9] : 
                        isSolitary = False
                if isSolitary : solitaryROVols.append(v)
    if afs.defaultConfig.moveRWVols :
        for v in RWVols :
            # check for moving osd-volumes
            if v.get("osdPolicy",0) != 0 :
                if not afs.defaultConfig.moveOSDVOlumes : 
                    print "Skipping %s, because it is an OSD-Volume" % v["name"]
                    continue
            # check for minSize
            if minUsage != 0 :
                if int(v.get("diskused")) < minUsage : 
                    print "Skipping %s, because it is smaller than %s" % minUsage 
                    continue
           
            # check for name with given regex, these checks are mutually exclusive.
            skip_it=False
            if afs.defaultConfig.ignoreRX != None :
                skip_it=False
                for rx in ignoreRX :
                    if rx.match(v["name"]) : skip_it = True
            elif afs.defaultConfig.onlyRX != None :
                skip_it=True
                for rx in onlyRX :
                    if rx.match(v["name"]) : skip_it = False
            elif afs.defaultConfig.onlyProjects != None :
                skip_it=True
                volProjects=PS.getProjectsByVolumeName(v["name"])
                for prj in volProjects :
                    if prj.name in afs.defaultConfig.onlyProjects : skip_it = False
            elif afs.defaultConfig.ignoreProjects != None :
                skip_it=False
                volProjects=PS.getProjectsByVolumeName(v["name"])
                for prj in volProjects :
                    if prj.name in afs.defaultConfig.ignoreProjects : skip_it = True
            
            if skip_it  : continue
            # remove osd-attributes from dict, create Obj
            v.pop("filequota")
            v.pop("osdPolicy")
            v["serv_uuid"]=afs.LookupUtil[afs.defaultConfig.CELL_NAME].getFSUUID(v["servername"])
            VolObj.setByDict(v)
            if dstFS == None :
                minNestingLevel=-1 # NestingLevel should be "spezifizitaet"
                for p in PS.getProjectsByVolumeName(v["name"]) :
                    if p.NestingLevel <  minNestingLevel or  minNestingLevel == -1 :
                        minNestingLevel =  p.NestingLevel
                        PrjObj=p
                dstSrv,dstP = PS.getNewVolumeLocation(PrjObj.name,VolObj)
                if dstSrv == None :
                    sys.stderr.write("found no appropriate location for %s, part of project %s. Skipping\n" % (VolObj.name,PrjObj.name))
                    continue
            else :
                dstSrv = dstFS.servernames[0]
                parts=FS.getPartitions(dstSrv)
                if reqDstPart == None :
                    maxFree=0
                    for p in parts :
                        if parts[p]["free"] > maxFree :
                            dstP=p
                            maxFree=parts[p]["free"] 
                else :
                    dstP=reqDstPart      
            print "moving volume %s from %s %s to %s %s" % (v["name"],srcFS.servernames[0],srcP,dstSrv,dstP)
            if not afs.defaultConfig.dryrun : 
                VD.move(v["name"],srcFS.servernames[0],srcP,dstSrv,dstP)
                try :
                    # add RO to dstSrv if there is none yet.
                    hasRO=False
                    for ov in VS.getVolume("%s.readonly" % VolObj.name, cached=False) :
                        if ov.servername == dstSrv and ov.part == dstP :
                            hasRO = True
                    if hasRO :  # find a second server to move the RO to then
                        dstSrv,dstP = PS.getNewVolumeLocation(PrjObj.name,ov)
                        if dstSrv == None :
                            sys.stderr.write("found no appropriate location for %s. Skipping\n" % VolObj.name)
                            continue
                except : # there is no RO, so just skip this.
                    continue 
            print "Moving accompanying RO to  %s %s" % (dstSrv,dstP)
            if not afs.defaultConfig.dryrun  :
                VlD.addsite(v["name"],dstSrv,dstP)
                VD.release(v["name"])
                # only remove accompanying RO from srcSRV if we are sure there is one!
                for ov in VS.getVolume("%s.readonly" % VolObj.name, cached=False) :
                    if ov.servername == srcFS.servernames[0] and ov.part == srcP :
                        VD.remove("%s.readonly" % v["name"],srcFS.servernames[0],srcP)
                        break
            movedVolcount += 1
            if movedVolcount > afs.defaultConfig.maxnum and afs.defaultConfig.maxnum > 0 :
                print "moved %d volumes. Terminating." % afs.defaultConfig.maxnum
                sys.exit(0)
            # check if partition is freed enough
            parts=FS.getPartitions(afs.defaultConfig.ssrv)
            if parts[srcP]["free"] > untilFree and untilFree > 0 :
                print "%s bytes free on spart %s." % (afs.util.afsutil.humanReadableSize(parts[srcP]["free"]),srcP )
                break
    if afs.defaultConfig.moveSolitaryROVols :
        for v in solitaryROVols :
            # get RWVolName
            RWVolName=v['name'][:-len(".readonly")]
            # check for moving osd-volumes
            if v.get("osdPolicy",0) != 0 :
                if not afs.defaultConfig.moveOSDVOlumes : 
                    print "Skipping %s, because it is an OSD-Volume" % v["name"]
                    continue
            # check for minSize
            if minUsage != 0 :
                if int(v.get("diskused")) < minUsage : 
                    print "Skipping %s, because it is smaller than %s" % minUsage 
                    continue
           
            if afs.defaultConfig.ignoreRX != None :
                skip_it=False
                for rx in ignoreRX :
                    if rx.match(RWVolName) : skip_it = True
            elif afs.defaultConfig.onlyRX != None :
                skip_it=True
                for rx in onlyRX :
                    if rx.match(RWVolName) : skip_it = False
            elif afs.defaultConfig.onlyProjects != None :
                skip_it=True
                volProjects=PS.getProjectsByVolumeName(RWVolName)
                for prj in volProjects :
                    if prj.name in afs.defaultConfig.onlyProjects : skip_it = False
            elif afs.defaultConfig.ignoreProjects != None :
                skip_it=False
                volProjects=PS.getProjectsByVolumeName(RWVolName)
                for prj in volProjects :
                    if prj.name in afs.defaultConfig.ignoreProjects : skip_it = True
            else :
                skip_it = False
            if skip_it  : continue

            # remove osd-attributes from dict, create object
            v.pop("filequota")
            v.pop("osdPolicy")
            v["serv_uuid"]=afs.LookupUtil[afs.defaultConfig.CELL_NAME].getFSUUID(v["servername"])
            VolObj.setByDict(v)

            if dstFS == None :
                # get actual stuff from live
                #Vol=VS.getVolume(v["name"],cached=False)
                minNestingLevel=-1 # NestingLevel should be "spezifizitaet"
                for p in PS.getProjectsByVolumeName(RWVolName) :
                    if p.NestingLevel <  minNestingLevel or  minNestingLevel == -1 :
                        minNestingLevel =  p.NestingLevel
                        PrjObj=p
                dstSrv,dstP = PS.getNewVolumeLocation(PrjObj.name,VolObj)
                if dstSrv == None :
                    sys.stderr.write("found no appropriate location for %s. Skipping\n" % VolObj.name)
                    continue
            else :
                dstSrv = dstFS.servernames[0]
                if reqDstPart == None :
                    dstP=None
                    maxFree=0
                    parts=FS.getPartitions(dstSrv)
                    for p in parts :
                        if parts[p]["free"] > maxFree :
                            dstP=p
                            maxFree=parts[p]["free"]
              
                    if dstP == None :
                        sys.stderr.write("found no appropriate partition on server %s for %s. Skipping\n" % (dstSrv,VolObj.name))
                        continue
                else :
                    # check if requested destination is ok
                    dstP=reqDstPart 
                    skip_it= False
                    for rov in VS.getVolGroup(VolObj.name,cached=False)["RO"] :
                        if rov.serv_uuid == dstFS.uuid : 
                            print "Found one existing RO-copy of %s on server %s. Skipping." % (VolObj.name,dstSrv)
                            skip_it = True 
                    if skip_it : continue
                         
            # XXX only move RO, if we don't have enough of them -> auto-healing
            # get RO-Sites of the Volume :
            # the most specific project for this volums counts
            print "Moving solitary RO %s to %s %s" % (v['name'],dstSrv,dstP)
            if not afs.defaultConfig.dryrun :
                VlD.addsite(RWVolName,dstSrv,dstP)
                VD.release(RWVolName)
                VD.remove(v['name'],srcFS.servernames[0],srcP)
            movedVolcount += 1
            if movedVolcount > afs.defaultConfig.maxnum and afs.defaultConfig.maxnum > 0 :
                print "moved %d volumes. Terminating." % afs.defaultConfig.maxnum
                sys.exit(0)

            # check if partition is freed enough
            parts=FS.getPartitions(afs.defaultConfig.ssrv)
            if parts[srcP]["free"] > untilFree and untilFree > 0 :
                print "%s bytes free on spart %s." % (afs.util.afsutil.humanReadableSize(parts[srcP]["free"]),srcP )
                break

