from source.panel.panel_sounddata import PanelSoundData
from source.vanilla_resourcepack import VanillaResourcePack


class PanelGame(PanelSoundData):

    def __init__(self, soundwindow):
        path_soundfiles = VanillaResourcePack().get_pathlist('game')
        super().__init__(soundwindow, path_soundfiles)

    def get_pngfilepath(self, path_ogg=None):
        return './image/grass.png'
