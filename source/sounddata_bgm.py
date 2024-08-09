import wx
import os
import subprocess
from source.message import Message
from source.filedroptarget import FileDropTarget
from source.window_edittitle import EditTitleWindow
from source.wrap_statictext import WrapStaticText


class SoundDataBGM(wx.Panel):
    HEIGHT = 72
    WIDTH_OFFSET = 18

    def __init__(self, scrollwindow, panel_bgm, title, pos_):
        wx.Panel.__init__(self, scrollwindow, pos=pos_)

        self.SetBackgroundColour(wx.WHITE)
        self.line = wx.Panel(self, pos=(15, self.HEIGHT - 1))
        self.line.SetBackgroundColour('#969696')

        self.title = title
        self.path_sourcefile = ''  # 音源
        self.panel_bgm = panel_bgm

        self.statictext_title = wx.StaticText(self, -1, title, pos=(20, 10))

        self.statictext_title.Bind(wx.EVT_LEFT_UP, self.click_title)
        self.statictext_title.Bind(wx.EVT_ENTER_WINDOW, self.mouse_enter_window)

        self.button_add = wx.BitmapButton(self, -1, wx.Bitmap('./image/button_plus.png'), pos=(self.HEIGHT + 10, 40),
                                          size=(16, 16))
        self.button_add.SetBitmapPressed(wx.Bitmap('./image/button_plus_on.png'))
        self.button_add.SetBitmapCurrent(wx.Bitmap('./image/button_plus_hover.png'))
        self.button_add.SetToolTip('リスト追加')
        self.button_add.Bind(wx.EVT_BUTTON, self.click_add)

        self.button_delete = wx.BitmapButton(self, -1, wx.Bitmap('./image/button_cancel.png'),
                                             pos=(self.HEIGHT + 35, 40), size=(16, 16))
        self.button_delete.SetBitmapPressed(wx.Bitmap('./image/button_cancel_on.png'))
        self.button_delete.SetBitmapCurrent(wx.Bitmap('./image/button_cancel_hover.png'))
        self.button_delete.SetToolTip('リスト削除')
        self.button_delete.Bind(wx.EVT_BUTTON, self.click_delete)

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

    def mouse_enter_window(self, event):
        label = self.statictext_title.GetLabel()
        self.statictext_title.SetToolTip(label)

    def click_title(self, event):
        category, nowtitle = self.title.split('.')
        EditTitleWindow(self, nowtitle)

    def click_add(self, event):
        self.panel_bgm.add_sounddata()

    def click_delete(self, event):
        self.panel_bgm.delete_sounddata(self)

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

        # If the music file path is invalid, write the same in glayout sounddata_bgm.py
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

    def get_source_and_title(self):
        return self.path_sourcefile, self.title

    def replace_escape(self, path):
        return path.replace('\\', '/')

    def get_parentpanel(self):
        return self.panel_bgm

    def get_title(self):
        return self.title

    def get_sourcepath(self):
        return self.path_sourcefile

    def hide_addbutton(self):
        self.button_add.Hide()

    def show_addbutton(self):
        self.button_add.Show()

    def set_newtitle(self, newtitle):
        category, index = self.title.split('.')
        title = category + '.' + newtitle
        self.statictext_title.SetLabel(title)
        self.title = title

    def check_duplicatetitle(self, newtitle):
        return self.panel_bgm.check_duplicatetitle(newtitle)

    def get_width(self):
        width = self.panel_bgm.GetSize()[0]
        return width - 18  # offset -18

    def show(self):
        width = self.panel_bgm.GetSize()[0] - self.WIDTH_OFFSET
        self.SetSize((width, self.HEIGHT))
        self.Show()

    def hide(self):
        width = self.panel_bgm.GetSize()[0] - self.WIDTH_OFFSET
        self.SetSize((width, 0))
        self.Hide()

    def resize(self):
        size = self.panel_bgm.GetSize()
        self.SetSize((size[0] - self.WIDTH_OFFSET, self.HEIGHT))
        self.line.SetSize(size[0] - 50, 1)
        self.statictext_replacesound.resize((size[0], self.HEIGHT))
