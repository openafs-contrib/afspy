#!/usr/bin/env python
#
# Copyright 2010 Manfred Furuholmen
#
#

from afs.service.VolService import VolService
from afs.model.Token import Token



if __name__ == "__main__" :
    token = Token('foo','foo','ipp-garching.mpg.de')
    volMng = VolService(token)
    vol = volMng.getVolByName('536985802')
    
    
    
    print "Volume ---"
    print vol
    print "------"
    print "All volume from cell"
    vols = volMng.loadVol()
    for vol in vols:
        print vol
    
   
     
