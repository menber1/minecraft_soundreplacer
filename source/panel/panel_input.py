import json
import os
import shutil
import threading
import wx
import uuid
import ctypes
import logging
from ctypes import wintypes
from PIL import Image
from source.config_manager import ConfigManager
from source.database_helper import DatabaseHelper
from source.ffmpeg_manager import FFmpegManager
from source.message import Message
from source.vanilla_resourcepack import VanillaResourcePack
from source.window_bundle import WindowBundle


class ImageDropTarget(wx.FileDropTarget):

    def __init__(self, inputpanel):
        wx.FileDropTarget.__init__(self)
        self.inputpanel = inputpanel

    def OnDropFiles(self, x, y, files):
        path = files[0]
        self.inputpanel.set_bitmap(path)
        return True


class PanelInput(wx.Panel):
    WIDTH = 974
    HEIGHT = 435
    ICON_DEFAULT = './image/pack_icon_default.png'

    def __init__(self, soundwindow, database_packdata=None):
        wx.Panel.__init__(self, soundwindow, pos=(110, 120), size=(self.WIDTH, self.HEIGHT))

        self._set_logging()
        self.SetBackgroundColour(wx.WHITE)
        self.icon = self.ICON_DEFAULT
        self.soundwindow = soundwindow
        self.database_index = -1
        self.bundle = []

        self.button_icon = wx.BitmapButton(self, -1, wx.Bitmap(self.ICON_DEFAULT), pos=(15, 10), size=(128, 128))
        self.button_icon.Bind(wx.EVT_BUTTON, self.click_icon)

        self.button_clearicon = wx.BitmapButton(self, -1, wx.Bitmap('./image/button_cancel.png'), pos=(15, 145),
                                                size=(16, 16))
        self.button_clearicon.SetBitmapPressed(wx.Bitmap('./image/button_cancel_on.png'))
        self.button_clearicon.SetBitmapCurrent(wx.Bitmap('./image/button_cancel_hover.png'))
        self.button_clearicon.SetToolTip('アイコン画像クリア')
        self.button_clearicon.Bind(wx.EVT_BUTTON, self.click_clearicon)

        wx.StaticText(self, -1, 'name :', pos=(160, 12))
        wx.StaticText(self, -1, 'description :', pos=(160, 45))
        wx.StaticText(self, -1, 'header uuid :', pos=(160, 78))
        wx.StaticText(self, -1, 'modules uuid :', pos=(160, 111))
        wx.StaticText(self, -1, 'version :', pos=(160, 144))
        wx.StaticText(self, -1, 'save folder :', pos=(160, 177))
        wx.StaticText(self, -1, 'version :', pos=(160, 223))

        self.textctrl_name = wx.TextCtrl(self, -1, pos=(250, 10), size=(467, 23))
        self.textctrl_description = wx.TextCtrl(self, -1, pos=(250, 43), size=(467, 23))
        self.textctrl_header_uuid = wx.TextCtrl(self, -1, str(uuid.uuid4()), pos=(250, 76), size=(467, 23))
        self.textctrl_modules_uuid = wx.TextCtrl(self, -1, str(uuid.uuid4()), pos=(250, 109), size=(467, 23))
        self.textctrl_version = wx.TextCtrl(self, -1, pos=(250, 142), size=(100, 23))
        self.textctrl_version.SetLabel('0,0,1')

        self.textctrl_save = wx.TextCtrl(self, -1, pos=(250, 175), size=(467, 23))
        savepath = ConfigManager().get_path_savefolder()
        if os.path.isdir(savepath):
            self.textctrl_save.SetValue(savepath)

        self.button_header_uuid = wx.BitmapButton(self, -1, wx.Bitmap('./image/button_random.png'), pos=(725, 80),
                                                  size=(16, 16))
        self.button_header_uuid.SetBitmapPressed(wx.Bitmap('./image/button_random_on.png'))
        self.button_header_uuid.SetBitmapCurrent(wx.Bitmap('./image/button_random_hover.png'))
        self.button_header_uuid.SetToolTip('uuid生成')
        self.button_header_uuid.Bind(wx.EVT_BUTTON, self.click_header_newid)

        self.button_modules_uuid = wx.BitmapButton(self, -1, wx.Bitmap('./image/button_random.png'), pos=(725, 113),
                                                   size=(16, 16))
        self.button_modules_uuid.SetBitmapPressed(wx.Bitmap('./image/button_random_on.png'))
        self.button_modules_uuid.SetBitmapCurrent(wx.Bitmap('./image/button_random_hover.png'))
        self.button_modules_uuid.SetToolTip('uuid生成')
        self.button_modules_uuid.Bind(wx.EVT_BUTTON, self.click_modules_newid)

        self.button_reference = wx.BitmapButton(self, -1, wx.Bitmap('./image/button_folder.png'), pos=(725, 179),
                                                size=(16, 16))
        self.button_reference.SetBitmapPressed(wx.Bitmap('./image/button_folder_on.png'))
        self.button_reference.SetBitmapCurrent(wx.Bitmap('./image/button_folder_hover.png'))
        self.button_reference.SetToolTip('保存先フォルダ選択')
        self.button_reference.Bind(wx.EVT_BUTTON, self.click_reference)

        versionlist = ConfigManager().get_versionlist()
        self.combobox_version = wx.ComboBox(self, -1, choices=versionlist, style=wx.CB_READONLY, size=(60, 23),
                                            pos=(215, 220))
        v = ConfigManager().get_select_version()
        self.combobox_version.SetStringSelection(v)
        self.combobox_version.SetToolTip('JE用version設定')

        self.radiobutton_JE = wx.RadioButton(self, -1, 'JE', pos=(300, 225))
        self.radiobutton_BE = wx.RadioButton(self, -1, 'BE', pos=(340, 225))

        self.checkbox_zip_compression = wx.CheckBox(self, -1, 'ZIP', pos=(390, 225))
        self.checkbox_zip_compression.SetToolTip('JE : zip圧縮化 | BE : mcpack化 | 手動カスタムする場合のみoff')
        if ConfigManager().get_zip_compression():
            self.checkbox_zip_compression.SetValue(True)
        else:
            self.checkbox_zip_compression.SetValue(False)

        edition = ConfigManager().get_minecraft_edition()

        if edition == 'JE':
            self.radiobutton_JE.SetValue(True)
        elif edition == 'BE':
            self.radiobutton_BE.SetValue(True)

        self.label_bundle = wx.StaticText(self, -1, 'bundle : 0', pos=(440, 225))

        self.button_bundle = wx.BitmapButton(self, -1, wx.Bitmap('./image/button_folder.png'), pos=(505, 225),
                                             size=(16, 16))
        self.button_bundle.SetBitmapPressed(wx.Bitmap('./image/button_folder_on.png'))
        self.button_bundle.SetBitmapCurrent(wx.Bitmap('./image/button_folder_hover.png'))
        self.button_bundle.SetToolTip('リソースパックに同梱するフォルダを選択')
        self.button_bundle.Bind(wx.EVT_BUTTON, self.click_bundle)

        self.button_save = wx.Button(self, -1, 'save', pos=(550, 220), size=(80, 25))
        self.button_save.Bind(wx.EVT_BUTTON, self.click_save)

        self.button_export = wx.Button(self, -1, 'export', pos=(640, 220), size=(80, 25))
        self.button_export.Bind(wx.EVT_BUTTON, self.click_export)

        self.SetDropTarget(ImageDropTarget(self))
        self.set_packdata(database_packdata)

    def click_icon(self, event):
        with wx.FileDialog(self.button_icon, '画像ファイルを指定してください。') as dialog:

            if dialog.ShowModal() == wx.ID_CANCEL:
                return

            path = dialog.GetPath()
            if not os.path.exists(path):
                Message().show(self, '指定されたファイルが見つかりません。')
                return

            self.set_bitmap(path)

    def click_clearicon(self, event):
        self.icon = self.ICON_DEFAULT
        bmp = wx.Bitmap(self.ICON_DEFAULT)
        self.button_icon.SetBitmap(bmp)

    def click_header_newid(self, event):
        id_ = str(uuid.uuid4())
        self.textctrl_header_uuid.SetLabel(id_)

    def click_modules_newid(self, event):
        id_ = str(uuid.uuid4())
        self.textctrl_modules_uuid.SetLabel(id_)

    def click_reference(self, event):
        dialog = wx.DirDialog(self, style=wx.DD_DEFAULT_STYLE, message=".mcpackの保存先フォルダを選択")
        ans = dialog.ShowModal()
        if ans == wx.ID_OK:
            self.textctrl_save.SetLabel(dialog.GetPath())

    def click_bundle(self, event):
        WindowBundle(self.soundwindow, self.bundle)

    def click_save(self, event):

        if not self.database_index == -1:
            if not Message().yes_no(self, '設定を上書きしますか？'):
                return

        ConfigManager().set_minecraft_edition(self.get_selectedition())
        ConfigManager().set_zip_compression(self.checkbox_zip_compression.GetValue())
        ConfigManager().set_select_version(self.combobox_version.GetStringSelection())
        ConfigManager().set_path_savefolder(self.textctrl_save.GetValue())

        name = self.textctrl_name.GetValue()
        description = self.textctrl_description.GetValue()
        header_uuid = self.textctrl_header_uuid.GetValue()
        modules_uuid = self.textctrl_modules_uuid.GetValue()
        version = self.textctrl_version.GetValue()
        bundle = self.bundle

        if name == '':
            Message().show(self, 'name が空欄です。')
            return

        elif header_uuid == '':
            Message.show(self, 'header uuid が空欄です。')
            return

        elif modules_uuid == '':
            Message.show(self, 'modules uuid が空欄です。')
            return

        if self.save_database(self.database_index, name, self.icon, description, header_uuid, modules_uuid, version,
                              bundle):  # 20230209
            Message().show(self, '設定を保存しました。')
            self.soundwindow.get_startwindow().updatelist()
            self.soundwindow.Close()

    def click_export(self, event):
        try:
            name = self.textctrl_name.GetValue()
            description = self.textctrl_description.GetValue()
            header_uuid = self.textctrl_header_uuid.GetValue()
            modules_uuid = self.textctrl_modules_uuid.GetValue()
            version = self.textctrl_version.GetValue()
            savepath = self.textctrl_save.GetValue()
            bandle = self.bundle

            if name == '':
                Message().show(self, 'name が空欄です。')
                return

            elif header_uuid == '':
                Message().show(self, 'header uuid が空欄です。')
                return

            elif modules_uuid == '':
                Message().show(self, 'modules uuid が空欄です。')
                return

            elif self.bundle != []:
                for path_bundle_data in self.bundle:
                    is_dir = os.path.isdir(path_bundle_data)
                    is_file = os.path.isfile(path_bundle_data)
                    if not is_dir and not is_file:
                        Message().show(self, '同梱データに無効なパス：' + path_bundle_data)
                        return

            edition = self.get_selectedition()
            ConfigManager().set_minecraft_edition(edition)
            ConfigManager().set_select_version(self.combobox_version.GetStringSelection())

            # Export destination file exists -------------------------------------------------------

            if savepath == '':
                savepath = self.get_desktoppath()

            if not os.path.isdir(savepath):
                Message().show(self, '保存先を指定してください。')
                return

            ConfigManager().set_path_savefolder(savepath)

            savepath = savepath.replace('\\', '/')
            resourcepack = ''

            flag_zip = self.checkbox_zip_compression.GetValue()  # 圧縮指定True zip圧縮処理前に再度取得している。

            if edition == 'BE' and flag_zip == True:
                resourcepack = os.path.join(savepath, name + '.mcpack')
            elif edition == 'JE' and flag_zip == True:
                resourcepack = os.path.join(savepath, name + '.zip')
            else:
                resourcepack = os.path.join(savepath, name)  # BE JE どちらも拡張子無しのフォルダ名

            resourcepack = resourcepack.replace('\\', '/')

            if os.path.exists(resourcepack):
                ans = Message().yes_no(self, 'エクスポート先に同一名のリソースパックが存在します。削除しますか？')
                if ans:
                    if flag_zip:
                        os.remove(resourcepack)
                    else:
                        shutil.rmtree(resourcepack)
                else:
                    return

            # Folder creation, json creation, additional folder ------------------------------------------------

            if edition == 'BE':
                self.clear_temp()
                self._json_in_blankpack_BE()

                if not self._is_manifest_json(self.bundle):
                    self._manifest_in_blankpack(name, description, header_uuid, modules_uuid, version)

                self._add_bundle_data('BE', self.bundle)

            elif edition == 'JE':
                self.clear_temp()
                self._json_in_blankpack_JE()
                self._mcmeta_in_blankpack(description)
                self._add_bundle_data('JE', self.bundle)

            # generate icon -----------------------------------------------------------------------

            self._icon_in_blankpack(self.icon, edition)

            # generate oggfile store --------------------------------------------------------------

            if not self._newsource_in_blankpack(edition):
                return

            # zip compression ---------------------------------------------------------------------------

            flag_zip = self.checkbox_zip_compression.GetValue()  # 圧縮指定がTrue 上書き判定時に一度flag_zipを取得しているが、ここでも取得。
            ConfigManager().set_zip_compression(flag_zip)

            savepath_name = savepath + '/' + name

            if flag_zip == True and edition == 'JE':
                shutil.make_archive(savepath_name, 'zip', root_dir='./temp')

            elif flag_zip == True and edition == 'BE':
                '''
                保存場所に同一名.zipが存在する場合、.mcpackにリネームする前に上書きされてしまう為、
                tempフォルダを作成し、一旦、.zipを保存、ファイルコピー&リネームで保存先に移す。
                '''
                savepath_temp = savepath + '/temp'
                os.mkdir(savepath_temp)
                savepath_temp_name = savepath_temp + '/' + name
                shutil.make_archive(savepath_temp_name, 'zip', root_dir='./temp')
                shutil.move(savepath_temp_name + '.zip', savepath_name + '.mcpack')
                os.rmdir(savepath_temp)
            else:
                shutil.copytree('./temp', savepath_name)

            # export complate -------------------------------------------------------------------

            Message().show(self, 'リソースパックを作成しました。')
            self.save_database(self.database_index, name, self.icon, description, header_uuid, modules_uuid, version,
                               bandle)
            self.soundwindow.get_startwindow().updatelist()
            self.soundwindow.Close()

        except PermissionError as e:
            self._logging(e,
                          'PermissionError : エクスポート失敗。ファイルアクセス権限に問題があります。処理を中断します。')

        except UnicodeDecodeError as e:
            self._logging(e,
                          'UnicodeDecodeError : エクスポート失敗。ファイルエンコードに問題があります。処理を中断します。')

        except FileNotFoundError as e:
            self._logging(e, 'FileNotFoundError : エクスポート失敗。存在しないファイルへのアクセス。処理を中断します。')

        except Exception as e:
            self._logging(e, 'Error : エクスポートに失敗しました。処理を中断します。')

    def get_selectedition(self):
        if self.radiobutton_BE.GetValue():
            return 'BE'

        if self.radiobutton_JE.GetValue():
            return 'JE'

    def set_bitmap(self, path):

        if not os.path.exists(path):
            self.icon = self.ICON_DEFAULT
            bmp = wx.Bitmap(self.icon)
            self.button_icon.SetBitmap(bmp)
            return

        im = Image.open(path)
        width, height = im.size

        if width < height:  # 縦長
            trimsize = int((height - width) / 2)
            im = im.crop((0, trimsize, width, trimsize + width))

        elif height < width:
            trimsize = int((width - height) / 2)
            im = im.crop((trimsize, 0, trimsize + height, height))

        im = im.resize((128, 128))
        self.icon = os.path.join('./image_user', os.path.basename(path))

        im.save(self.icon, quality=95, format='PNG', icc_profile=None)
        bmp = wx.Bitmap(self.icon)
        self.button_icon.SetBitmap(bmp)

    def set_bundle_data(self, pathlist):
        self.bundle = pathlist
        self.label_bundle.SetLabel("bundle: " + str(len(self.bundle)))

    def save_database(self, index, name, icon, description, header_uuid, modules_uuid, version, bundle):  # 20230209

        newsourcelist = self.soundwindow.get_newsourcelist()

        if len(newsourcelist) == 0:
            Message().error(self, '音源が設定されていません。#4')
            return False

        if index == -1:
            DatabaseHelper().insert_record(name, icon, description, header_uuid, modules_uuid, version, newsourcelist,
                                           bundle)
        else:
            DatabaseHelper().update_record(index, name, icon, description, header_uuid, modules_uuid, version,
                                           newsourcelist, bundle)
        return True

    def get_desktoppath(self):
        desktop = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH") + "/Desktop"
        if os.path.isdir(desktop):
            return desktop

        desktop = os.path.expanduser('~/Desktop')
        if os.path.isdir(desktop):
            return desktop

        CSIDL_DESKTOP = 0x0000
        SHGFP_TYPE_CURRENT = 0
        buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_DESKTOP, None, SHGFP_TYPE_CURRENT, buf)
        if os.path.isdir(buf.value):
            return buf.value

        return ''  # desktop path 未取得。

    def _json_in_blankpack_BE(self):

        # copy sound_definitions.json -----------------------------------------------------------------

        os.makedirs('./temp/sounds')
        vanilla = VanillaResourcePack()
        sound_definitions_json = vanilla.get_sound_definitions_json()
        dist = os.path.join('./temp', 'sounds', os.path.basename(sound_definitions_json))
        shutil.copyfile(sound_definitions_json, dist)

        # postscript sound_definitions.json -----------------------------------------------------------------

        titlelist = self._get_addtitlelist_definitionsjson()

        if not len(titlelist) == 0:
            self._appendblock_definitionsjson(titlelist, dist)

        # copy sounds.json -----------------------------------------------------------------

        sounds_json = vanilla.get_sounds_json()
        dist = os.path.join('./temp', os.path.basename(sounds_json))
        shutil.copyfile(sounds_json, dist)

    def _json_in_blankpack_JE(self):

        # copy sound.json -----------------------------------------------------------------

        os.makedirs('./temp/assets/minecraft/sounds', exist_ok=True)
        vanilla = VanillaResourcePack()
        sounds_json = vanilla.get_sounds_json_JE()
        dist = os.path.join('./temp/assets/minecraft', os.path.basename(sounds_json))
        shutil.copyfile(sounds_json, dist)

        # postscript sound.json -----------------------------------------------------------------

        titlelist = self._get_addtitlelist_definitionsjson()

        if not len(titlelist) == 0:
            self._appendblock_definitionsjson_JE(titlelist, dist)

    def clear_temp(self):
        shutil.rmtree('./temp')
        os.mkdir('./temp')

    def _icon_in_blankpack(self, icon, minecraft_edition):
        if minecraft_edition == 'BE':
            shutil.copyfile(icon, './temp/pack_icon.png')
        elif minecraft_edition == 'JE':
            shutil.copyfile(icon, './temp/pack.png')

    def _manifest_in_blankpack(self, name, description, header_uuid, modules_uuid, version):

        json_template = './Vanilla_Resource_Pack_BE/manifest.json'
        json_new = './temp/manifest.json'

        version = self.convert_int_version(version)

        with open(json_template) as templatefile:
            dict_ = json.load(templatefile)

            dict_['header']['description'] = description
            dict_['header']['name'] = name
            dict_['header']['uuid'] = header_uuid
            dict_['header']['version'] = version
            dict_['modules'][0]['description'] = description
            dict_['modules'][0]['uuid'] = modules_uuid
            dict_['modules'][0]['version'] = version

        with open(json_new, 'w') as newfile:
            json.dump(dict_, newfile)

    def _mcmeta_in_blankpack(self, description):

        description = description.replace('n\\', '')
        select_version = self.combobox_version.GetStringSelection()
        pack_format = ConfigManager().get_packformat(select_version)

        str_ = {
            "pack": {
                "pack_format": pack_format,
                "description": description
            }
        }

        path_current = os.getcwd()
        path_pack_mcmeta = os.path.join(path_current, 'temp', 'pack.mcmeta')
        with open(path_pack_mcmeta, 'w') as f:
            json.dump(str_, f, ensure_ascii=False)

    def _newsource_in_blankpack(self, minecraft_edition):

        newsourcelist = self.soundwindow.get_newsourcelist()

        if len(newsourcelist) == 0:
            Message().error(self, '音源が設定されていません。#3')
            return False

        for newsource, ogg in newsourcelist:
            filename = os.path.basename(newsource)  # 20240404
            if not os.path.exists(newsource):
                Message().show(self, filename + ' が見つかりません。処理を中断します。')
                return False

        thread_processffmpeg = threading.Thread(
            target=self.thread_processffmpeg(newsourcelist, minecraft_edition))  # progressDialog 非表示のため、第三引数省略。
        thread_processffmpeg.start()
        thread_processffmpeg.join()

        return True

    def _add_bundle_data(self, edition, datalist):
        for path_x in datalist:
            if edition == 'JE':
                path_dist = os.path.join('./temp/assets/minecraft', os.path.basename(path_x))
                if os.path.isdir(path_x):
                    shutil.copytree(path_x, path_dist)
                elif os.path.isfile(path_x):
                    shutil.copy(path_x, path_dist)
            elif edition == 'BE':
                path_dist = os.path.join('./temp', os.path.basename(path_x))
                if os.path.isdir(path_x):
                    shutil.copytree(path_x, path_dist)
                if os.path.isfile(path_x):
                    shutil.copy(path_x, path_dist)

    def convert_int_version(self, version):

        new_version = []
        list_ = version.split(',')
        new_version.append(int(list_[0]))
        new_version.append(int(list_[1]))
        new_version.append(int(list_[2]))
        return new_version

    def thread_processffmpeg(self, newsourcelist, minecraft_edition):

        ffmpeg = FFmpegManager()
        batfile = ffmpeg.create_batfile()

        for newsource, ogg in newsourcelist:
            distdir = self.get_distdir(ogg, minecraft_edition)
            os.makedirs(distdir, exist_ok=True)

            category = self._check_originalsound(ogg)

            if category == 'bgm' or category == 'se':
                c, index = ogg.split('.')
                oggfile = distdir + '/' + str(index) + '.ogg'
            else:
                basename = os.path.basename(ogg)
                '''
                For some reason, the same bass sound is assigned to bass.ogg 
                and bassattack.ogg in the sound block. bass.ogg does not seem to be used.
                '''
                if basename == 'bass.ogg':
                    basename = 'bassattack.ogg'

                # In JE, it is called pigstep.ogg, and in BE, it is called pigstep_master.ogg.
                if basename == 'pigstep.ogg' and minecraft_edition == 'BE':
                    basename = 'pigstep_master.ogg'

                oggfile = distdir + '/' + basename

            above_dir = os.path.basename(os.path.dirname(oggfile))

            if above_dir == 'records' or above_dir == 'note' or above_dir == 'se':  # レコード、音ブロック、効果音のみモノラル変換
                ffmpeg.write_batfile(batfile, newsource, oggfile, mono=True)
            else:
                ffmpeg.write_batfile(batfile, newsource, oggfile)

        ffmpeg.close_batfile(batfile)
        ffmpeg.run_batfile()

    def get_distdir(self, ogg, minecraft_edition):
        cm = ConfigManager()
        bgmlist_record = cm.get_musiclist('record')
        bgmlist_menu = cm.get_musiclist('menu')
        bgmlist_game = cm.get_musiclist('game')
        bgmlist_creative = cm.get_musiclist('creative')
        bgmlist_end = cm.get_musiclist('end')
        bgmlist_nether = cm.get_musiclist('nether')
        bgmlist_water = cm.get_musiclist('water')
        bgmlist_note = cm.get_musiclist('note')

        category = self._check_originalsound(ogg)

        if category == 'bgm' or category == 'se':
            name = category
        else:
            name, ext = os.path.splitext(os.path.basename(ogg))

        # BE //////////////////////////////////////////////////
        if minecraft_edition == 'BE':
            if name in bgmlist_record:
                return './temp/sounds/music/game/records'

            elif name in bgmlist_menu:
                return './temp/sounds/music/menu'

            elif name in bgmlist_game:
                return './temp/sounds/music/game'

            elif name in bgmlist_creative:
                return './temp/sounds/music/game/creative'

            elif name in bgmlist_end:
                return './temp/sounds/music/game/end'

            elif name in bgmlist_nether:
                return './temp/sounds/music/game/nether'

            elif name in bgmlist_water:
                return './temp/sounds/music/game/water'

            elif name in bgmlist_note:
                return './temp/sounds/note'

            elif name == 'bgm':
                return './temp/sounds/bgm'

            elif name == 'se':
                return './temp/sounds/se'

        # JE //////////////////////////////////////////////////
        # In JE, new songs have a different hierarchy. See sounds.json
        elif minecraft_edition == 'JE':

            if name in bgmlist_record:
                return './temp/assets/minecraft/sounds/records'

            elif name in bgmlist_menu:
                return './temp/assets/minecraft/sounds/music/menu'

            elif name in bgmlist_game:
                if name in ['aerie', 'firebugs', 'labyrinthine']:
                    return './temp/assets/minecraft/sounds/music/game/swamp'
                else:
                    return './temp/assets/minecraft/sounds/music/game'

            elif name in bgmlist_creative:
                return './temp/assets/minecraft/sounds/music/game/creative'

            elif name in bgmlist_end:
                return './temp/assets/minecraft/sounds/music/game/end'

            elif name in bgmlist_nether:
                if name == 'chrysopoeia':
                    return './temp/assets/minecraft/sounds/music/game/nether/crimson_forest'
                elif name == 'rubedo':
                    return './temp/assets/minecraft/sounds/music/game/nether/nether_wastes'
                elif name == 'so_below':
                    return './temp/assets/minecraft/sounds/music/game/nether/soulsand_valley'
                else:
                    return './temp/assets/minecraft/sounds/music/game/nether'

            elif name in bgmlist_water:
                return './temp/assets/minecraft/sounds/music/game/water'

            elif name in bgmlist_note:
                return './temp/assets/minecraft/sounds/note'

            elif name == 'bgm':
                return './temp/assets/minecraft/sounds/bgm'

            elif name == 'se':
                return './temp/assets/minecraft/sounds/se'

    def get_ext(self, path):
        basename = os.path.basename(path)
        base, ext = os.path.splitext(basename)
        return ext

    def get_filename_noext(self, path):
        basename = os.path.basename(path)
        name, ext = os.path.splitext(basename)
        return name

    def set_packdata(self, packdata):
        if packdata == None: return
        self.database_index = packdata[0]
        self.textctrl_name.SetLabel(packdata[1])
        self.set_bitmap(packdata[2])
        self.textctrl_description.SetLabel(packdata[3])
        self.textctrl_header_uuid.SetLabel(packdata[4])
        self.textctrl_modules_uuid.SetLabel(packdata[5])
        self.textctrl_version.SetLabel(packdata[6])
        self.bundle = packdata[7]
        self.label_bundle.SetLabel('bundle : ' + str(len(self.bundle)))

    def _get_addtitlelist_definitionsjson(self):

        newsourcelist = self.soundwindow.get_newsourcelist()
        addlist = []

        for resource, title in newsourcelist:

            ans = self._check_originalsound(title)
            if ans == 'bgm' or ans == 'se':
                addlist.append(title)

        return addlist  # bgm.1 bgm.2 se.1 se.2 ・・・

    def _appendblock_definitionsjson(self, titlelist, definitions_json):

        addlist = {}

        for title in titlelist:
            category, index = title.split('.')

            if category == 'bgm':

                block = {
                    title: {
                        'category': 'music',
                        'sounds': [
                            {
                                'name': 'sounds/bgm/' + index,
                                'stream': True,
                                'volume': 0.3,
                                'load_on_low_memory': True
                            }
                        ]
                    }
                }

            elif category == 'se':

                block = {
                    title: {
                        'sounds': [
                            {
                                'name': 'sounds/se/' + index,
                                'stream': True,
                                'volume': 0.3,
                                'load_on_low_memory': True
                            }
                        ]
                    }
                }

            addlist.update(block)

        with open(definitions_json, 'r') as jsonfile:
            jsonall = json.load(jsonfile)

        jsonall['sound_definitions'].update(addlist)

        with open(definitions_json, 'w') as f:
            json.dump(jsonall, f, indent=4)

    def _appendblock_definitionsjson_JE(self, titlelist, sounds_json):

        addlist = {}

        for title in titlelist:
            category, index = title.split('.')

            if category == 'bgm':

                block = {
                    title: {
                        'sounds': [
                            {
                                'name': 'bgm/' + index,
                                'stream': True
                            }
                        ]
                    }
                }

            elif category == 'se':

                block = {
                    title: {
                        'sounds': [
                            {
                                'name': 'se/' + index,
                                'stream': True
                            }
                        ]
                    }
                }

            addlist.update(block)

        with open(sounds_json, 'r') as jsonfile:
            jsonall = json.load(jsonfile)

        jsonall.update(addlist)

        with open(sounds_json, 'w') as f:
            json.dump(jsonall, f, indent=4)

    def _check_originalsound(self, path):

        list_ = path.split('.')

        if len(list_) == 2:
            if list_[0] == 'bgm':
                return 'bgm'
            elif list_[0] == 'se':
                return 'se'
            else:
                return None
        else:
            return None

    def _set_logging(self):
        log_format = '[%(asctime)s] ---------------------------------------------------------------------------------------'
        logging.basicConfig(filename='error.log', level=logging.ERROR, format=log_format)

    def _logging(self, e, message):
        logging.error(f'{e}', exc_info=True)
        Message().show(self, message)

    def _is_manifest_json(self, bundle_data_list):
        for path in bundle_data_list:
            filename = os.path.basename(path)
            if filename == 'manifest.json':
                return True
            return False
