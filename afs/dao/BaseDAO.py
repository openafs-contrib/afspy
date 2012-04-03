import logging
import string,os,sys
import subprocess,types
import tempfile, traceback

class ExecError( BaseException):
    def __init__(self, message, stack=[]):
        BaseException.__init__(self, message)
        self.message   = message
        self.stack = stack

    def __str__(self):
      #FIXME parse build a complete message with stack
      return repr(self.message)
      
class BaseDAO(object) :
    
    """
    The mother of all DAOs
    """
    
    def __init__(self) :
        # LOG INIT
        self.Logger=logging.getLogger("afs.dao.%s" % self.__class__.__name__)
        # we would like to have DAO directly useable
        # thus, just try to setup logging from config, do not force it
        try :
            import afs
            if afs.defaultConfig.classLogLevels.has_key(self.__class__.__name__) :
                numeric_level = getattr(logging,afs.defaultConfig.classLogLevels[self.__class__.__name__].upper() , None)
            else :
                numeric_level = getattr(logging,afs.defaultConfig.globalLogLevel.upper(), None)
            self.Logger.setLevel(numeric_level)
            self.Logger.debug("initializing %s-Object" % (self.__class__.__name__))
        except :
            pass
        return
        
    def execute(self,CmdList,  env={}, Input="", stdout=None, stderr=None) :
        tb=traceback.extract_stack()
        moduleName=tb[len(tb)-2][0].split("/")[-1:][0]
        self.Logger.debug("BaseDAO.execute called from %s.%s from %s:%s" % (self.__class__.__name__,tb[len(tb)-2][2], moduleName,  tb[len(tb)-2][1]))
        self.Logger.debug("method %s.%s called from %s.%s from %s:%s" % (self.__class__.__name__, tb[len(tb)-2][2], self.__class__.__name__,tb[len(tb)-3][2], moduleName,  tb[len(tb)-3][1]))
        self.Logger.info("executing command: '%s'" % string.join(CmdList, " "))
        if stdout == None :
            stdout=subprocess.PIPE
        if stderr == None :
            stderr = subprocess.PIPE

        if Input == "" :
            pipo=subprocess.Popen(CmdList,stdout=stdout,stderr=stderr, env=env)
            _output,_outerr=pipo.communicate()
        else :
            pipo=subprocess.Popen(CmdList,stdin=subprocess.PIPE, stdout=stdout,stderr=stderr, env=env)
            _output,_outerr=pipo.communicate(Input)
        if pipo.returncode != 0 :
            if pipo.returncode == 13 : # permission denied
                return 13, "","Permission denied"
            if "not authorized" in _output.lower() or  "not authorized" in _outerr.lower()  :
                return 13, "","Permission denied"
            raise ExecError("cmd: \"%s\" failed with rc=%d and stderr=%s\n" % (string.join(CmdList),pipo.returncode, _outerr))
    
        # get rid of whitespace
        _output=map(self.safeStrip,_output.split("\n"))
        _outerr=map(self.safeStrip,_outerr.split("\n"))
    
        output=[]
        for line in _output :
            if line == "" : continue
            output.append(line)
    
        outerr=[]
        for line in _outerr :
            if line == "" : continue
            outerr.append(line)
        self.Logger.debug("Leaving BaseDAO.execute called from %s:%s and returning %s" % (self.__class__.__name__, tb[len(tb)-2][2], (pipo.returncode, output, outerr)))
        return pipo.returncode,output,outerr

    def execute_detached(self,CmdList, SpoolDir, env={}, Input="") :
        tb=traceback.extract_stack()
        moduleName=tb[len(tb)-2][0].split("/")[-1:][0]
        self.Logger.debug("BaseDAO.execute_detached called from %s.%s from %s:%s" % (self.__class__.__name__,tb[len(tb)-2][2], moduleName,  tb[len(tb)-2][1]))
        self.Logger.info("executing command: '%s'" % string.join(CmdList, " "))
        outFile=tempfile.NamedTemporaryFile(prefix=SpoolDir, delete=False)
        errFile=file(outFile.name, "w+")
        self.Logger.info("detaching redirecting to file '%s' and '%s.err'" % (outFile.name, errFile.name) )
        
        ## partly from {{{ http://code.activestate.com/recipes/66012/ (r1)
        ## and stuff from comments.
        ## the second fork is done in execute() itself.
        # do the UNIX double-fork magic, see Stevens' "Advanced 
        # Programming in the UNIX Environment" for details (ISBN 0201563177)
        try: 
            pid = os.fork() 
            if pid > 0:
                # exit first parent,close Files here
                outFile.close()
                errFile.close()
                sys.exit(0) 
        except OSError, e: 
            errFile.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror) )
            sys.exit(1)

        # decouple from parent environment
        os.chdir(SpoolDir) 
        os.setsid() 
        os.umask(127) 
        
        # flush and redirect i/o-streams
        dev_null = file('/dev/null', 'r')
        sys.stdout.flush()
        sys.stderr.flush()
        os.dup2(outFile.fileno(), sys.stdout.fileno())
        os.dup2(errFile.fileno(), sys.stderr.fileno())
        os.dup2(dev_null.fileno(), sys.stdin.fileno())
        ## end of http://code.activestate.com/recipes/66012/ }}}
   
        rc, output, outerr=self.execute(CmdList, env=env, Input=Input, stdout=outFile, stderr=errFile)
        self.Logger.debug("Leaving BaseDAO.execute_detached called from %s:%s and returning %s" % ( self.__class__.__name__,tb[len(tb)-2][2], (rc, output, outerr)))
        return rc,output,outerr

    def safeStrip(self,Thing) :
        if type(Thing) == types.StringType :
            return Thing.strip()
        return  
