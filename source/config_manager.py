import configparser
import os


class ConfigManager:

    def __init__(self):
        if not os.path.exists('./config.ini'):
            self.create_configfile()

    # 'JE' or 'BE'------------------------------------
    def set_minecraft_edition(self, edition):
        config = configparser.RawConfigParser()
        config.read('./config.ini', 'utf-8')
        config.set('export', 'edition', edition)
        with open('./config.ini', 'w', encoding='utf-8') as file:
            config.write(file)

    def get_minecraft_edition(self):
        config = configparser.RawConfigParser()
        config.read('./config.ini', 'utf-8')
        return config.get('export', 'edition')

    # zip----------------------------------------------
    def set_zip_compression(self, flag):

        if flag == True:
            flag = 'True'
        else:
            flag = 'False'

        config = configparser.RawConfigParser()
        config.read('./config.ini', 'utf-8')
        config.set('export', 'zip_compression', flag)
        with open('./config.ini', 'w', encoding='utf-8') as file:
            config.write(file)

    def get_zip_compression(self):
        config = configparser.RawConfigParser()
        config.read('./config.ini', 'utf-8')
        flag = config.get('export', 'zip_compression')
        if flag == 'True':
            return True
        else:
            return False

    # version-----------------------------------------------
    def get_packformat(self, version):
        config = configparser.RawConfigParser()
        config.read('./config.ini', 'utf-8')
        packformat_csv = config.get('packformat', 'list_packformat')
        packformat_list = packformat_csv.split('|')

        for version_and_packformat in packformat_list:
            version_, packformat = version_and_packformat.split(',')
            if version_ == version:
                return int(packformat)

    def get_versionlist(self):
        config = configparser.RawConfigParser()
        config.read('./config.ini', 'utf-8')
        packformat_csv = config.get('packformat', 'list_packformat')
        packformat_list = packformat_csv.split('|')

        versionlist = []
        for ver_and_pack in packformat_list:
            version, packformat = ver_and_pack.split(',')
            versionlist.append(version)
        return versionlist

    def get_select_version(self):
        config = configparser.RawConfigParser()
        config.read('./config.ini', 'utf-8')
        version = config.get('export', 'select_version')
        if version == '':
            latest = self.get_versionlist()
            return latest[0]
        else:
            return version

    def set_select_version(self, version):
        config = configparser.RawConfigParser()
        config.read('./config.ini', 'utf-8')
        config.set('export', 'select_version', version)
        with open('./config.ini', 'w', encoding='utf-8') as file:
            config.write(file)

    # window size -------------------------------------------
    def get_size_startwindow(self):
        try:
            config = configparser.RawConfigParser()
            config.read('./config.ini', 'utf-8')
            size = config.get('window', 'size_start')
            width, height = size.split(',')
            return (int(width), int(height))
        except UnicodeDecodeError:
            return int(700), int(538)

    def set_size_startwindow(self, size):
        config = configparser.RawConfigParser()
        config.read('./config.ini', 'utf-8')
        config.set('window', 'size_start', str(size[0]) + ',' + str(size[1]))
        with open('./config.ini', 'w', encoding='utf-8') as file:
            config.write(file)

    def get_size_soundwindow(self):
        config = configparser.RawConfigParser()
        config.read('./config.ini', 'utf-8')
        size = config.get('window', 'size_sound')
        width, height = size.split(',')
        return (int(width), int(height))

    def set_size_soundwindow(self, size):
        config = configparser.RawConfigParser()
        config.read('./config.ini', 'utf-8')
        config.set('window', 'size_sound', str(size[0]) + ',' + str(size[1]))
        with open('./config.ini', 'w', encoding='utf-8') as file:
            config.write(file)

    # folder path ---------------------------------------------

    def get_path_musicfolder(self):
        config = configparser.RawConfigParser()
        config.read('./config.ini', 'utf-8')
        path = config.get('linkbutton', 'musicfolder')
        return path

    def set_path_musicfolder(self, path):
        if not os.path.isdir(path):
            path = ''
        config = configparser.RawConfigParser()
        config.read('./config.ini', 'utf-8')
        config.set('linkbutton', 'musicfolder', path)
        with open('./config.ini', 'w', encoding='utf-8') as file:
            config.write(file)

    def get_path_savefolder(self):
        config = configparser.RawConfigParser()
        config.read('./config.ini', 'utf-8')
        path = config.get('export', 'savefolder')
        return path

    def set_path_savefolder(self, path):
        if not os.path.isdir(path):
            path = ''
        config = configparser.RawConfigParser()
        config.read('./config.ini', 'utf-8')
        config.set('export', 'savefolder', path)
        with open('./config.ini', 'w', encoding='utf-8') as file:
            config.write(file)

    def get_musiclist(self, category):
        config = configparser.RawConfigParser()
        config.read('./config.ini', 'utf-8')
        csv = config.get('music', category)
        musiclist = csv.split(',')
        return musiclist

    def create_configfile(self):
        config = configparser.ConfigParser()

        config['export'] = {
            'edition': 'BE',
            'zip_compression': True,
            'select_version': '',
            'savefolder': ''
        }

        config['packformat'] = {
            'list_packformat': '1.21.6,63|1.21.5,55|1.21.4,46|1.21.3,42|1.21,34|1.20.6,32|1.20.4,22|1.20.2,18|1.20,15|1.19.4,13|1.19.3,12|1.19,9|1.18,8|1.17,7|1.16,6'
        }

        config['window'] = {
            'size_start': '700,538',
            'size_sound': '1000,525'
        }

        config['linkbutton'] = {
            'musicfolder': ''
        }

        config['music'] = {
            'record': '11,13,5,blocks,cat,chirp,creator,creator_music_box,far,mall,mellohi,otherside,pigstep,precipice,relic,stal,strad,wait,ward,tears',
            'menu': 'menu1,menu2,menu3,menu4',
            'game': 'a_familiar_room,aerie,ancestry,an_ordinary_day,bromeliad,calm1,calm2,calm3,comforting_memories,'
                    'crescent_dunes,deeper,echo_in_the_wind,eld_unknown,endless,featherfall,firebugs,floating_dream,hal1,hal2,hal3,hal4,infinite_amethyst,'
                    'komorebi,labyrinthine,left_to_bloom,nuance1,nuance2,one_more_day,piano1,piano2,piano3,pokopoko,puzzlebox,stand_tall,watcher,wending,yakusoku,'
                    'broken_clocks,below_and_above,os_piano,fireflies,lilypad',
            'creative': 'creative1,creative2,creative3,creative4,creative5,creative6',
            'end': 'boss,credits,end',
            'nether': 'chrysopoeia,nether1,nether2,nether3,nether4,rubedo,so_below',
            'water': 'axolotl,dragon_fish,shuniji',
            'note': 'banjo,bass,bd,bell,bit,cow_bell,didgeridoo,flute,guitar,harp,hat,icechime,iron_xylophone,pling,'
                    'snare,xylobone'
        }

        with open('./config.ini', 'w', encoding='utf-8') as f:
            config.write(f)
