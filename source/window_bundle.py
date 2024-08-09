import os.path
import wx
from source.message import Message


class WindowBundle(wx.Dialog):
    WIDTH = 850
    HEIGHT = 230
    TOOLBAR_HEIGHT = 35

    def __init__(self, parent, bundle):
        wx.Frame.__init__(self, parent, title="select bundle folder", size=(self.WIDTH, self.HEIGHT))

        self.SetBackgroundColour(wx.WHITE)
        icon = wx.Icon('./image/icon_frame.ico')
        self.SetIcon(icon)

        self.soundwindow = parent

        x, y = self.soundwindow.GetPosition()
        self.SetPosition((x + 120, y + 410))

        base_toolbar = wx.Panel(self, pos=(0, 0), size=(self.WIDTH, self.TOOLBAR_HEIGHT))
        base_toolbar.SetBackgroundColour('#969696')
        self.toolbar = wx.Panel(base_toolbar, pos=(0, 0), size=(self.WIDTH, self.TOOLBAR_HEIGHT - 1))
        self.toolbar.SetBackgroundColour(wx.WHITE)

        self.button_add = wx.BitmapButton(self.toolbar, -1, wx.Bitmap('./image/button_plus.png'), pos=(20, 10),
                                          size=(16, 16))
        self.button_add.SetBitmapPressed(wx.Bitmap('./image/button_plus_on.png'))
        self.button_add.SetBitmapCurrent(wx.Bitmap('./image/button_plus_hover.png'))
        self.button_add.SetToolTip('ファイルの追加')
        self.button_add.Bind(wx.EVT_BUTTON, self.click_add_file)

        self.button_add = wx.BitmapButton(self.toolbar, -1, wx.Bitmap('./image/button_folderplus.png'), pos=(55, 10),
                                          size=(16, 16))
        self.button_add.SetBitmapPressed(wx.Bitmap('./image/button_folderplus_on.png'))
        self.button_add.SetBitmapCurrent(wx.Bitmap('./image/button_folderplus_hover.png'))
        self.button_add.SetToolTip('フォルダの追加')
        self.button_add.Bind(wx.EVT_BUTTON, self.click_add_folder)

        self.button_remove = wx.BitmapButton(self.toolbar, -1, wx.Bitmap('./image/button_cancel.png'), pos=(90, 10),
                                             size=(16, 16))
        self.button_remove.SetBitmapPressed(wx.Bitmap('./image/button_cancel_on.png'))
        self.button_remove.SetBitmapCurrent(wx.Bitmap('./image/button_cancel_hover.png'))
        self.button_remove.SetToolTip('選択を除外する')
        self.button_remove.Bind(wx.EVT_BUTTON, self.click_remove)

        wx.StaticText(self.toolbar, -1, 'copy to : <JE>./assets/minecraft/...    <BE>./...', pos=(135, 10))

        self.panel_bottom = wx.Panel(self, pos=(0, 35), size=(self.WIDTH, self.HEIGHT - self.TOOLBAR_HEIGHT))
        self.panel_bottom.SetBackgroundColour(wx.WHITE)

        self.listbox = wx.ListBox(self.panel_bottom, -1, pos=(0, 0),
                                  size=(self.WIDTH - 15, self.HEIGHT - self.TOOLBAR_HEIGHT - 40), choices=bundle,
                                  style=wx.NO_BORDER | wx.VSCROLL | wx.HSCROLL)

        self.Bind(wx.EVT_CLOSE, self.close_window)

        self.ShowModal()

    def click_add_file(self, event):
        dlg = wx.FileDialog(self, "リソースパックに同梱するファイルを選択", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            filename = os.path.basename(path)
            if filename == 'sounds.json':
                Message().show(self,
                               'sounds.json は自動生成するため同梱不可です。ファイルを組み込む場合は手動で行ってください。')
            elif filename == 'sound_definitions.json':
                Message().show(self,
                               'sound_definitions.json は自動生成するため同梱不可です。ファイルを組み込む場合は手動で行ってください。')
            elif path in self.listbox.GetStrings():
                Message().show(self, '指定されたファイルは既に追加されています。')
            elif filename == 'manifest.json':
                Message().show(self, '既存の manifest.json を同梱する場合、エクスポート時、同ファイルを作成しません。')
                self.listbox.Append(path)
            else:
                self.listbox.Append(path)
        dlg.Destroy()

    def click_add_folder(self, event):
        dlg = wx.DirDialog(self, "リソースパックに同梱するフォルダを選択", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            if path in self.listbox.GetStrings():
                Message().show(self, '指定されたフォルダは既に追加されています。')
            else:
                self.listbox.Append(path)
        dlg.Destroy()

    def click_remove(self, event):
        selected = self.listbox.GetSelection()
        if selected != wx.NOT_FOUND:
            self.listbox.Delete(selected)

    def close_window(self, event):
        self.soundwindow.get_inputpanel().set_bundle_data(self.listbox.GetItems())
        self.Destroy()
