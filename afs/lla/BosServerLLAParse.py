"""
functions for parsing 
output from shell commands executed by lla.BosServer
"""
import re
from BosServerLLAError import BosServerLLAError
from afs.model import BNode

def get_restart_times(ret, output, outerr, parse_param_list, logger):
    """
    parses result from method of same name in lla.BosServer
    """
    obj = parse_param_list["args"][0]
    general_restart_regex = re.compile("Server (\S+) restarts (?:at)?(.*)")
    binary_restart_regex = re.compile(\
        "Server (\S+) restarts for new binaries (?:at)?(.*)")
    if ret :
        raise BosServerLLAError(outerr, output)
    
    if len(output) != 2 :
        raise BosServerLLAError(outerr, output)
    
    obj.general_restart_time = \
        general_restart_regex.match(output[0]).groups()[1].strip()
    obj.newbinary_restart_time = \
        binary_restart_regex.match(output[1]).groups()[1].strip()
    return obj

def set_restart_time(ret, output, outerr, parse_param_list, logger):
    """
    parses result from method of same name in lla.BosServer
    """
    obj = parse_param_list["args"][0]
    if ret :
        raise BosServerLLAError(outerr, output)
    return obj

def get_db_servers(ret, output, outerr, parse_param_list, logger) :
    """
    parses result from method of same name in lla.BosServer
    """
    obj = parse_param_list["args"][0]
    dbserver_regex = re.compile("Host (\d+) is (\S+)")
    if ret :
        raise BosServerLLAError(outerr, output)
    obj.db_servers = []
    for line in output :
        match_obj = dbserver_regex.match(line)
        if match_obj :
            server = {}
            host = match_obj.groups()[1].strip()
            if host[0] == "[" and host[len(host)-1] == "]" :
                server['hostname'] = host[1:-1]
                server['isClone'] = 1
            else :
                server['hostname'] = host
                server['isClone'] = 0
            obj.db_servers.append(server)
    return obj


def get_bnodes(ret, output, outerr, parse_param_list, logger):
    """
    parses result from method of same name in lla.BosServer
    """
    if ret :
        raise BosServerLLAError(outerr, output)
    obj = parse_param_list["args"][0]
    obj.bnodes = []
    idx = 0
    while 1 :
      if idx >= len(output) : break
      tokens = output[idx].split()
      if tokens[0] == "Instance" :
          this_bnode = BNode.BNode(instance_name=tokens[1][:-1], bnode_type=tokens[4][:-1])
          if "currently running normally" in output[idx] : 
              this_bnode.status = "running"
          elif "disabled, currently shutdown" in output[idx] :
              this_bnode.status = "disabled"
          elif ") currently shutting down." in output[idx] :
              this_bnode.status = "shutting down"
          else :
              this_bnode.status = "stopped"
          idx += 1
          if "Auxiliary status is:" in output[idx] :
              idx += 1 
          tokens = output[idx].split()
          this_bnode.start_date = " ".join(tokens[4:8])
          idx += 1 
          tokens = output[idx].split()
          if tokens[0] == "Last" and tokens[1] == "exit" :
              this_bnode.last_exit_date = " ".join(tokens[3:] )
              idx += 1 
              tokens = output[idx].split()
          if tokens[0] == "Last" and tokens[1] == "error" :
              this_bnode.error_exit_date = " ".join(tokens[4:8])
              idx += 1
              tokens = output[idx].split()
          this_bnode.commands = []
          while 1 :
              if tokens[0] == "Instance" : break
              if tokens[0] == "Command" :
                  cmd = " ".join(tokens[3:]).translate(None,"'")
                  this_bnode.commands.append(cmd)
                  idx += 1 
              else : 
                  import sys
                  for ii in range(len(output)) :
                      sys.stderr.write("%d: %s\n" % (ii, output[ii].strip()))
                  raise RuntimeError("parse error at line no %d : %s" % (idx, output[idx]))
              if idx >= len(output) : break
              tokens = output[idx].split()
          obj.bnodes.append(this_bnode)
                       
    return obj 

def salvage(ret, output, outerr, parse_param_list, logger):
    """
    parses result from method of same name in lla.BosServer
    """
    obj = parse_param_list["args"][0]
    if ret :
        raise BosServerLLAError(outerr, output)
    return output

def add_user(ret, output, outerr, parse_param_list, logger):
    """
    parses result from method of same name in lla.BosServer
    """
    if ret :
        raise BosServerLLAError(outerr, output)
    obj = parse_param_list["args"][0]
    obj.superusers = []
    for su in parse_param_list["args"][1] :
         obj.superusers.append(su)    
    return obj

