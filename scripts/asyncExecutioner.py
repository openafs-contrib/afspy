#!/usr/bin/python 
"""
non-threaded intermediate process to
create a completely detached process
"""

import os,sys
import subprocess, types


if __name__ == "__main__" :

    if len(sys.argv) < 3 :
        sys.stderr.write("usage: %s <Spoolfile> <command-list>+\n")
        sys.exit(0)
    SpoolFile=sys.argv[1]
    CmdList=sys.argv[2:]
        
    ## partly from {{{ http://code.activestate.com/recipes/66012/ (r1)
    ## and stuff from comments.
    ## note that we return to calling application
    # do the UNIX double-fork magic, see Stevens' "Advanced 
    # Programming in the UNIX Environment" for details (ISBN 0201563177)
    try: 
        pid = os.fork() 
        if pid > 0:
            sys.exit(0)
    except OSError as e: 
        sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror) )
        sys.exit(1)
        
    # decouple from parent environment
    os.setsid() 
    os.umask(127) 
    
    outFile=open(SpoolFile+".out", "w+")
    errFile=open(SpoolFile+".err", "w+")
    
    # flush and redirect i/o-streams
    dev_null = open('/dev/null', 'r')
    sys.stdout.flush()
    sys.stderr.flush()
    os.dup2(outFile.fileno(), sys.stdout.fileno())
    os.dup2(errFile.fileno(), sys.stderr.fileno())
    os.dup2(dev_null.fileno(), sys.stdin.fileno())
    
    # close all filedescriptors
    
    # do second fork
    try: 
        pid = os.fork() 
        if pid > 0: # exit immediatly from intermediate process
            sys.exit(0) 
    except OSError as e: 
        errFile.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror) )
        sys.exit(1)
    ## end of http://code.activestate.com/recipes/66012/ }}}
    
    #  careful with logs here, they all end up in the stderr file
    # self.Logger.info("# executing detached command: '%s'" % " ".join(CmdList ))
    # execute command
    pipo=subprocess.Popen(CmdList,stdout=outFile,stderr=errFile)
    pidFile=open(SpoolFile + ".pid", "w+")
    pidFile.write(str(pipo.pid)+"\n")
    pidFile.close()
    _output,_outerr=pipo.communicate()
    rcFile=open(SpoolFile+".rc", "w+")
    rcFile.write(str(pipo.returncode)+"\n")
    rcFile.close()
    outFile.close()
    errFile.close()
    sys.exit(0)
