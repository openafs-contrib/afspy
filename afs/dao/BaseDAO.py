"""
base class for all DAOs :
initializes logging.
and Executor-class
deals with actual execution of commands
"""
import afs
import inspect
import logging
import os
import random
import shutil
import subprocess
import time

class BaseDAO :
    """
    The mother of all DAOs
    """
    
    def __init__(self) :
        """initializes logger and async housekeeping"""

        class_loglevel = getattr(afs.CONFIG,"LogLevel_%s" \
            % self.__class__.__name__, "").upper()
        numeric_loglevel = getattr(logging, class_loglevel, 0)
        self.logger = logging.getLogger("afs.dao.%s" % self.__class__.__name__)
        self.logger.setLevel(numeric_loglevel)
        self.logger.debug("initializing %s-Object" % (self.__class__.__name__))
        self.spool_dir = "%s/%s" % (afs.CONFIG.SpoolDirBase, self.__class__.__name__)
        if not os.path.exists(afs.CONFIG.SpoolDirBase) :
            try :
                os.makedirs(afs.CONFIG.SpoolDirBase) 
            except :
                raise RuntimeError("Cannot create SpoolDirBase %s. Please check your configuration." % afs.CONFIG.SpoolDirBase)
                 
        # create spool dir
        count = 0
        while 1 :
            if os.path.exists(self.spool_dir) :
                count += 1 
                self.spool_dir = "%s/%s-%d" % (afs.CONFIG.SpoolDirBase, self.__class__.__name__, count)
            else :
                os.mkdir(self.spool_dir)
                break

        # Async INIT
        # dict of active jobs in this service
        # is of form [sp_idant] = {"parse_fct" : , "parse_parameterlist": , "cmd_list": , "timeout" :, "start_time" : }
        self.active_subprocesses = {}
        # dict of for [sp_ident] = result_obj 
        self.finished_subprocesses = {}
        return

    def check_subprocesses(self) :
        """
        checks for finished active_subprocesses and parses them
        """ 
        for sp_ident in self.active_subprocesses :
            if not os.path.exists("%s/%s.rc" % (self.spool_dir, sp_ident ) ) : continue
            self.finished_subprocesses[sp_ident] = self.get_subprocess_result(sp_ident)
            self.active_subprocesses.pop(sp_ident)


    def wait_for_subprocess(self, sp_ident)  :
        """
        wait in a blocking manner for a specific subprocess to finish 
        timeout 
        """
        # check if sp_ident should be running at all.
        if not sp_ident in self.active_subprocesses.keys() :
            self.logger.error("No active subprocess with sp_ident %s." % sp_ident)
            return None

        # check if sp_ident has spool files at all
        # but first wait one scond
        while 1 :
            if not os.path.exists("%s/%s.pid" % (self.spool_dir, sp_ident) ) :
                if ( time.mktime(time.localtime())  - self.active_subprocesses[sp_ident]["start_time"] ) > self.active_subprocesses[sp_ident]["timeout"] :
                    raise RuntimeError("Internal Error. Cannot find pid-file for subprocess %s." % (sp_ident) )
                time.sleep(0.1)
            else :
                break

        rc = -1
        now = time.mktime(time.localtime())
        while 1 :
            if os.path.exists("%s/%s.rc" % (self.spool_dir, sp_ident ) ) :
                f = file("%s/%s.rc" % (self.spool_dir, sp_ident ), "r")
                try :
                    rc = int(f.readline().strip())
                except :
                    raise RuntimeError("Internal Error. Cannot read rc-file for subprocesses %s" % (sp_ident))
                f.close()
                break
            time.sleep(0.1)
            if ( time.mktime(time.localtime()) - now ) > self.active_subprocesses[sp_ident]["timeout"] :
                 raise RuntimeError("Timeout. Subprocess %s with cmd_list %s exceeded timeout of %s secs." % (sp_ident, self.active_subprocesses[sp_ident][0], timeout) )
        return rc
 
    def get_subprocess_result(self, sp_ident) :
        """
        retrieve results and clean up spool-files
        """
        if not sp_ident in self.active_subprocesses.keys() :
            self.logger.error("No active subprocess with sp_ident %s." % sp_ident)
            return None

        raw_result = {}
        for suffix in ["rc","out", "err", "pid" ] :
            f = file("%s/%s.%s" % (self.spool_dir, sp_ident, suffix))
            while 1 :
                line = f.readline()
                if not line : break
                # get rid of whitespace
                line = line.strip()
                if line == "" : 
                    continue
                if not suffix in raw_result.keys() :
                    raw_result[suffix] = [ line.strip() ]
                else :
                    raw_result[suffix].append(line.strip())
            f.close()
            os.unlink("%s/%s.%s" % (self.spool_dir, sp_ident, suffix)) 

        # parse the result

        parse_fct = self.active_subprocesses[sp_ident]["parse_fct"]
        parse_parameterlist = self.active_subprocesses[sp_ident]["parse_parameterlist"]
        ret = int(raw_result["rc"][0])
        output = raw_result["out"]
        outerr = raw_result["err"]

        self.logger.debug( "calling parse_fct %s with %s, %s, %s, %s" \
            % (parse_fct.__name__, ret , output[:10],\
               outerr[:10], parse_parameterlist))
        result = parse_fct(ret, output, outerr , \
            parse_parameterlist, self.logger)
        self.logger.debug("returning : %s" % (result.__repr__()))

        return result

    def execute(self, cmd_list, stdin = "") :
        """
        executes shell command as syncronuos subprocess
        """

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
            raise RuntimeError("cmd: \"%s\" failed with ret=%d and stderr=%s" % \
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

    def execute_detached(self, cmd_list, stdin = "") :
        """
        executes shell command fully detached and returns
        hash to be used by the service to get status info 
        
        """

        sp_ident = str(time.mktime(time.localtime()))
        sp_ident += "-"
        for c in random.sample(range(1000000), 5) :
            sp_ident += chr(c % 26 +ord('a'))
        ret = subprocess.call([afs.CONFIG.binaries["async_executioner"],"%s/%s" % (self.spool_dir, sp_ident)] + cmd_list)
        self.logger.debug("Called Executioner with [%s,%s/%s,%s], ret= %d" % (afs.CONFIG.binaries["async_executioner"], self.spool_dir, sp_ident, cmd_list,  ret))
        
        return sp_ident 

    def __del__(self) :
        """
        cleanup on exit
        """
        shutil.rmtree(self.spool_dir)
        return 

        
def exec_wrapper(func) :
    """
    This decorator is intended for all DAO- and Util-methods .
    The method itself is just compiling the command_list to execute,
    and returns the appropriate parsing function and all info this
    parsing function needs.
    Hooks for Auth checking are in place, but unused.
    Warning: if the interpreter complains 
    got multiple values for keyword argument _cfg, then you're
    passing a positional argument, which should not be there.
    """

    def wrapped(self, *args, **kwargs):
        """actual wrapper code"""

        self.logger.debug("%s: entering with self=%s, args=%s, kwargs=%s" \
            % (func.__name__, self, args, kwargs))

        # kwarg  _user is not passed to DAO
        if not kwargs.has_key("_user") :
            _user = ""
        else :
            _user = kwargs["_user"]
            kwargs.pop("_user")

        # kwarg _timeout is not passed to DAO
        if not kwargs.has_key("_timeout") :
            _timeout = afs.CONFIG.AsyncTimeout
        else :
            _timeout = int(kwargs["_timeout"])
            kwargs.pop("_timeout")
        
        
        if kwargs.has_key("async") :
            async = kwargs["async"]
            kwargs.pop("async")
        else :
            async = False
        

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
        if async == False :
            ret, output, outerr = self.execute(cmd_list)
        else :
            sp_ident = self.execute_detached(cmd_list)
            self.logger.debug("executed detached subprocess with sp_ident %s" % sp_ident)
            self.active_subprocesses[sp_ident] = { "cmd_list": cmd_list, "parse_fct" : parse_fct, "parse_parameterlist" : parse_parameterlist, "start_time" : time.mktime(time.localtime()), "timeout" : _timeout }
            return sp_ident

        # parse the result
        self.logger.debug( "calling parse_fct %s with %s, %s, %s, %s" \
            % (parse_fct.__name__, ret, output[:10],\
               outerr[:10], parse_parameterlist))
        result = parse_fct(ret, output, outerr, \
            parse_parameterlist, self.logger)
        self.logger.debug("%s returning : %s" % (func.__name__, result.__repr__()))
        return result

    return wrapped
