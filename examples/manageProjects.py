#!/usr/bin/python

import sys,os,argparse,string,json,re,logging
from ConfigParser import ConfigParser
from types import ListType

import afs
from afs.util.AfsConfig import parseDefaultConfig
import afs.util.afsutil as afsutil
from afs.util.DBManager import DBManager
from afs.service.OSDVolService import OSDVolService
from afs.service.CellService import CellService
from afs.service.OSDFsService import OSDFsService
from afs.service.ProjectService import ProjectService
from afs.model.Project import Project
from afs.model.Partition import Partition
from afs.model.ExtendedVolumeAttributes import ExtVolAttr


global CellInfo

def getProjDetailsFromKeyboard(defaultDict) :
    for key in defaultDict :
        # do not ask for DB-internal stuff
        if key in ["id","cdate","udate","sync"] : continue 
        defaultValue=defaultDict[key]
        # manage "CSV" lists, actual separator is "\r\n"
        if key in ["volnameRegEx","excludedVolnames","additionalVolnames","rw_locations","ro_locations","rw_serverparts","ro_serverparts"] : 
            defaultDict[key]=""
            count = 0 
            if defaultValue :
                defaultList=defaultValue
            else :
                defaultList=[]
            resultList=[]
            while 1:
                if len(defaultList) > count :
                    defaultElement=defaultList[count]
                    count += 1
                else :
                    defaultElement=""
                if "serverparts" in key and defaultElement != "" :
                    uuid,part=defaultElement
                    FsName=afsutil.getHostnameByFSUUID(uuid)
                    defaultElement = "{0}_{1}".format(FsName,part)
                    
                givenValue=raw_input("{0} [{1}] : ".format(key,defaultElement))
                if givenValue == "--" : continue
                if givenValue == "---" : break
                if givenValue == "" : givenValue = defaultElement
                # if still empty value, break
                if givenValue == "" : break
                # mangle input wrt to key
                if "serverparts" in key :
                    server,part=givenValue.strip().split("_")
                    # get servername
                    server=afsutil.getDNSInfo(server)[0][0]
                    uuid=afsutil.getFSUUIDByName_IP(server,None)
                    resultList.append([uuid,part])
                else :
                    resultList.append(givenValue)
            defaultDict[key]=resultList
        else :
            givenValue=raw_input("{0} [{1}] : ".format(key,defaultValue))
            if givenValue == "" : givenValue = defaultValue 
            defaultDict[key]=givenValue
    return defaultDict



myParser=argparse.ArgumentParser(parents=[afs.argParser], add_help=False)
myParser.add_argument("--prjname", default="", help="projectname")
Commands=myParser.add_mutually_exclusive_group(required=True)
Commands.add_argument('--dumpPrj', action='store_true')
Commands.add_argument('--importPrj', action='store_true')
Commands.add_argument('--addPrj', action='store_true')
Commands.add_argument('--rmPrj', action='store_true')
Commands.add_argument('--modifyPrj', action='store_true')
Commands.add_argument('--showFSList', action='store_true')
Commands.add_argument('--updateVolumeMappings', action='store_true')
Commands.add_argument('--showServerSpread', action='store_true')
Commands.add_argument('--updateServerSpread', action='store_true')
Commands.add_argument('--showStorageUsage', action='store_true')

parseDefaultConfig(myParser)

CS=CellService()
VS=OSDVolService()
FsS=OSDFsService()
PS=ProjectService()
DBM=DBManager()

CellInfo=CS.getCellInfo(cached=True)
CellInfo.FileServers=CellInfo.FileServers
PrjObj = Project()
defaultDict=PrjObj.getDict()

#
#
# dump/import :
# for serverpartitions, tranlsate for dump into human readable.
# also dump raw server-uuids. 
# for import only consider human readable
# but fail if we find no UUID for the hostname
if afs.defaultConfig.dumpPrj == True :
    for p in PS.getProjectList() :
        if afs.defaultConfig.prjname != "" and p.name != afs.defaultConfig.prjname : continue
        d=p.getDict()
        if afs.defaultConfig.prjname != ""  and afs.defaultConfig.prjname !=  d["name"] : continue 
        print "========================================"
        print "name: {0}".format(d["name"])
        for k in d :
            if k in [ "name", "ignAttrList" ] : continue
            if k in [ "rw_serverparts","ro_serverparts" ] :
                translatedList=[]
                for FSUUID,Part in d[k] :
                    FSName=afs.LookupUtil[afs.defaultConfig.CELL_NAME].getHostnameByFSUUID(FSUUID)
                    translatedList.append([FSName,Part])
                print "{0}_human: {1}".format(k,translatedList)
                print "{0}_raw: {1}".format(k,d[k])
            else :
                print "{0}: {1}".format(k,d[k])
    print "========================================"
