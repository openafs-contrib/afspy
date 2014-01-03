[general]
Cell=ipp-garching.mpg.de
User=
Password=
allDBServs=afs-db1.rzg.mpg.de,afs-db2.aug.ipp-garching.mpg.de,afs-db3.bc.rzg.mpg.de
min_ubikdb_version=1327470000

[DNSConfDAO]
allDBIPs=130.183.100.10,130.183.14.14,130.183.9.5

[BosServerDAO]
server=afs32.rzg.mpg.de
logfile=FileLog
newbinary_restart_time=5:00 am
general_restart_time=sun 4:00 am
superuser=hullafax
db_server=afs-db2.aug.ipp-garching.mpg.de
db_server_clone=afs-db-hgw.ipp-hgw.mpg.de


[CacheManagerDAO]
aliases=rzg=ipp-garching.mpg.de,@cell=ipp-garching.mpg.de,ipp=ipp-garching.mpg.de,mpa=mpa-garching.mpg.de,mpe=mpe.mpg.de,rzg.mpg.de=ipp-garching.mpg.de

[VolService]
VolID=536999539
VolName=test.afs1
minCopy=2
Owner="afspy"
FS=130.183.30.4
FSName=afs1.rzg.mpg.de
Part=a
Type=RW

[FsService]
FS=130.183.30.55
Partitions=a,b,c,d,hs,k,l,s,ha,hg

[BsService]
BS=130.183.30.55
BNodes=fs

[VLDbDAO]
numServ=20

[FileServerDAO]
FS=130.183.30.55
Part=k
allParts=a,b,c,d,k,l,s,ha,hg,hs 

[UbikDAO]
SyncSite=130.183.14.14
DBPort=7002
allDBs=194.94.214.140,194.94.214.4,130.183.100.10,130.183.14.14,130.183.9.5
DBState=OK
MinDBVersion=100000

[CellService]
FS=130.183.30.55
FsUUID=00430d64-8e1b-1cef-b3-f7-371eb782aa77
allDBIPs=194.94.214.140,194.94.214.4,130.183.100.10,130.183.14.14,130.183.9.5
allDBHostnames=afs-db1.rzg.mpg.de,afs-db2.aug.ipp-garching.mpg.de,afs-db3.bc.rzg.mpg.de,afs-hgw1.ipp-hgw.mpg.de,afs-db-hgw.ipp-hgw.mpg.de
numFSs=44
MinUbikDBVersion=1000

[VolumeDAO]
FS=130.183.30.4
Part=a
VolID=536999539
numVols=1

[ProjectService]
VolID=536985805
ProjectName=MPE INTEGRAL
ProjectID=1
ProjectIDs=1,3

[LookupUtil]
HostAlias=jack.ipp-hgw.mpg.de
primaryHostName=afs-db-hgw.ipp-hgw.mpg.de
IPAddr=194.94.214.140
FsUUID=00274cf0-5006-1460-b9-d9-8cd65ec2aa77

