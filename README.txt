===========
afspy
===========

afspy are (as the name suggests) python bindings to AFS, here
in the implementation of openAFS.
It provides a high-level interface to AFS.
Also, database-cacheing of information is supported.
Asynchronous and detached access to AFS is planned so that 
an application using afspy remains responsive at all times.

Layout 
======

The different parts of this package are :

* afs/ : The actual module

* afs/dao/ : low-level internal interface

* afs/service/ : high-level interface

* afs/model/ : object declarations

* afs/orm/ : object-relational-mapping functionality used fo DB-Cache 

* afs/util/ : helper functions

* tests/ : unit-tests, requires some configuration to run in your cell

Usage
=====

You can start an interactive python shell 
Interactively:
PYTHONSTARTUP=<PATH/TO/AFS-Module>/etc/pythonstartup python

in scripts:

see examples


Configuration
=============

Config options are read as :
1. read system wide configuration file:
   Path is hard-coded in module

2. read user's personal $HOME/.config/afspy

3. read config file given on command line

4. use options given on command line

Later definitions override earlier ones.
This configuration is stored in a AfsConfig-object.
and passed to any service called by default.

Contents of the AfsConfig
========================

* Credential to use 

* default AFS Cellname

* default Keberos REALM

* DAO-implementation to use

* DB-implementation to use.

* Logging. There are two types of Loglevels,

  * the global one for all modules : 
     e.g.  globalLogLevel="[debug|info|warn|critical]"
  * a class local one to override the global one for certain classes.
    CSV list of Classname=Loglevel pairs:
    e.g. classLogLevels="CellService=warn,UbikPeerDAO=warn,FileServerDAO=debug"
    beside the normal classes, also "util" and "sqlalchemy" are available.

DB-Cacheing
===========

If the option DB_CACHE is set to True.
A connection to the configured DB is set up 
and stored in the AfsConfig-Object.
Every service creates its own session, so that any created Object is attached
to the DB-Cache as long as the service is alive.
