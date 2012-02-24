import logging
import string,os,sys
import subprocess,types


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
    
    def __init__(self):
        # LOG INIT
        LogExtra={'classname' : self.__class__.__name__}
        Logger=logging.getLogger("afs.dao.%s" % self.__class__.__name__)
        self.Logger=logging.LoggerAdapter(Logger,LogExtra)
        # we would like to have DAO directly useable
        # thus, just try to setup logging
        try :
            import afs
            if afs.defaultConfig.classLogLevels.has_key(self.__class__.__name__) :
                numeric_level = getattr(logging,afs.defaultConfig.classLogLevels[self.__class__.__name__].upper() , None)
            else :
                numeric_level = getattr(logging,afs.defaultConfig.globalLogLevel.upper(), None)
            Logger.setLevel(numeric_level)
            self.Logger.debug("initializing %s-Object" % (self.__class__.__name__))
        except :
            pass
        return
        
    def execute(self,CmdList, Input="", env={}) :
        self.Logger.info("executing command: '%s'" % string.join(CmdList, " "))
        if Input == "" :
            pipo=subprocess.Popen(CmdList,stdout=subprocess.PIPE,stderr=subprocess.PIPE, env=env)
            _output,_outerr=pipo.communicate()
        else :
            pipo=subprocess.Popen(CmdList,stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE, env=env)
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
        return pipo.returncode,output,outerr

    def safeStrip(self,Thing) :
        if type(Thing) == types.StringType :
            return Thing.strip()
        return  
