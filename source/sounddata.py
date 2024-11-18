import wx
import os
import csv
import subprocess
import webbrowser
from source.message import Message
from source.filedroptarget import FileDropTarget
from source.wrap_statictext import WrapStaticText


class SoundData(wx.Panel):
    HEIGHT = 72
    WIDTH_OFFSET = 18

    def __init__(self, scrollwindow, panel_sounddata, path_ogg, pos_):
        wx.Panel.__init__(self, scrollwindow, pos=pos_)

        self.SetBackgroundColour(wx.WHITE)
        self.line = wx.Panel(self, pos=(15, self.HEIGHT - 1))
        self.line.SetBackgroundColour('#969696')

        self.path_ogg = path_ogg  # ogg file
        self.path_sourcefile = ''  # sound resouce
        self.flag_sound_run = False
        self.panel_sounddata = panel_sounddata

        path_pngfile = self.panel_sounddata.get_pngfilepath(path_ogg)
        self.icon = wx.StaticBitmap(self, -1, wx.Bitmap(path_pngfile), pos=(5, 2), size=(64, 64))

        title = self.get_soundtitle()
        self.statictext_recordtitle = wx.StaticText(self, -1, title, pos=(self.HEIGHT + 10, 10))

        self.button_run_record = wx.BitmapButton(self, -1, wx.Bitmap('./image/button_music.png'),
                                                 pos=(self.HEIGHT + 10, 40), size=(16, 16))
        self.button_run_record.SetBitmapPressed(wx.Bitmap('./image/button_music_on.png'))
        self.button_run_record.SetBitmapCurrent(wx.Bitmap('./image/button_music_hover.png'))
        self.button_run_record.SetToolTip('元音源再生')
        self.button_run_record.Bind(wx.EVT_BUTTON, self.click_run_record)

        self.button_clear = wx.BitmapButton(self, -1, wx.Bitmap('./image/button_cancel.png'),
                                            pos=(self.HEIGHT + 35, 40), size=(16, 16))
        self.button_clear.SetBitmapPressed(wx.Bitmap('./image/button_cancel_on.png'))
        self.button_clear.SetBitmapCurrent(wx.Bitmap('./image/button_cancel_hover.png'))
        self.button_clear.SetToolTip('指定解除')
        self.button_clear.Bind(wx.EVT_BUTTON, self.click_clear)

        self.button_select = wx.BitmapButton(self, -1, wx.Bitmap('./image/button_folder.png'),
                                             pos=(self.HEIGHT + 60, 40), size=(16, 16))
        self.button_select.SetBitmapPressed(wx.Bitmap('./image/button_folder_on.png'))
        self.button_select.SetBitmapCurrent(wx.Bitmap('./image/button_folder_hover.png'))
        self.button_select.SetToolTip('フォルダ選択')
        self.button_select.Bind(wx.EVT_BUTTON, self.click_select)

        self.button_run_soundfile = wx.BitmapButton(self, -1, wx.Bitmap('./image/button_sound.png'),
                                                    pos=(self.HEIGHT + 85, 40), size=(16, 16))
        self.button_run_soundfile.SetBitmapPressed(wx.Bitmap('./image/button_sound_on.png'))
        self.button_run_soundfile.SetBitmapCurrent(wx.Bitmap('./image/button_sound_hover.png'))
        self.button_run_soundfile.SetToolTip('ファイル再生')
        self.button_run_soundfile.Bind(wx.EVT_BUTTON, self.click_run_soundfile)

        varticalline = wx.Panel(self, -1, pos=(200, 10), size=(1, 53))
        varticalline.SetBackgroundColour('#969696')

        path_replacesound = ''
        self.statictext_replacesound = WrapStaticText(self, path_replacesound, pos=(self.HEIGHT + 140, 10))
        self.resize()

        self.SetDropTarget(FileDropTarget(self, self.statictext_replacesound))

    def get_oggfilepath(self):
        return self.path_ogg

    def get_soundtitle(self):
        basename = os.path.basename(self.path_ogg)
        name, ext = os.path.splitext(basename)
        return name

    def get_pngfilepath(self, path_sourcefile=None):
        return ''

    def click_clear(self, event):
        self.statictext_replacesound.set_label('')
        self.path_sourcefile = ''

    def click_select(self, event):

        filter = " All file(*.*) | *.*|" \
                 " WAV (*.wav;*.WAV) | *.wav;*.WAV |" \
                 " WMA (*.wma;*.WMA) | *.wma;*.WMA |" \
                 " MP3 (*.mp3;*.MP3) | *.mp3;*.MP3 |" \
                 " AAC (*.aac;*.AAC) | *.aac;*.AAC |" \
                 " M4A (*.m4a;*.M4A) | *.m4a;*.M4A |" \
                 " FLAC (*.flac;*.FLAC) | *.flac;*.FLAC |" \
                 " Vorbis (*.ogg;*.OGG) | *.ogg;*.OGG"

        with wx.FileDialog(self.button_select, '音声ファイルを指定してください。', '', '', filter) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return

            path = dialog.GetPath()
            path = self.replace_escape(path)

            if self.check_ext(path):
                self.set_sourcepath(path)
            else:
                dialog = wx.MessageDialog(self, 'サポートされない拡張子です。', 'メッセージ', style=wx.OK)
                dialog.ShowModal()
                dialog.Destroy()

    def click_run_record(self, event):

        if 'PanelNote' == self.get_parentpanel().__class__.__name__:
            path = '"' + self.path_ogg + '"'
            subprocess.run(path, shell=True)
        else:
            filename = os.path.splitext(os.path.basename(self.path_ogg))[0]
            with open('./url.csv', 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                for row in reader:
                    if row[0] == filename:
                        webbrowser.open(row[2])
                        return

    def click_run_soundfile(self, event):

        if self.path_sourcefile == '':
            return
        if not os.path.exists(self.path_sourcefile):
            Message().show(self, '指定されたファイルが見つかりません。')
            return

        path = '"' + self.path_sourcefile + '"'
        subprocess.run(path, shell=True)

    def set_sourcepath(self, sourcepath):
        self.path_sourcefile = sourcepath
        self.statictext_replacesound.set_label(sourcepath)
        if os.path.isfile(self.path_sourcefile):
            self.statictext_replacesound.SetForegroundColour(wx.BLACK)
        else:
            self.statictext_replacesound.SetForegroundColour((130, 130, 130))
        self.statictext_replacesound.Refresh()
        self.resize()

    def check_ext(self, path):
        name, ext = os.path.splitext(os.path.basename(path))
        ext = ext.lower()
        if ext in ['.wav', '.mp3', '.m4a', '.aac', '.flac', '.wma', '.ogg']:
            return True
        else:
            return False

    def get_source_and_ogg(self):
        return self.path_sourcefile, self.path_ogg

    def replace_escape(self, path):
        return path.replace('\\', '/')

    def get_parentpanel(self):
        return self.panel_sounddata

    def resize(self):
        size = self.panel_sounddata.GetSize()
        self.SetSize((size[0] - self.WIDTH_OFFSET, self.HEIGHT))
        self.line.SetSize(size[0] - 50, 1)
        self.statictext_replacesound.resize((size[0], self.HEIGHT))
