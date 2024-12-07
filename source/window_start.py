import getpass
import os.path
import subprocess
import webbrowser
import wx
from source.config_manager import ConfigManager
from source.panel.panel_packdata import PackdataPanel
from source.window_sound import SoundWindow


class StartWindow(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Minecraft SoundReplacer v0.9.3b')

        self.SetBackgroundColour(wx.WHITE)
        self.SetSize(ConfigManager().get_size_startwindow())
        self.SetMinSize((700, 538))
        self.SetMaxSize((700, 1050))
        icon = wx.Icon('./image/icon_frame.ico')
        self.SetIcon(icon)
        self.soundwindow = None
        self.inputwindow = None
        self.packdatapanel = None

        self.toolbar = self.create_toolbar()
        self.packdatapanel = PackdataPanel(self)

        self.Bind(wx.EVT_CLOSE, self.close_frame)
        self.Bind(wx.EVT_SIZE, self.resize_frame)

    def create_toolbar(self):
        toolbar = wx.Panel(self, -1, pos=(30, 15), size=(620, 17))

        self.button_new = wx.BitmapButton(toolbar, -1, wx.Bitmap('./image/button_plus.png'), pos=(0, 0), size=(16, 16))
        self.button_new.SetBitmapPressed(wx.Bitmap('./image/button_plus_on.png'))
        self.button_new.SetBitmapCurrent(wx.Bitmap('./image/button_plus_hover.png'))
        self.button_new.SetToolTip('新しいリソースパックを作成')
        self.button_new.Bind(wx.EVT_BUTTON, self.click_new)

        self.button_folder_music = wx.BitmapButton(toolbar, -1, wx.Bitmap('./image/button_folder.png'), pos=(40, 0),
                                                   size=(16, 16))
        self.button_folder_music.SetBitmapPressed(wx.Bitmap('./image/button_folder_on.png'))
        self.button_folder_music.SetBitmapCurrent(wx.Bitmap('./image/button_folder_hover.png'))
        self.button_folder_music.SetToolTip('MusicFolder/右クリックでリンク先変更')
        self.button_folder_music.Bind(wx.EVT_BUTTON, self.click_folder_music)
        self.button_folder_music.Bind(wx.EVT_RIGHT_UP, self.rightclick_folder_music)

        self.button_folder_JE = wx.BitmapButton(toolbar, -1, wx.Bitmap('./image/button_folder.png'), pos=(80, 0),
                                                size=(16, 16))
        self.button_folder_JE.SetBitmapPressed(wx.Bitmap('./image/button_folder_on.png'))
        self.button_folder_JE.SetBitmapCurrent(wx.Bitmap('./image/button_folder_hover.png'))
        self.button_folder_JE.SetToolTip('Minecraft JE - .minecraft / resourcepacks')
        self.button_folder_JE.Bind(wx.EVT_BUTTON, self.click_folder_JE)

        self.button_folder_BE = wx.BitmapButton(toolbar, -1, wx.Bitmap('./image/button_folder.png'), pos=(120, 0),
                                                size=(16, 16))
        self.button_folder_BE.SetBitmapPressed(wx.Bitmap('./image/button_folder_on.png'))
        self.button_folder_BE.SetBitmapCurrent(wx.Bitmap('./image/button_folder_hover.png'))
        self.button_folder_BE.SetToolTip('Minecraft BE - com.mojang / resource_packs')
        self.button_folder_BE.Bind(wx.EVT_BUTTON, self.click_folder_BE)

        self.button_support = wx.BitmapButton(toolbar, -1, wx.Bitmap('./image/button_door.png'), pos=(600, 0),
                                              size=(16, 16))
        self.button_support.SetBitmapPressed(wx.Bitmap('./image/button_door_on.png'))
        self.button_support.SetBitmapFocus(wx.Bitmap('./image/button_door_hover.png'))
        self.button_support.SetToolTip(
            'ウェブサイト：https://sites.google.com/view/kusunoki-games/minecraft-soundreplacer')
        self.button_support.Bind(wx.EVT_BUTTON, self.click_website)

        return toolbar

    def close_frame(self, event):
        ConfigManager().set_size_startwindow(self.GetSize())
        self.Destroy()

    def resize_frame(self, event):
        self.packdatapanel.resize()

    def click_new(self, event):
        self.destroy_soundwindow()
        self.soundwindow = SoundWindow(self)
        self.soundwindow.Show()

    def click_folder_music(self, event):
        musicfolder = ConfigManager().get_path_musicfolder()
        if not os.path.exists(musicfolder):
            username = getpass.getuser()
            path = '"C:\\Users\\' + username + '\\Music"'
        else:
            path = musicfolder
        subprocess.run('explorer {}'.format(path))

    def rightclick_folder_music(self, event):

        dialog = wx.DirDialog(None, "フォルダを選択してください")
        if dialog.ShowModal() == wx.ID_OK:
            folder_path = dialog.GetPath()
            ConfigManager().set_path_musicfolder(folder_path)
        dialog.Destroy()

    def click_folder_JE(self, event):
        username = getpass.getuser()
        path = '"C:\\Users\\' + username + '\\AppData\\Roaming\\.minecraft\\resourcepacks"'
        subprocess.run('explorer {}'.format(path))

    def click_folder_BE(self, event):
        username = getpass.getuser()
        path = '"C:\\Users\\' + username + '\\AppData\\Local\\Packages\\Microsoft.MinecraftUWP_8wekyb3d8bbwe\\LocalState\\games\\com.mojang\\resource_packs"'
        subprocess.run('explorer {}'.format(path))

    def click_website(self, event):
        webbrowser.open('https://sites.google.com/view/kusunoki-games/minecraft-soundreplacer')

    def get_soundwindow(self):
        return self.soundwindow

    def destroy_soundwindow(self):
        if type(self.soundwindow) == SoundWindow:
            size = self.soundwindow.GetSize()
            width = size[0]
            height = size[1]

            if width >= 1936 and height >= 1056:  # 最大化で閉じた場合、デフォルトサイズに戻す。
                size = (1000, 525)
            ConfigManager().set_size_soundwindow(size)
            self.soundwindow.Destroy()
            self.soundwindow = None

    def show_soundwindow(self, data_for_soundwindow, data_for_panelinput=None):
        self.soundwindow = SoundWindow(self, data_for_soundwindow, data_for_panelinput)
        self.soundwindow.Show()

    def updatelist(self):
        self.packdatapanel.update()
