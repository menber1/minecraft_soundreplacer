import os
from source.panel.panel_sounddata import PanelSoundData
from source.vanilla_resourcepack import VanillaResourcePack


class PanelNote(PanelSoundData):

    def __init__(self, soundwindow):
        path_soundfiles = VanillaResourcePack().get_pathlist('note')
        super().__init__(soundwindow, path_soundfiles)

    def get_pngfilepath(self, path_ogg=None):

        ogg = os.path.basename(path_ogg)
        name, ext = os.path.splitext(ogg)

        if name == 'banjo':
            return './image/hay_block.png'
        elif name == 'bass':
            return './image/woodplank.png'
        elif name == 'bd':
            return './image/stone.png'
        elif name == 'bell':
            return './image/gold_block.png'
        elif name == 'bit':
            return './image/emerald_block.png'
        elif name == 'cow_bell':
            return './image/soul_sand.png'
        elif name == 'didgeridoo':
            return './image/pumpkin.png'
        elif name == 'flute':
            return './image/clay.png'
        elif name == 'guitar':
            return './image/wool.png'
        elif name == 'harp':
            return './image/grass.png'
        elif name == 'hat':
            return './image/glass.png'
        elif name == 'icechime':
            return './image/packed_ice.png'
        elif name == 'iron_xylophone':
            return './image/iron_block.png'
        elif name == 'pling':
            return './image/glowstone.png'
        elif name == 'snare':
            return './image/sand.png'
        elif name == 'xylobone':
            return './image/bone_block.png'
        else:
            return './image/grass.png'
