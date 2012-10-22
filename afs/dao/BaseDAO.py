import logging,inspect
import string,os,sys
import subprocess,types
import tempfile
import afs
from afs.exceptions.AfsError import AfsError


class ExecError( BaseException):
    def __init__(self, message, stack=[]):
        BaseException.__init__(self, message)
        self.message   = message
        self.stack = stack

    def __str__(self):
      #FIXME parse build a complete message with stack
      return repr(self.message)
       

def execwrapper(fn) :
    """
    This decorator is intended for all DAO-methods.
    The method itself is just compiling the CMDList to execute,
    and returns the appropriate parsing function and all Info this
    parsing function needs.
    Hooks for Auth checking are in place.
    """
    def wrapped(self,*args,**kwargs):
        if not kwargs.has_key("_user") :
            raise AfsError("Internal error. No _user= given in parameterlist")
        else :
            _user=kwargs["_user"]
            kwargs.pop("_user")
        if not kwargs.has_key("_cfg") :
            raise AfsError("Internal error. No _cfg= given in parameterlist")
        else : 
            _cfg=kwargs["_cfg"]
        self.Logger.debug("should check auth of user=%s for method %s in class %s" % (_user,fn.__name__,self.__class__.__name__))
        # get cmdlist and parsefunction from method
        self.Logger.debug("%s: entering with  self=%s, args=%s, kwargs=%s" % (self,fn.__name__,args,kwargs))
        # ParseFct is parsing the output of the executed function
        # ParseInfo are any info the ParseFct requires beside rc, outout and outerr 
        parseParamList={"args" : args, "kwargs" : kwargs } 
        argspec=inspect.getargspec(fn)
        for a in range(len(argspec[0])-len(argspec[3])) :
            k = argspec[0][a+len(argspec[0])-len(argspec[3])]
            v = argspec[3][a]
            if not parseParamList["kwargs"].has_key(k) :
                parseParamList["kwargs"][k]=v
        CmdList,ParseFct=fn(self,*args, **kwargs) 
        if self.Implementation == "childprocs" :
            rc,output,outerr=self.execute(CmdList)
        elif self.Implementation == "detached" :
            jobinfo=self.execute_detached(CmdList)
            self.Logger.debug("should put jobinfo %s into jobmanager" % jobinfo)
        self.Logger.debug("calling ParseFct %s with rc=%s, output=%s,outerr=%s,parseParamList=%s" % (ParseFct.__name__,rc,output[:10],outerr[:10],parseParamList))
        result=ParseFct(rc,output,outerr,parseParamList,self.Logger)
        self.Logger.debug("%s: returning %s..." % (fn.__name__,result))
        return result
    return wrapped
 
class BaseDAO(object) :
    
    """
    The mother of all DAOs
    """
    
    def __init__(self, Implementation="childprocs" ) :
        # LOG INIT
        classLogLevel = getattr(afs.defaultConfig,"LogLevel_%s" % self.__class__.__name__, "").upper()
        numericLogLevel = getattr(logging,classLogLevel, 0)
        self.Logger=logging.getLogger("afs.dao.%s" % self.__class__.__name__)   
        self.Logger.setLevel(numericLogLevel)
        self.Logger.debug("initializing %s-Object" % (self.__class__.__name__))
        self.Implementation=Implementation
        return
        
    def execute(self,CmdList,  env={}, Input="", stdout=None, stderr=None) :
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
            for line in _output + _outerr :
                if "not authorized" in line.lower() :
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
        # XXX magic constant here
        self.Logger.debug("returning (truncateed to 10 lines in output, outerr) %s" % ( (pipo.returncode, output[:10], outerr[:10]), ))
        return pipo.returncode,output,outerr

    def execute_detached(self,CmdList, SpoolDir, env={}, Input="") :
        self.Logger.info("executing detached command: '%s'" % string.join(CmdList, " "))
        outFile=tempfile.NamedTemporaryFile(prefix=SpoolDir, delete=False)
        errFile=file(outFile.name, "w+")
        self.Logger.info("detaching and redirecting to file '%s' and '%s.err'" % (outFile.name, errFile.name) )
        
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
        self.Logger.debug("returning %s" % ( (rc, output, outerr), ))
        return rc,output,outerr

    def safeStrip(self,Thing) :
        if type(Thing) == types.StringType :
            return Thing.strip()
        return  