def remove_user(ret, output, outerr, parse_param_list, logger):
    """
    parses result from method of same name in lla.BosServer
    """
    obj = parse_param_list["args"][0]
    if ret :
        raise BosServerLLAError(outerr, output)
    for su in parse_param_list["args"][1] :
         obj.superusers.remove(su)    
    return obj

def get_userlist(ret, output, outerr, parse_param_list, logger):
    """
    parses result from method of same name in lla.BosServer
    """
    if ret :
        raise BosServerLLAError(outerr, output)
    obj = parse_param_list["args"][0]
    obj.superusers = []
    # first line 
    for su in output[0].split()[2:] :
         if len(su) == 0 : continue
         obj.superusers.append(su)
    for line in output[1:] :
        for su in line.split() :
            if len(su) == 0 : continue
            obj.superusers.append(su)
    return obj

def get_filedate(ret, output, outerr, parse_param_list, logger):
    """
    parses result from method of same name in lla.BosServer
    """
    obj = parse_param_list["args"][0]
    if ret :
        raise BosServerLLAError(outerr, output)
    # File /usr/afs/bin/fileserver dated Thu Nov 21 14:16:14 2013, no .BAK file, no .OLD file.
    # or 
    # File /usr/afs/bin/fileserver dated Tue Jul  8 14:12:05 2014, .BAK file dated Fri Oct 10 10:07:38 2014, .OLD file dated Fri Oct 10 10:07:35 2014.
    if "does not exist" in output[0] :
        raise BosServerLLAError(output)
    tokens=output[0].split()
    res_dict = { "current" : " ".join(tokens[4:8])[:-1],
        "backup" : None, "old" : None } 
    if not "no .BAK file" in output[0] :
        res_dict["backup"] = " ".join(tokens[12:16])[:-1]
        if not "no .OLD file" in output[0] :
            res_dict["old"] = " ".join(tokens[20:24])[:-1]
    else :
        if not "no .OLD file" in output[0] :
            res_dict["old"] = " ".join(tokens[15:19])[:-1]
    return res_dict

def restart(ret, output, outerr, parse_param_list, logger):
    """
    parses result from method of same name in lla.BosServer
    """
    if ret :
        raise BosServerLLAError(outerr, output)
    return True

def start_bnodes(ret, output, outerr, parse_param_list, logger):
    """
    parses result from method of same name in lla.BosServer
    """
    if ret :
        raise BosServerLLAError(outerr, output)
    return True

def stop_bnodes(ret, output, outerr, parse_param_list, logger):
    """
    parses result from method of same name in lla.BosServer
    """
    obj = parse_param_list["args"][0]
    if ret :
        raise RuntimeError("%s, %s" % (output, outerr) ) 
    return True

def execute_shell(ret, output, outerr, parse_param_list, logger):
    """
    parses result from method of same name in lla.BosServer
    """
    if ret :
        raise BosServerLLAError(outerr, output)
    return True

def get_log(ret, output, outerr, parse_param_list, logger):
    """
    parses result from method of same name in lla.BosServer
    """
    if ret :
        raise BosServerLLAError(outerr, output)
    ## we just get the LogFile as array of lines
    return output[1:]

def prune_log(ret, output, outerr, parse_param_list, logger):
    """
    parses result from method of same name in lla.BosServer
    """
    if ret :
        raise BosServerLLAError(outerr, output)
    return True

def shutdown(ret, output, outerr, parse_param_list, logger):
    """
    parses result from method of same name in lla.BosServer
    """
    if ret :
        raise BosServerLLAError(outerr, output)
    return True

def startup(ret, output, outerr, parse_param_list, logger):
    """
    parses result from method of same name in lla.BosServer
    """
    if ret :
        raise BosServerLLAError(outerr, output)
    return True

#
# convenience helper
#

def restarttime_to_minutes(time):
    """
    converts a restart time from the human readable output to
    minutes after midnight.
    -1 means never
    """
    if time == "never" : 
        return -1
    minutes = 0
    tokens = time.split()
    if tokens[1] == "pm" :
        minutes = 12*60
    hours, min = tokens[0].split(":")
    minutes += int(hours)*60 + min
    return minutes

def minutes_to_restarttime(minutes) :
    """
    converts an int meaning Minutes after midnight into a 
    restartTime string  understood by the bos command
    """
    if minutes == -1 :
        return "never"
    pod = "am"
    if minutes > 12*60 :
        pod = "pm"
        minutes -= 12*60
    time = "%d:%02d %s" % (minutes / 60, minutes % 60, pod)
    return time

