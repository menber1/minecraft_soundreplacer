import os
import wx
from source.message import Message


class PathSettingWindow(wx.Dialog):
    WIDTH = 850
    HEIGHT = 90

    def __init__(self, sounddata_bgm, path, message):
        wx.Frame.__init__(self, sounddata_bgm, -1, 'setting path - ' + message, size=(self.WIDTH, self.HEIGHT))

        self.SetBackgroundColour(wx.WHITE)
        self.sounddata_bgm = sounddata_bgm
        self.path = path

        self.textctrl = wx.TextCtrl(self, -1, path, pos=(15, 15), size=(740, 23))
        self.textctrl.Bind(wx.EVT_CHAR_HOOK, self.keydown_enter)

        self.button_ref = wx.BitmapButton(self, -1, wx.Bitmap('./image/button_folder.png'), pos=(770, 20),
                                          size=(16, 16))
        self.button_ref.SetBitmapPressed(wx.Bitmap('./image/button_folder_on.png'))
        self.button_ref.SetBitmapCurrent(wx.Bitmap('./image/button_folder_hover.png'))
        self.button_ref.SetToolTip('参照')
        self.button_ref.Bind(wx.EVT_BUTTON, self.click_reference)
        self.button_ref.SetFocus()

        self.button_ok = wx.BitmapButton(self, -1, wx.Bitmap('./image/button_check.png'), pos=(800, 20), size=(16, 16))
        self.button_ok.SetBitmapPressed(wx.Bitmap('./image/button_check_on.png'))
        self.button_ok.SetBitmapCurrent(wx.Bitmap('./image/button_check_hover.png'))
        self.button_ok.SetToolTip('OK : ファイルを指定。空欄でファイル指定解除')
        self.button_ok.Bind(wx.EVT_BUTTON, self.click_ok)

        self.ShowModal()

    def keydown_enter(self, event):
        if event.GetKeyCode() == wx.WXK_RETURN:
            self.set_path()
        else:
            event.Skip()

    def click_ok(self, event):
        self.set_path()

    def validate(self, path):
        if path == '':
            return "blank"
        if not os.path.isfile(path):
            return "not exist"
        extensions = ('.mp3', '.wav', '.wma', '.flac', '.aac', '.ogg', '.m4a')
        _, ext = os.path.splitext(path)
        if ext.lower() in extensions:
            return "yes audiofile"
        else:
            return "not audiofile"

    def set_path(self):
        path = self.textctrl.GetValue()
        ans = self.validate(path)

        if ans == "blank":
            self.sounddata_bgm.set_sourcepath('')
            self.Close()
        elif ans == "yes audiofile":
            self.sounddata_bgm.set_sourcepath(path)
            self.Close()
        elif ans == "not exist":
            Message().show(self, "存在しないファイルパスです。")
        elif ans == "not audiofile":
            Message().show(self, "音声ファイルを指定してください。")

    def click_reference(self, event):

        filter = " All file(*.*) | *.*|" \
                 " WAV (*.wav;*.WAV) | *.wav;*.WAV |" \
                 " WMA (*.wma;*.WMA) | *.wma;*.WMA |" \
                 " MP3 (*.mp3;*.MP3) | *.mp3;*.MP3 |" \
                 " AAC (*.aac;*.AAC) | *.aac;*.AAC |" \
                 " M4A (*.m4a;*.M4A) | *.m4a;*.M4A |" \
                 " FLAC (*.flac;*.FLAC) | *.flac;*.FLAC |" \
                 " Vorbis (*.ogg;*.OGG) | *.ogg;*.OGG"

        with wx.FileDialog(self.button_ref, '音声ファイルを指定してください。', '', '', filter) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return
            path = dialog.GetPath()
            self.textctrl.SetLabel(path)
