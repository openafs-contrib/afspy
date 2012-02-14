#!/usr/bin/env python

import os,subprocess,string,sys

numFailed=0
exit_on_fail=True

for f in os.listdir(".") :
    if f == "testall.py" : continue
    if "Test" in f and f[-3:] == ".py" :
       	print "Executing test %s" % f
        print "================="
        CmdList=[f]
        pipo=subprocess.Popen(CmdList,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        _output,_outerr=pipo.communicate() 
        _output=map(string.strip,_output.split("\n"))
        _outerr=map(string.strip,_outerr.split("\n"))

        result=_outerr[-2:][0]
        print result
        print 
        if "FAILED" in result :
	    if exit_on_fail :
		for line in _outerr :
		    print line
                sys.exit(0)
	    numFailed += 1

print "Total number of Failed units: %s" % numFailed	
