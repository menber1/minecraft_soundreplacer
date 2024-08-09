import wx
import os
import glob


class VanillaResourcePack():

    def __init__(self):
        pass

    def get_pathlist(self, name):
        if name == 'records':
            path = './Vanilla_Resource_Pack_1.21.0/sounds/music/game/records/*.ogg'
        elif name == 'menu':
            path = './Vanilla_Resource_Pack_1.21.0/sounds/music/menu/*.ogg'
        elif name == 'game':
            path = './Vanilla_Resource_Pack_1.21.0/sounds/music/game/*.ogg'
        elif name == 'creative':
            path = './Vanilla_Resource_Pack_1.21.0/sounds/music/game/creative/*.ogg'
        elif name == 'end':
            path = './Vanilla_Resource_Pack_1.21.0/sounds/music/game/end/*.ogg'
        elif name == 'nether':
            path = './Vanilla_Resource_Pack_1.21.0/sounds/music/game/nether/*.ogg'
        elif name == 'water':
            path = './Vanilla_Resource_Pack_1.21.0/sounds/music/game/water/*.ogg'
        elif name == 'note':
            path = './Vanilla_Resource_Pack_1.21.0/sounds/note/*.ogg'
        else:
            print('VanillaResourcePack().get_pathlist() return []')
            return []

        paths = glob.glob(path)
        pathlist = []
        for filepath in paths:
            filepath = filepath.replace('\\', '/')
            pathlist.append(filepath)
        return pathlist

    def get_sound_definitions_json(self):
        return './Vanilla_Resource_Pack_1.21.0/sounds/sound_definitions.json'

    def get_sounds_json(self):
        return './Vanilla_Resource_Pack_1.21.0/sounds.json'

    def get_sounds_json_JE(self):
        return './Vanilla_Resource_Pack_1.21_JE/assets/minecraft/sounds.json'
