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

    @exec_wrapper
    def move(self, volume, dst_server, dst_partition, _cfg = None ) :
        """
        moves a volume to a new Destination. 
        """
        command_list = [_cfg.binaries["vos"], "move", "%s" % volume.vid, \
            "-fromserver", volume.servername, "-frompartition" , \
            volume.partition, "-toserver" , "%s" % dst_server, "-topartition", \
            "%s" % dst_partition,  "-cell", _cfg.cell ]
        return command_list, PM.move

    @exec_wrapper
    def release(self, volume, _cfg=None) :
        """
        release this volume
        """
        command_list = [_cfg.binaries["vos"], "release","%s" % volume.vid, \
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
        return command_list, PM.set_blockquota
        
    @exec_wrapper
    def dump(self, volume, dump_file, force=False, _cfg = None) :
        """
        Dumps a volume into a file
        """
        name_or_id = PM._get_name_or_id(volume)
        if os.path.exists(dump_file) and not force :
            raise RuntimeError("Dumpfile %s exists. Not overwriting." % dump_file)
        command_list = [_cfg.binaries["vos"], "dump", "-id" , \
            name_or_id, "-file", dump_file, "-cell", _cfg.cell]
        return command_list, PM.dump

    @exec_wrapper
    def restore(self, volume, dump_file, _cfg = None) :
        """
        Restores this (abstract) volume from a file.
        aborts if the volume already exists.
        """
        command_list = [_cfg.binaries["vos"], "restore", "-server", \
            volume.servername, "-partition", volume.partition, "-name", \
            volume.name, "-file", dump_file, "-overwrite", "abort", "-cell", _cfg.cell]
        return command_list, PM.restore
    
    @exec_wrapper
    def convert(self, volume, _cfg = None) :
        """
        converts this RO-Volume to a RW
        """
        name_or_id = PM._get_name_or_id(volume)
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
        name_or_id = PM._get_name_or_id(volume)
        command_list = [_cfg.binaries["vos"], "remove", "-server", \
            volume.servername, "-partition", volume.partition, "-id", \
            name_or_id, "-cell", _cfg.cell ]
        return command_list, PM.remove
   
    @exec_wrapper
    def examine(self, volume, _cfg = None) :
        """
        returns volume object filled by vos examine from vol-server. 
        """
        name_or_id = PM._get_name_or_id(volume)
        command_list = [_cfg.binaries["vos"], "examine", "%s"  % name_or_id, \
            "-format", "-cell", _cfg.cell]
        return command_list, PM.examine

