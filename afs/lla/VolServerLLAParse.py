"""
functions for parsing
output from shell commands executed by Volume
"""

import re
import afs.util.misc
from datetime import datetime
from VolServerLLAError import VolServerLLAError
from afs.model import Volume 
import afs

def examine(ret, output, outerr, parse_param_list, logger):
    """
    parse  vos examine to fills in volume object from AFS-cell.
    """
    obj = parse_param_list["args"][0]
    if ret:
        raise VolServerLLAError("ret=%s, output=%s, outerr=%s" % (ret, output, outerr))

    _cfg = parse_param_list["kwargs"]["_cfg"] 
    logger.debug("examine: got=%s" % output)

    line_no = 0
    line = output[line_no]

    if re.search("Could not fetch the entry", line) or line == \
        "VLDB: no such entry"  or re.search(\
        "Unknown volume ID or name", line) \
        or re.search("does not exist in VLDB", line) :
        logger.info("Did not find volume %s in VLDB" % obj.name)
        return None

    volume_list  = []
    obj_num = -1
    line_num = 0
    while line_num < len(output):
        splits = output[line_num].split()
        # Beginning block
        if splits[0] == "name":
            logger.debug("Reading line: %s" % output[line_num])
            obj_num += 1
            volume_list.append(Volume.Volume())
            splits = output[line_num].split()
            volume_list[obj_num].name     = splits[1]
            splits = output[line_num+1].split()
            volume_list[obj_num].vid      = int(splits[1])
            splits = output[line_num+2].split()
            volume_list[obj_num].servername     = splits[1]
            if len(splits) > 2:
                volume_list[obj_num].servername     = splits[2]
            splits = output[line_num+3].split()
            volume_list[obj_num].partition = \
                afs.util.misc.canonicalize_partition(splits[1])
            splits = output[line_num+4].split()
            volume_list[obj_num].status     = splits[1]
            splits = output[line_num+5].split()
            volume_list[obj_num].backup_id = int(splits[1])
            splits = output[line_num+6].split()
            volume_list[obj_num].parent_id = int(splits[1])
            splits = output[line_num+7].split()
            volume_list[obj_num].clone_id  = int(splits[1])
            splits = output[line_num+8].split()
            volume_list[obj_num].in_use    = splits[1]
            splits = output[line_num+9].split()
            volume_list[obj_num].needs_salvage = splits[1]
            splits = output[line_num+10].split()
            volume_list[obj_num].destroy_me     = splits[1]
            splits = output[line_num+11].split()
            volume_list[obj_num].type          = splits[1]
            splits = output[line_num+12].split()
            volume_list[obj_num].creation_date  = \
                datetime.fromtimestamp(float(splits[1]))
            splits = output[line_num+13].split()
            volume_list[obj_num].access_date = \
                datetime.fromtimestamp(float(splits[1]))
            splits = output[line_num+14].split()
            volume_list[obj_num].copy_date    = \
                datetime.fromtimestamp(float(splits[1]))
            splits = output[line_num+15].split()
            volume_list[obj_num].backup_date    = \
                datetime.fromtimestamp(float(splits[1]))
            splits = output[line_num+16].split()
            volume_list[obj_num].copy_date      = \
                datetime.fromtimestamp(float(splits[1]))
            splits = output[line_num+17].split()
            volume_list[obj_num].flags         = splits[1]
            splits = output[line_num+18].split()
            volume_list[obj_num].diskused      = int(splits[1])
            splits = output[line_num+19].split()
            volume_list[obj_num].maxquota      = int(splits[1])
            splits = output[line_num+20].split()
            volume_list[obj_num].minquota      = int(splits[1])
            splits = output[line_num+21].split()
            volume_list[obj_num].filecount     = int(splits[1])
            splits = output[line_num+22].split()
            volume_list[obj_num].day_use        = int(splits[1])
            splits = output[line_num+23].split()
            volume_list[obj_num].week_use       = int(splits[1])
            splits = output[line_num+24].split()
            volume_list[obj_num].spare2        = splits[1]
            splits = output[line_num+25].split()
            volume_list[obj_num].spare3        = splits[1]
            splits = output[line_num+27].split()
            if len(splits) >= 4 :
                volume_list[obj_num].readonly_id = splits[3]
            else :
                volume_list[obj_num].readonly_id = 0
            line_num += 27
        else :
            logger.debug("Skipping line: %s" % output[line_num])
            line_num += 1
    if obj.servername != None  :
        for vol in volume_list :
            DNSInfo = afs.LOOKUP_UTIL[_cfg.cell].get_dns_info(vol.servername)
            # strictly, we should only check in "names". But DNS is a mess anyway.
            if obj.servername in DNSInfo["names"] or obj.servername in DNSInfo["ipaddrs"] :
                return vol
        raise VolServerLLAError("volume %s not on server %s partition %s" % \
            (obj.vid, obj.servername, obj.partition))
    # return whole list if server/partition unspecified
    return volume_list

def move(ret, output, outerr, parse_param_list, logger) :
    """
    parses result from method of same name in lo.Volume
    """
    obj = parse_param_list["args"][0]
    if ret:
        raise VolServerLLAError("ret=%s, output=%s, outerr=%s" % (ret, output, outerr))
    return obj

def release(ret, output, outerr, parse_param_list, logger):
    """
    parses result from method of same name in lo.Volume
    """
    obj = parse_param_list["args"][0]
    if ret:
        raise VolServerLLAError("ret=%s, output=%s, outerr=%s" % (ret, output, outerr))
    return True

def set_blockquota(ret, output, outerr, parse_param_list, logger):
    """
    parses result from method of same name in lo.Volume
    """
    obj = parse_param_list["args"][0]
    if ret:
        raise VolServerLLAError("ret=%s, output=%s, outerr=%s" % (ret, output, outerr))
    return obj

def dump(ret, output, outerr, parse_param_list, logger):
    """
    parses result from method of same name in lo.Volume
    """
    obj = parse_param_list["args"][0]
    if ret:
        raise VolServerLLAError("ret=%s, output=%s, outerr=%s" % (ret, output, outerr))
    return True

def restore(ret, output, outerr, parse_param_list, logger):
    """
    parses result from method of same name in lo.Volume
    """
    obj = parse_param_list["args"][0]
    if ret:
        raise VolServerLLAError("ret=%s, output=%s, outerr=%s" % (ret, output, outerr))
    return obj

def convert(ret, output, outerr, parse_param_list, logger):
    """
    parses result from method of same name in lo.Volume
    """
    obj = parse_param_list["args"][0]
    if ret:
        raise VolServerLLAError("ret=%s, output=%s, outerr=%s" % (ret, output, outerr))
    return obj

def create(ret, output, outerr, parse_param_list, logger):
    """
    parses result from method of same name in lo.Volume
    """
    obj = parse_param_list["args"][0]
    if ret:
        raise VolServerLLAError("ret=%s, output=%s, outerr=%s" % (ret, output, outerr))
    return True

def remove(ret, output, outerr, parse_param_list, logger):
    """
    parses result from method of same name in lo.Volume
    """
    obj = parse_param_list["args"][0]
    if ret:
        raise VolServerLLAError("ret=%s, output=%s, outerr=%s" % (ret, output, outerr))
    return True

