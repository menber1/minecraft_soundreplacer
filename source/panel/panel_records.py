import os

from source.panel.panel_sounddata import PanelSoundData
from source.vanilla_resourcepack import VanillaResourcePack


class PanelRecords(PanelSoundData):

    def __init__(self, soundwindow):
        path_soundfiles = VanillaResourcePack().get_pathlist('records')
        super().__init__(soundwindow, path_soundfiles)

    def get_pngfilepath(self, path_ogg=None):
        basename = os.path.basename(path_ogg)
        name, ext = os.path.splitext(basename)
        return os.path.join('./image', name + '.png')
