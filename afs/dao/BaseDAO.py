"""
base class for all DAOs :
initializes logging.
declares decorators.
deals with actual execution of commands
"""
import afs
import inspect
import logging
import subprocess


class ExecError(BaseException):
    """custom exception for executing shell commands."""

    def __init__(self, message, stack = None):
        BaseException.__init__(self, message)
        self.message   = message
        if stack != None :
            self.stack = stack
        else :
            self.stack = []

    def __str__(self):
        return repr(self.message)
       

def exec_wrapper(func) :
    """
    This decorator is intended for all DAO-methods.
    The DAO-method itself is just compiling the CMDList to execute,
    and returns the appropriate parsing function and all info this
    parsing function needs.
    Hooks for Auth checking are in place, but unused.
    Warning: if the interpreter complains 
    got multiple values for keyword argument _cfg, then you're
    passing a positional argument, which should not be there.
    """

    def wrapped(self, *args, **kwargs):
        """actual wrapper code"""

        self.logger.debug("%s: entering with  self=%s, args=%s, kwargs=%s" \
            % (self, func.__name__, args, kwargs))

        # kwarg  _user is not passed to DAO
        if not kwargs.has_key("_user") :
            _user = ""
        else :
            _user = kwargs["_user"]
            kwargs.pop("_user")

        # kwarg _cfg must be passed to DAO
        if not kwargs.has_key("_cfg") :
            self.logger.debug("injecting default config.")
            kwargs["_cfg"] = afs.CONFIG

        # here we should check the authorisation
        self.logger.debug(\
            "should check auth of user=%s for method %s in class %s"\
             % (_user, func.__name__, self.__class__.__name__))

        # get cmdlist and parsefunction from method
        # parse_fct is parsing the output of the executed function
        # ParseInfo are any info the parse_fct requires beside ret,
        # outout and outerr 
        parse_parameterlist = {"args" : args, "kwargs" : kwargs } 
        argspec = inspect.getargspec(func)
         
        self.logger.debug("argspec=%s" % (argspec,))

        count = 0
        if argspec[3] != None : 
            for key in argspec[0][-len(argspec[3]):] :
                self.logger.debug("checking argspec key=%s" % key)
                value = argspec[3][count]
                self.logger.debug("value=%s" % value)
                count += 1
                if not parse_parameterlist["kwargs"].has_key(key) :
                    parse_parameterlist["kwargs"][key] = value

        self.logger.debug("args=%s" % (args,))
        self.logger.debug("kwargs=%s" % (kwargs,))
        self.logger.debug("parse_parameterlist=%s" % (parse_parameterlist,))

        cmd_list, parse_fct = func(self, *args, **kwargs) 
       
        # do really execute the call
        if self.implementation == "childprocs" :
            ret, output, outerr = self.execute(cmd_list)
        elif self.implementation == "detached" :
            job_handle = self.execute_detached(cmd_list)
            self.logger.debug("should put job_handle %s into job_manager" \
                % job_handle)

        # parse the result
        self.logger.debug(\
        "calling parse_fct %s with %s, %s, %s, %s" \
            % (parse_fct.__name__, ret, output[:10],\
               outerr[:10], parse_parameterlist))
        result = parse_fct(ret, output, outerr, \
            parse_parameterlist, self.logger)
        self.logger.debug("%s: returning %s..." % (func.__name__, result))
        return result

    return wrapped
 
class BaseDAO(object) :
    """
    The mother of all DAOs
    """
    
    def __init__(self, implementation="childprocs") :
        """initializes logger and sets implementation"""

        class_loglevel = getattr(afs.CONFIG,"loglevel_%s" \
            % self.__class__.__name__, "").upper()
        numeric_loglevel = getattr(logging, class_loglevel, 0)
        self.logger = logging.getLogger("afs.dao.%s" % self.__class__.__name__)
        self.logger.setLevel(numeric_loglevel)
        self.logger.debug("initializing %s-Object" % (self.__class__.__name__))
        self.implementation = implementation
        return
        
    def execute(self, cmd_list, stdin = "") :
        """executes shell command as subprocess"""

        self.logger.info("executing command: '%s'" % ' '.join(cmd_list))

        if stdin == "" :
            pipo = subprocess.Popen(cmd_list, stdout = subprocess.PIPE, \
                 stderr = subprocess.PIPE)
            _output, _outerr = pipo.communicate()
        else :
            pipo = subprocess.Popen(cmd_list, stdin = subprocess.PIPE, \
                stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            _output, _outerr = pipo.communicate(stdin)

        if pipo.returncode != 0 :
            if pipo.returncode == 13 : # permission denied
                return 13, "","Permission denied"
            for line in _output + _outerr :
                if "not authorized" in line.lower() :
                    return 13, "","Permission denied"
            raise ExecError("cmd: \"%s\" failed with ret=%d and stderr=%s\n" % \
                (' '.join(cmd_list), pipo.returncode, _outerr))
    
        # get rid of whitespace
        output = []
        for line in _output.split("\n") :
            line = line.strip()
            if line == "" : 
                continue
            output.append(line)
    
        outerr = []
        for line in _outerr.split("\n") :
            line = line.strip()
            if line == "" : 
                continue
            outerr.append(line)

        self.logger.debug(\
             "returning (ret, output[:10], outerr[:10] to 10 lines ) %s" %\
             ((pipo.returncode, output[:10], outerr[:10]), ))

        return pipo.returncode, output, outerr

    def execute_detached(self, job_sissy, cmd_list, stdin = "") :
        """
        executes shell command using pyJobSissy
        to be implemented.
        returns handle for getting information about the job
        """

        self.logger.info(\
        "sending command: '%s' with and sdtin=%s to job_sissy at %s" % \
        (' '.join(cmd_list), stdin, job_sissy))
        job_handle = None
        return job_handle 
