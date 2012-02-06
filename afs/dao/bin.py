#!/usr/bin/python

import string,os,sys
import subprocess,types

VOSBIN="/usr/sbin/vos"
RXDEBUGBIN="/usr/sbin/rxdebug"
UDEBUGBIN="/usr/bin/udebug"
FSBIN="/usr/bin/fs"
OSDBIN="osd"
BOSBIN="/usr/sbin/bos"
TOKENBIN="/usr/bin/tokens"
AKLOGBIN="/usr/bin/aklog"
KINITBIN="/usr/bin/kinit"
KLISTBIN="/usr/bin/klist"
KDESTROYBIN="/usr/lib/mit/bin/kdestroy"

class ExecError( BaseException):
    def __init__(self, message, stack=[]):
        BaseException.__init__(self, message)
        self.message   = message
        self.stack = stack
  
    def __str__(self):
      #FIXME parse build a complete message with stack
      return repr(self.message)


def execute(CmdList, Input="", env={}) :
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
    _output=map(safeStrip,_output.split("\n"))
    _outerr=map(safeStrip,_outerr.split("\n"))

    output=[]
    for line in _output :
        if line == "" : continue
        output.append(line)

    outerr=[]
    for line in _outerr :
        if line == "" : continue
        outerr.append(line)
   
    return pipo.returncode,output,outerr

def safeStrip(Thing) :
    if type(Thing) == types.StringType :
        return Thing.strip()
    return
