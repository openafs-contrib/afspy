"""
Provides Methods to query and modify live AFS-Volumes
Makes use of the model object Volume.
"""

import os

from afs.lla.BaseLLA import BaseLLA, exec_wrapper
import VolServerLLAParse as PM
from VolServerLLAError import VolServerLLAError
from afs.model import Volume 

class VolServerLLA(BaseLLA) :
    """
    Provides Methods to query and modify live AFS-Volumes
    Makes use of the model object Volume.
    """
    
    def __init__(self) :
        BaseLLA.__init__(self)
        return

    def get_name_or_id(self, param) :
        try: 
            if param.vid != None :
                name_or_id = "%s" % param.vid
            elif param.name != None :
                name_or_id = param.name
            else :
                raise RuntimeError("Volume name or id required.")
        except AttributeError :
            name_or_id = param   
        return name_or_id

    @exec_wrapper
    def move(self, volume, dst_server, dst_partition, _cfg = None ) :
        """
        moves a volume to a new Destination. 
        """
        name_or_id = self.get_name_or_id(volume)
        command_list = [_cfg.binaries["vos"], "move", "%s" % name_or_id, \
            "-fromserver", volume.servername, "-frompartition" , \
            volume.partition, "-toserver" , "%s" % dst_server, "-topartition", \
            "%s" % dst_partition,  "-cell", _cfg.cell ]
        volume.servername = dst_server
        volume.partition = dst_partition
        return command_list, PM.move

    @exec_wrapper
    def release(self, volume, _cfg=None) :
        """
        release this volume. 
        Also accepts volume_name. 
        This is just implemented as a reminder
        """
        name_or_id = self.get_name_or_id(volume)

        command_list = [_cfg.binaries["vos"], "release","%s" % name_or_id, \
            "-cell", _cfg.cell]
        return command_list, PM.release
    
    @exec_wrapper
    def set_blockquota(self, volume, blockquota, _cfg = None) :
        """
        sets Blockquota
        """
        command_list = [_cfg.binaries["vos"], "setfield", "-id" , \
            "%s" % volume.vid, "-maxquota", "%s" % blockquota, \
            "-cell", _cfg.cell]
        volume.maxquota = blockquota
        return command_list, PM.set_blockquota
        
    @exec_wrapper
    def dump(self, volume, dump_file, force=False, _cfg = None) :
        """
        Dumps a volume into a file
        """
        name_or_id = self.get_name_or_id(volume)
        if os.path.exists(dump_file) and not force :
            raise RuntimeError("Dumpfile %s exists. Not overwriting." % dump_file)
        command_list = [_cfg.binaries["vos"], "dump", "-id" , \
            name_or_id, "-file", dump_file, "-cell", _cfg.cell]
        return command_list, PM.dump

    @exec_wrapper
    def restore(self, volume, dump_file, flags=[], _cfg = None) :
        """
        Restores this (abstract) volume from a file.
        by default, abors if the volume already exists.
        """
        if not "-overwrite" in flags :
            flags += [  "-overwrite", "abort"  ]
        command_list = [_cfg.binaries["vos"], "restore", "-server", \
            volume.servername, "-partition", volume.partition, "-name", \
            volume.name, "-file", dump_file, "-cell", _cfg.cell] + flags
        return command_list, PM.restore
    
    @exec_wrapper
    def convert(self, volume, _cfg = None) :
        """
        converts this RO-Volume to a RW
        """
        name_or_id = self.get_name_or_id(volume)
        command_list = [_cfg.binaries["vos"], "convertROtoRW", "-server", \
            volume.servername, "-partition", volume.partition, "-id", \
            name_or_id, "-cell", _cfg.cell]
        return command_list, PM.convert

    @exec_wrapper
    def create(self, volume, maxquota=5000, _cfg = None) :
        """
        create a Volume
        """
        command_list = [_cfg.binaries["vos"], "create", "-server", \
            volume.servername, "-partition", volume.partition, "-name", \
            volume.name , "-maxquota", "%s" % maxquota, "-cell", _cfg.cell]
        return command_list, PM.create
    
    @exec_wrapper
    def remove(self, volume, _cfg = None) :
        """
        remove this Volume from the Server
        """
        name_or_id = self.get_name_or_id(volume)
        command_list = [_cfg.binaries["vos"], "remove", "-server", \
            volume.servername, "-partition", volume.partition, "-id", \
            name_or_id, "-cell", _cfg.cell ]
        return command_list, PM.remove
   
    @exec_wrapper
    def examine(self, volume, _cfg = None) :
        """
        returns volume object filled by vos examine from vol-server. 
        """
        name_or_id = self.get_name_or_id(volume)
        command_list = [_cfg.binaries["vos"], "examine", "%s"  % name_or_id, \
            "-format", "-cell", _cfg.cell]
        return command_list, PM.examine

