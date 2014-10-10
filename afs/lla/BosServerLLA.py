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

    #
    # public interface to deal with a full bos_server object
    #

    def push_bos_server(self, bos_server, _cfg=None) :
        """
        pushes configuration of bos_server to AFS-cell
        do not change bnodes
        """
        result_list = []
        # restart times
        result_list.append(self.push_general_restart_time(bos_server, \
            ))
        result_list.append(self.push_newbinary_restart_time(bos_server, \
            ))
        # userlist
        superusers=self.get_userlist(bos_server).superusers
        to_be_removed = []
        to_be_added = []
        for su in superusers :
            if not su in bos_server.superusers :
                to_be_removed.append(su)
        if len(to_be_removed) > 0 :
            self.remove_user(bos_server,to_be_removed)
        for su in bos_server.superusers :
            if not su in superusers :
                to_be_added.append(su)
        if len(to_be_added) > 0 :
            self.add_user(bos_server,to_be_added)
            
        return  

    def get_bos_server(self, bos_server, _cfg = None) :
        """
        get a full bos_server object from server.
        filled attributes depends on authorization. 
        """
        dns_info = afs.LOOKUP_UTIL[_cfg.cell].get_dns_info(bos_server.servernames[0])
        bos_server.servernames = dns_info["names"]
        bos_server.ipaddrs = dns_info["ipaddrs"]
        bos_server = self.get_bnodes(bos_server)
        bos_server = self.get_restart_times(bos_server)
        bos_server = self.get_db_servers(bos_server)
        return bos_server

    def push_restart_times(self, bos_server, _cfg = None) :
        """
        pushes general restart time onto bosserver as given in the object.
        """
        obj=self.push_general_restart_time(bos_server)
        obj.newbinary_restart_time = bos_server.newbinary_restart_time
        obj=self.push_newbinary_restart_time(obj)
        return obj

    @exec_wrapper    
    def get_bnodes(self, bos_server, _cfg = None) :
        """
        get list of BNode Objects from a server.
        """ 
        command_list = [_cfg.binaries["bos"], "status", "-server", \
            "%s"  % bos_server.servernames[0] ,"-long", "-cell" , "%s" % _cfg.cell]
        return command_list, PM.get_bnodes

    #
    # methods to deal with specific attributes of a bos_server object
    #

    @exec_wrapper    
    def get_restart_times(self, bos_server, _cfg = None):
        """
        get attributes restart times from bosserver into given object
        """
        command_list = [_cfg.binaries["bos"], "getrestart", "-server", \
            "%s"  % bos_server.servernames[0], "-cell" , "%s" % _cfg.cell]
        return command_list, PM.get_restart_times

    @exec_wrapper    
    def push_general_restart_time(self, bos_server, _cfg = None) :
        """
        pushes general restart time onto bosserver as given in the object.
        """
        command_list = [_cfg.binaries["bos"], "setrestart", "-server", "%s"  % \
            bos_server.servernames[0], "-time",  "%s" % \
            bos_server.general_restart_time,  "-general", "-cell" , "%s" % _cfg.cell ]
        return command_list, PM.push_restart_time

    @exec_wrapper    
    def push_newbinary_restart_time(self, bos_server, _cfg = None) :
        """
        pushes restart time for new binaries on bosserver as given in the object.
        """
        command_list = [_cfg.binaries["bos"], "setrestart", "-server", "%s"  % \
            bos_server.servernames[0], "-time",  "%s" % \
            bos_server.general_restart_time,  "-newbinary", "-cell" , "%s" % _cfg.cell ]
        return command_list, PM.push_restart_time

    @exec_wrapper    
    def add_user(self, bos_server, userlist, _cfg = None) :
        """
        adds userlist to bosserver*s superuserlist
        should only be called by push_bos_server
        """
        if type(userlist) != types.ListType :
              raise BosServerLLAError("userlist must be a list of strings")
        usernames = " ".join(userlist)
        command_list = [_cfg.binaries["bos"], "adduser", "-server", "%s"  % \
            bos_server.servernames[0],  "-user",  "%s" % usernames, "-cell" , "%s" % _cfg.cell ]
        return command_list, PM.add_user
    
    @exec_wrapper    
    def remove_user(self, bos_server, userlist, _cfg = None) :
        """
        removes userlist to bosserver*s superuserlist
        should only be called by push_bos_server
        """
        if type(userlist) != types.ListType :
              raise BosServerLLAError("userlist must be a list of strings")
        usernames = " ".join(userlist)
        command_list = [_cfg.binaries["bos"], "removeuser", "-server", \
           "%s"  % bos_server.servernames[0], "-user",  "%s" % usernames, "-cell" , "%s" % _cfg.cell ]
        return command_list, PM.remove_user
    
    @exec_wrapper    
    def get_userlist(self, bos_server, _cfg = None) :
        """
        get bosserver's superuserlist into given object
        """
        command_list = [_cfg.binaries["bos"], "listuser", "-server", \
            "%s"  % bos_server.servernames[0] ]
        return command_list, PM.get_userlist
    
    @exec_wrapper    
    def get_filedate(self, bos_server, filelist, destdir="", _cfg = None) :
        """
        return mdate of file(s) on the bosserver
        """
        filenames = " ".join(filelist)
        command_list = [_cfg.binaries["bos"], "getdate", "-server", \
            "%s"  % bos_server.servernames[0], "-file", "%s" % filenames, "-cell" , "%s" % _cfg.cell ]
        if destdir != "" :
            command_list += ["-dir", "%s" % destdir]
        return command_list, PM.get_filedate
    
    @exec_wrapper    
    def get_db_servers(self, bos_server, _cfg = None) :
        """
        get list of all database-servers known to a given AFS-server
        """
        command_list = [_cfg.binaries["bos"], "listhosts", "-server", \
            "%s"  % bos_server.servernames[0], "-cell" , "%s" % _cfg.cell]
        return command_list, PM.get_db_servers

    @exec_wrapper    
    def restart(self, bos_server, bnodes = None, restart_bosserver = False, \
                _cfg = None) :
        """
        restart one or all bnodes on server
        optionally, restart bosserver itself as well
        """
        command_list = [_cfg.binaries["bos"], "restart", "-server", \
            "%s"  % bos_server.servernames[0], "-cell" , "%s" % _cfg.cell ]
        if bnodes == None :
            command_list += ["-all"]
        else :
            all_bnodes = ""
            for _bnode in bnodes :
                all_bnodes += _bnode.name + " "  
            command_list += ["-instance %s" % all_bnodes ]
        if restart_bosserver :
            command_list += ["-bosserver"]
        return command_list, PM.restart
    
    @exec_wrapper    
    def start_bnodes(self, bos_server, bnodes, _cfg = None) :
        """
        start previuosly stopped bnode(s) 
        """ 
        command_list = [_cfg.binaries["bos"], "start", "-server", \
            "%s"  % bos_server.servernames[0], "-cell" , "%s" % _cfg.cell, "-instance" ]
        for _bnode in bnodes :
            command_list.append(_bnode.instance_name)
        return command_list, PM.start_bnodes

    @exec_wrapper    
    def stop_bnodes(self, bos_server, bnodes, _cfg = None) :
        """
        stop running bnode(s) 
        """
        command_list = [_cfg.binaries["bos"], "stop", "-server", \
            "%s"  % bos_server.servernames[0], "-cell" , "%s" % _cfg.cell, "-instance" ]
        for _bnode in bnodes :
            command_list.append(_bnode.instance_name)
        return command_list, PM.stop_bnodes

    @exec_wrapper    
    def execute_shell(self, bos_server, command, _cfg = None) :
        """
        execute shell command on server
        """
        command_list = [_cfg.binaries["bos"], "exec", "-server", \
            "%s"  % bos_server.servernames[0], "-cmd", "%s" % command, "-cell" , "%s" % _cfg.cell ]
        return command_list, PM.execute_shell
    
    @exec_wrapper    
    def get_log(self, bos_server, logfile, _cfg = None) :
        """
        retrieve logfile from server
        """
        command_list = [_cfg.binaries["bos"], "getlog", "-server", \
            "%s"  % bos_server.servernames[0], "-file", "%s" % logfile, "-cell" , "%s" % _cfg.cell ]
        return command_list, PM.get_log
    
    @exec_wrapper    
    def prune_log(self, bos_server, filetypes, _cfg = None) :
        """
        prune (remove) files on server 
        filetype must be one of "bak", "old", "core", "all"
        """ 
        command_list = [_cfg.binaries["bos"], "prune", "-server", \
            "%s"  % bos_server.servernames[0], "-cell" , "%s" % _cfg.cell, ]
        for _type in ["bak", "old", "core", "all" ] :
            if _type in filetypes :
                command_list += ["-" + _type]
        return command_list, PM.prune_log

    @exec_wrapper    
    def startup(self, bos_server, _cfg = None) :
        """
        start all bnodes on a server
        """
        command_list = [_cfg.binaries["bos"], "startup", "-server", \
            "%s"  % bos_server.servernames[0], "-cell" , "%s" % _cfg.cell ]
        return command_list, PM.startup
    
    @exec_wrapper    
    def shutdown(self, bos_server, _cfg = None) :
        """
        stop all bnodes on a server
        """
        command_list = [_cfg.binaries["bos"], "shutdown", "-server", \
            "%s"  % bos_server.servernames[0], "-cell" , "%s" % _cfg.cell ]
        return command_list, PM.shutdown
    
    @exec_wrapper    
    def salvage_volume(self, bos_server, volume, _cfg = None) :
        """
        salvage a volume on a server
        no extra options implemented yet.
        """ 
        command_list = [_cfg.binaries["bos"], "salvage", "-server", \
            "%s"  % bos_server.servernames[0], "-partition", "%s" % \
            volume.partition, "-volume", "%s" % volume.name, "-cell" , "%s" % _cfg.cell ]
        return command_list, PM.salvage_volume