elif afs.defaultConfig.importPrj == True :
    input=sys.stdin.readlines() 
    count=0
    thisPrj={}
    while 1 :
        if count >= len(input) : break
        line=input[count].strip()
        if len(line) == 0 : 
            count += 1
            continue
        if "===" in line :  # we are at the beginning of a new project, so save the old one
            if len(thisPrj) != 0 : # safeguard
                # fix serverparts....
                for sps in ["rw_serverparts_human", "ro_serverparts_human"] :
                    serverparts=thisPrj[sps] 
                    realKey=sps[:-6]
                    thisPrj[realKey] = []
                    for FSName,Part in serverparts :
                        FSUUID=afs.LookupUtil[afs.defaultConfig.CELL_NAME].getFSUUID(FSName)
                        if FSUUID == None :
                           sys.exit("Import Error: Cannot find server uuid for %s" % FSName)
                        thisPrj[realKey].append([FSUUID,Part])
                for k in ["rw_serverparts_human","ro_serverparts_human","rw_serverparts_raw","ro_serverparts_raw"]  :
                    thisPrj.pop(k)
                PrjObj = Project()
                # id is in the dump, so we don't need to fetch it from database 
                PrjObj.setByDict(thisPrj)
                PS.saveProject(PrjObj)
                thisPrj={}
                print ("Successfully imported Project %s" % PrjObj.name)
            count += 1
            if count >= len(input) : break
            line=input[count].strip()
            tokens=line.split(":")
            tokens=map(string.strip,tokens)
            thisPrj["name"]=tokens[1]
            count +=1
            continue
        tokens=line.split(":")
        tokens=map(string.strip,tokens)
        if tokens[0] in defaultDict.keys()+["rw_serverparts_human","ro_serverparts_human","rw_serverparts_raw","ro_serverparts_raw"] :
           # list 
           if tokens[0] in ["volnameRegEx","excludedVolnames","additionalVolnames","rw_locations","ro_locations","rw_serverparts_human","ro_serverparts_human"] :
               thisPrj[tokens[0]]=eval(tokens[1]) 
               count += 1
           else :
               thisPrj[tokens[0]]=tokens[1]
               count += 1
        else :
            print "Cannot parse : %s " % line
            sys.exit(0)
elif afs.defaultConfig.addPrj == True :
    defaultDict=PrjObj.getDict()
    PrjDict=getProjDetailsFromKeyboard(defaultDict=defaultDict)
    PrjObj.setByDict(PrjDict)
    print "PrjObj: %s " % PrjObj
    PS.saveProject(PrjObj)
elif afs.defaultConfig.rmPrj == True :
    if afs.defaultConfig.prjname == "" :
        name=raw_input("Name of project: ")
    else :
        name=afs.defaultConfig.prjname
    if PS.getProjectByName(name) == None :
        print "Found no project with name '%s'" % name
    PS.deleteProject(name)
elif afs.defaultConfig.modifyPrj == True :
    if afs.defaultConfig.prjname == "" :
        name=raw_input("Name of project: ")
    else :
        name=afs.defaultConfig.prjname
    oldPrjDict=PS.getProjectByName(name).getDict()
    PrjDict=getProjDetailsFromKeyboard(defaultDict=oldPrjDict)
    PrjObj.setByDict(PrjDict)
    PS.saveProject(PrjObj)
elif afs.defaultConfig.showFSList == True :
    for f in CellInfo.FileServers :
       print f
elif afs.defaultConfig.updateVolumeMappings == True :
    PS.updateVolumeMappings()
