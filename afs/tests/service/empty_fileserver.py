#!/usr/bin/env python


import afs

from afs.util.AFSConfig import parse_configs
from afs.service.FSService import FSService
from afs.service.VolumeService import VolumeService

import time



my_parser = argparse.ArgumentParser(parents = [afs.ARGPARSER], \
    add_help = False,epilog = afs.ARGPARSER.epilog)
my_parser.add_argument("--src_srv", required=True,\ 
    help="source-server")
my_parser.add_argument("--dst_srv", required=True,\ 
    help="destination-server")

#put all cmd-line options into afs.CONFIG
parse_configs(my_parser)


FSS = FSService()
VolS = VolumeService()

# get fileserver objects
src_fs = FSS.get_fileserver(afs.CONFIG.src_srv)
dst_fs = FSS.get_fileserver(afs.CONFIG.dst_srv)


# get list of all volumes on this fileserver
volume_list = FSS.get_volume_list(src_fs)

# move loop
move_count = 0
while move_count < len(volume_list) :
    if (VolS.active_tasks) >= 4 :
        time.sleep(10)

    VolS.move(volume_list[move_count], src_srv, dst_srv)

    # check finished moves
    for task in VolS.finished_tasks :
        # do something


# wait for last 4 moves to finish...
    
    
