import re

import wx

from source.message import Message


class EditTitleWindow(wx.Dialog):
    WIDTH = 235
    HEIGHT = 80

    def __init__(self, sounddata_bgm, nowtitle):
        wx.Frame.__init__(self, sounddata_bgm, -1, 'edit title', size=(self.WIDTH, self.HEIGHT))

        self.SetBackgroundColour(wx.WHITE)
        self.sounddata_bgm = sounddata_bgm
        self.nowtitle = nowtitle

        self.textctrl = wx.TextCtrl(self, -1, nowtitle, pos=(15, 5), size=(165, 23))
        self.textctrl.Bind(wx.EVT_CHAR_HOOK, self.keydown_enter)

        self.button_ok = wx.BitmapButton(self, -1, wx.Bitmap('./image/button_check.png'), pos=(190, 10), size=(16, 16))
        self.button_ok.SetBitmapPressed(wx.Bitmap('./image/button_check_on.png'))
        self.button_ok.SetBitmapCurrent(wx.Bitmap('./image/button_check_hover.png'))
        self.button_ok.SetToolTip('ok')
        self.button_ok.Bind(wx.EVT_BUTTON, self.click_ok)

        self.ShowModal()

    def keydown_enter(self, event):
        if event.GetKeyCode() == wx.WXK_RETURN:
            self.set_newtitle()
        else:
            event.Skip()

    def click_ok(self, event):
        self.set_newtitle()

    def set_newtitle(self):
        newtitle = self.textctrl.GetValue()
        p = re.compile('[a-z,A-Z,0-9,_]+')

        if None == p.fullmatch(newtitle):
            Message().show(self, '使用できる文字は半角英数字、アンダーバーのみです。')
            return

        if not self.sounddata_bgm.check_duplicatetitle(newtitle):
            Message().show(self, '同一名データが存在します。')
            return

        self.sounddata_bgm.set_newtitle(newtitle)
        self.Close()
