"""
Low-level implementation for methods
dealing with a bosserver.
uses BosServer and Bnode objects
"""
import types
import afs
from afs.lla.BaseLLA import BaseLLA, exec_wrapper
import BosServerLLAParse as PM
from afs.model import BosServer
from BosServerLLAError import BosServerLLAError


class BosServerLLA(BaseLLA) :
    """
    Direct Access Object for a Process (BNode)
    """

    def __init__(self) :
        BaseLLA.__init__(self)
        return

    def get_bos_server(self, bos_server_name, _cfg = None) :
        """
        get a full bos_server object from server.
        filled attributes depends on authorization. 
        """
        dns_info = afs.LOOKUP_UTIL[_cfg.cell].get_dns_info(bos_server_name)
        bos_server = BosServer.BosServer()
        bos_server.servernames = dns_info["names"]
        bos_server.ipaddrs = dns_info["ipaddrs"]
        bos_server = self.get_bnodes(bos_server)
        bos_server = self.get_restart_times(bos_server)
        bos_server = self.get_db_servers(bos_server)
        bos_server = self.get_superuserlist(bos_server)
        return bos_server

    @exec_wrapper    
    def get_bnodes(self, bos_server_name, _cfg = None) :
        """
        get list of BNode Objects from a server.
        """ 
        command_list = [_cfg.binaries["bos"], "status", "-server", \
            "%s"  % bos_server_name,"-long", "-cell" , "%s" % _cfg.cell]
        return command_list, PM.get_bnodes

    #
    # methods to deal with specific attributes of a bos_server object
    #

    @exec_wrapper    
    def get_restart_times(self, bos_server_name, _cfg = None):
        """
        get attributes restart times from bosserver into given object
        """
        command_list = [_cfg.binaries["bos"], "getrestart", "-server", \
            "%s"  % bos_server_name, "-cell" , "%s" % _cfg.cell]
        return command_list, PM.get_restart_times

    @exec_wrapper    
    def set_restart_time(self, bos_server_name, restart_type, time_string, _cfg = None) :
        """
        sets general restart time onto bosserver as given in the object.
        restarttype must be of ["general", "newbinary"]
        """
        if restart_type == "newbinary" :
            restart_type == "binary" 
        command_list = [_cfg.binaries["bos"], "setrestart", "-server", "%s"  % \
            bos_server_name, "-time",  "%s" % \
            time_string,  "-%s" % restart_type, "-cell" , "%s" % _cfg.cell ]
        return command_list, PM.set_restart_time

    @exec_wrapper    
    def add_superuser(self, bos_server_name, userlist, _cfg = None) :
        """
        adds userlist to bosserver*s superuserlist
        """
        if type(userlist) != types.ListType :
              raise BosServerLLAError("userlist must be a list of strings")
        if len(userlist) == 0 :
            raise BosServerLLAError("userlist empty.")
        usernames = " ".join(userlist)
        command_list = [_cfg.binaries["bos"], "adduser", "-server", "%s"  % \
            bos_server_name,  "-user",  "%s" % usernames, "-cell" , "%s" % _cfg.cell ]
        return command_list, PM.add_superuser
    
    @exec_wrapper    
    def remove_superuser(self, bos_server_name, userlist, _cfg = None) :
        """
        removes userlist to bosserver*s superuserlist
        """
        if type(userlist) != types.ListType :
            raise BosServerLLAError("userlist must be a list of strings")
        if len(userlist) == 0 :
            raise BosServerLLAError("userlist empty.")
        usernames = " ".join(userlist)
        command_list = [_cfg.binaries["bos"], "removeuser", "-server", \
           "%s"  % bos_server_name, "-user",  "%s" % usernames, "-cell" , "%s" % _cfg.cell ]
        return command_list, PM.remove_superuser
    
    @exec_wrapper    
    def get_superuserlist(self, bos_server_name, _cfg = None) :
        """
        get bosserver's superuserlist into given object
        """
        command_list = [_cfg.binaries["bos"], "listuser", "-server", \
            "%s"  % bos_server_name]
        return command_list, PM.get_superuserlist
    
    @exec_wrapper    
    def get_filedate(self, bos_server_name, filelist, destdir="", _cfg = None) :
        """
        return mdate of file(s) on the bosserver
        """
        filenames = " ".join(filelist)
        command_list = [_cfg.binaries["bos"], "getdate", "-server", \
            "%s"  % bos_server_name, "-file", "%s" % filenames, "-cell" , "%s" % _cfg.cell ]
        if destdir != "" :
            command_list += ["-dir", "%s" % destdir]
        return command_list, PM.get_filedate
    
    @exec_wrapper    
    def get_db_servers(self, bos_server_name, _cfg = None) :
        """
        get list of all database-servers known to a given AFS-server
        """
        command_list = [_cfg.binaries["bos"], "listhosts", "-server", \
            "%s"  % bos_server_name, "-cell" , "%s" % _cfg.cell]
        return command_list, PM.get_db_servers

    @exec_wrapper    
    def restart(self, bos_server_name, bnodes, restart_bosserver = False, \
                _cfg = None) :
        """
        restart one or all bnodes on server
        optionally, restart bosserver itself as well
        bnodes can be "-all" or list of bnodes to restart
        """
        command_list = [_cfg.binaries["bos"], "restart", "-server", \
            "%s"  % bos_server_name, "-cell" , "%s" % _cfg.cell ]
        if bnodes == "-all" :
            command_list += ["-all"]
        else :
            command_list += ["-instance %s" % " ".join(bnodes) ]
        if restart_bosserver :
            command_list += ["-bosserver"]
        return command_list, PM.restart
    
    @exec_wrapper    
    def start_bnodes(self, bos_server_name, bnodes, _cfg = None) :
        """
        start previuosly stopped bnode(s) 
        bnodes mut be list of bnode instancenames
        """ 
        command_list = [_cfg.binaries["bos"], "start", "-server", \
            "%s"  % bos_server_name, "-cell" , "%s" % _cfg.cell, "-instance" ]
        command_list += bnodes
        return command_list, PM.start_bnodes

    @exec_wrapper    
    def stop_bnodes(self, bos_server_name, bnodes, _cfg = None) :
        """
        stop running bnode(s) 
        bnodes mut be list of bnode instancenames
        """
        command_list = [_cfg.binaries["bos"], "stop", "-server", \
            "%s"  % bos_server_name, "-cell" , "%s" % _cfg.cell, "-instance" ]
        command_list += bnodes
        return command_list, PM.stop_bnodes

    @exec_wrapper    
    def execute_shell(self, bos_server_name, command, _cfg = None) :
        """
        execute shell command on server
        """
        command_list = [_cfg.binaries["bos"], "exec", "-server", \
            "%s"  % bos_server_name, "-cmd", "%s" % command, "-cell" , "%s" % _cfg.cell ]
        return command_list, PM.execute_shell
    
    @exec_wrapper    
    def get_log(self, bos_server_name, logfile, _cfg = None) :
        """
        retrieve logfile from server
        """
        command_list = [_cfg.binaries["bos"], "getlog", "-server", \
            "%s"  % bos_server_name, "-file", "%s" % logfile, "-cell" , "%s" % _cfg.cell ]
        return command_list, PM.get_log
    
    @exec_wrapper    
    def prune_log(self, bos_server_name, filetypes, _cfg = None) :
        """
        prune (remove) files on server 
        filetype must be one of "bak", "old", "core", "all"
        """ 
        command_list = [_cfg.binaries["bos"], "prune", "-server", \
            "%s"  % bos_server_name, "-cell" , "%s" % _cfg.cell, ]
        for _type in ["bak", "old", "core", "all" ] :
            if _type in filetypes :
                command_list += ["-" + _type]
        return command_list, PM.prune_log

    @exec_wrapper    
    def startup(self, bos_server_name, _cfg = None) :
        """
        start all bnodes on a server
        """
        command_list = [_cfg.binaries["bos"], "startup", "-server", \
            "%s"  % bos_server_name, "-cell" , "%s" % _cfg.cell ]
        return command_list, PM.startup
    
    @exec_wrapper    
    def shutdown(self, bos_server_name, _cfg = None) :
        """
        stop all bnodes on a server
        """
        command_list = [_cfg.binaries["bos"], "shutdown", "-server", \
            "%s"  % bos_server_name, "-cell" , "%s" % _cfg.cell ]
        return command_list, PM.shutdown
    
    @exec_wrapper    
    def salvage(self, bos_server_name, partition=None, volume=None, _cfg = None) :
        """
        salvage volume(s) on a server
        both partition and volume=None: all server
        volume=None: one partition on server
        """ 
        command_list = [_cfg.binaries["bos"], "salvage", "-server", \
            "%s"  % bos_server_name, "-forceDAFS", "-cell" , "%s" % _cfg.cell ]

        if volume != None :
            command_list += [  "-volume", "%s" % volume ] 
        if partition != None :
            command_list += [ "-partition", "%s" % partition ]

        if volume == None and partition == None :
            command_list += [ "-all" ]
        return command_list, PM.salvage