elif afs.defaultConfig.updateServerSpread == True :
    print "updateServerSpread"
    for p in PS.getProjectList() :
        if afs.defaultConfig.prjname != ""  and afs.defaultConfig.prjname !=  p.name : continue 
        print p.name
        PS.getServerSpread(p.name,cached=False)
elif afs.defaultConfig.showServerSpread == True :
    if afs.defaultConfig.prjname == "" :
        name=raw_input("Name of project: ")
    else :
        name=afs.defaultConfig.prjname
    thisPrj=PS.getProjectByName(name)
    if thisPrj == None :
        print "Unknown project: %s" % name
        sys.exit(1)
    print "ServerSpread of Project %s" % name
    print "=========================="
    AS = PS.getAssignedServers(name)
    SS = PS.getServerSpread(name,cached=True)
    for vol_type in ["RW", "RO", "BK" ] :
        print vol_type 
        for s in SS[vol_type] :
            print "%s %s : %s " % (afs.LookupUtil[afs.defaultConfig.CELL_NAME].getHostnameByFSUUID(s.serv_uuid),s.part,s.num_vol )
elif afs.defaultConfig.showStorageUsage == True :
    print "command: showStorageUsage"
    if afs.defaultConfig.prjname == "" : 
        prjRX=re.compile(".*")
    else :
        try :
            prjRX=re.compile(afs.defaultConfig.prjname)
        except :
            sys.stderr.write("Invalid Prjname regex %s" % afs.defaultConfig.prjname)
            sys.exit(1)
    total_numVol = 0
    total_files_fs = 0
    total_files_osd = 0
    total_blocks_fs = 0.0
    total_blocks_osd_on = 0.0
    total_blocks_osd_off = 0.0
    summedPrjs=[]
    for p in PS.getProjectList() :
        pDict=p.getDict()
        if prjRX.match(pDict["name"]) : 
            summedPrjs.append(pDict["name"])
            VolIDList=PS.getVolumeIDs(pDict["name"])
            StorageUsage=PS.getStorageUsage(pDict["name"])
            total_numVol += len(VolIDList)
            total_files_fs += StorageUsage["files_fs"]
            total_files_osd += StorageUsage["files_osd"]
            total_blocks_fs += float(StorageUsage["blocks_fs"])
            total_blocks_osd_on += float(StorageUsage["blocks_osd_on"])
            total_blocks_osd_off += float(StorageUsage["blocks_osd_off"])
            print "Project %s storage usage:" % pDict["name"]
            print "========================="
            print "Total number of Volumes : %d" % len(VolIDList)
            print "RW Volumes:"
            print "on fileserver: %f TB in %d files " % (float(StorageUsage["blocks_fs"])/1024/1024/1024/1024,StorageUsage["files_fs"])
            print "numFiles in osd = %d" % StorageUsage["files_osd"]
            print "on osd-server (online): %f TB" % (float(StorageUsage["blocks_osd_on"])/1024/1024/1024/1024)
            print "on archival server (offline): %f TB" % (float(StorageUsage["blocks_osd_off"])/1024/1024/1024/1024)
            print
            print "%s\t%s\t%s\t%s\t%s\t" % (pDict["name"],len(VolIDList),float(StorageUsage["blocks_fs"])/1024/1024/1024/1024,float(StorageUsage["blocks_osd_on"])/1024/1024/1024/1024,float(StorageUsage["blocks_osd_off"])/1024/1024/1024/1024)
            print
            print
    print "Total storage usage for projects %s :" % string.join(summedPrjs, ",")
    print "========================="
    print "Total number of Volumes : %d" % total_numVol
    print "RW Volumes:"
    print "on fileserver: %f TB in %d files " % (float(total_blocks_fs)/1024/1024/1024/1024,total_files_fs)
    print "numFiles in osd = %d" % total_files_osd
    print "on osd-server (online): %f TB" % (float(total_blocks_osd_on)/1024/1024/1024/1024)
    print "on archival server (offline): %f TB" % (float(total_blocks_osd_off)/1024/1024/1024/1024)
    print
    print
    print "%s\t%s\t%s\t%s\t%s\t" % ("Total",total_numVol,float(total_blocks_fs)/1024/1024/1024/1024,float(total_blocks_osd_on)/1024/1024/1024/1024,float(total_blocks_osd_off)/1024/1024/1024/1024)
else :
    print "unknown command." 
