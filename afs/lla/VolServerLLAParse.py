"""
functions for parsing
output from shell commands executed by Volume
"""

import re
import afs.util.misc
from datetime import datetime
from VolServerLLAError import VolServerLLAError
from afs.model import Volume 

def pull_volumes(ret, output, outerr, parse_param_list, logger):
    """
    fills in volume object from AFS-cell.
    if servername and parition are set, return a single object.
    Otherwise, return list of all found volumes
    """
    obj = parse_param_list["args"][0]
    if ret:
        raise VolServerLLAError("Error", outerr)

    logger.debug("getVolume: got=%s" % output)

    line_no = 0
    line = output[line_no]

    if re.search("Could not fetch the entry", line) or line == \
        "VLDB: no such entry"  or re.search(\
        "Unknown volume ID or name", line) \
        or re.search("does not exist in VLDB", line) :
        logger.info("Did not find volume %s in VLDB" % obj.name)
        return None

    # first line gives Name, ID, Type, Used and Status 
    volume_list  = []
    obj_num = -1
    line_num = 0
    while line_num < len(output):
        splits = output[line_num].split()
        #Beginnig block
        if splits[0] == "name":
            logger.debug("Reading line: %s" % output[line_num])
            obj_num += 1
            volume_list.append(Volume.Volume())
            splits = output[line_num].split()
            volume_list[obj_num].name     = splits[1]
            splits = output[line_num+1].split()
            volume_list[obj_num].vid      = int(splits[1])
            splits = output[line_num+2].split()
            volume_list[obj_num].serv     = splits[1]
            if len(splits) > 2:
                volume_list[obj_num].servername     = splits[2]
            splits = output[line_num+3].split()
            volume_list[obj_num].part = \
                afs.util.misc.canonicalize_partition(splits[1])
            splits = output[line_num+4].split()
            volume_list[obj_num].status     = splits[1]
            splits = output[line_num+5].split()
            volume_list[obj_num].backupID = int(splits[1])
            splits = output[line_num+6].split()
            volume_list[obj_num].parentID = int(splits[1])
            splits = output[line_num+7].split()
            volume_list[obj_num].cloneID  = int(splits[1])
            splits = output[line_num+8].split()
            volume_list[obj_num].inUse    = splits[1]
            splits = output[line_num+9].split()
            volume_list[obj_num].needsSalvaged = splits[1]
            splits = output[line_num+10].split()
            volume_list[obj_num].destroyMe     = splits[1]
            splits = output[line_num+11].split()
            volume_list[obj_num].type          = splits[1]
            splits = output[line_num+12].split()
            volume_list[obj_num].creationDate  = \
                datetime.fromtimestamp(float(splits[1]))
            splits = output[line_num+13].split()
            volume_list[obj_num].accessDate = \
                datetime.fromtimestamp(float(splits[1]))
            splits = output[line_num+14].split()
            volume_list[obj_num].updateDate    = \
                datetime.fromtimestamp(float(splits[1]))
            splits = output[line_num+15].split()
            volume_list[obj_num].backupDate    = \
                datetime.fromtimestamp(float(splits[1]))
            splits = output[line_num+16].split()
            volume_list[obj_num].copyDate      = \
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
            volume_list[obj_num].dayUse        = int(splits[1])
            splits = output[line_num+23].split()
            volume_list[obj_num].weekUse       = int(splits[1])
            splits = output[line_num+24].split()
            volume_list[obj_num].spare2        = splits[1]
            splits = output[line_num+25].split()
            volume_list[obj_num].spare3        = splits[1]
            line_num += 25
        else :
            logger.debug("Skipping line: %s" % output[line_num])
            line_num += 1
    if obj.servername != ""  :
        for vol in volume_list :
            if vol.servername == obj.servername and \
                vol.partition == obj.partition :
                return vol

        raise VolServerLLAError("volume %s not on server %s partition %s" % \
                obj.name, obj.servername, obj.partition)
    # return whole list if server/partition unspecified 
    return volume_list

def move(ret, output, outerr, parse_param_list, logger) :
    """
    parses result from method of same name in lo.Volume
    """
    obj = parse_param_list["args"][0]
    if ret:
        raise VolServerLLAError("Error", outerr)
    return obj

def release(ret, output, outerr, parse_param_list, logger):
    """
    parses result from method of same name in lo.Volume
    """
    obj = parse_param_list["args"][0]
    if ret:
        raise VolServerLLAError("Error", outerr)
    return obj

def set_blockquota(ret, output, outerr, parse_param_list, logger):
    """
    parses result from method of same name in lo.Volume
    """
    obj = parse_param_list["args"][0]
    if ret:
        raise VolServerLLAError("Error", outerr)
    return obj

def dump(ret, output, outerr, parse_param_list, logger):
    """
    parses result from method of same name in lo.Volume
    """
    obj = parse_param_list["args"][0]
    if ret:
        raise VolServerLLAError("Error", outerr)
    return obj

def restore(ret, output, outerr, parse_param_list, logger):
    """
    parses result from method of same name in lo.Volume
    """
    obj = parse_param_list["args"][0]
    if ret:
        raise VolServerLLAError("Error", outerr)
    return obj

def convert(ret, output, outerr, parse_param_list, logger):
    """
    parses result from method of same name in lo.Volume
    """
    obj = parse_param_list["args"][0]
    if ret:
        raise VolServerLLAError("Error", outerr)
    return obj

def create(ret, output, outerr, parse_param_list, logger):
    """
    parses result from method of same name in lo.Volume
    """
    obj = parse_param_list["args"][0]
    if ret:
        raise VolServerLLAError("Error", outerr)
    return obj

def remove(ret, output, outerr, parse_param_list, logger):
    """
    parses result from method of same name in lo.Volume
    """
    obj = parse_param_list["args"][0]
    if ret:
        raise VolServerLLAError("Error", outerr)
    return obj

def _get_name_or_id(volume) :
    """
    return name_or_id from volume object.  name takes precedence.
    it is an error if none of name or vid is set
    """
    if (volume.name) :
        name_or_id = volume.name
    elif (volume.vid) :
        name_or_id = "%s" % volume.vid
    else :
        raise VolServerLLAError("Neither name nor vid set in volume object")
    return name_or_id 
