import wx


class SearchBar(wx.Panel):
    WIDTH = 100
    HEIGHT = 20

    def __init__(self, soundwindow, pos):
        wx.Panel.__init__(self, soundwindow, pos=pos, size=(self.WIDTH, self.HEIGHT))

        self.SetBackgroundColour('#969696')
        self.soundwindow = soundwindow

        self.textctrl = wx.TextCtrl(self, -1, pos=(0, 0), size=(self.WIDTH, self.HEIGHT - 1), style=wx.NO_BORDER)
        self.textctrl.Bind(wx.EVT_TEXT, self.input_keyword)

    def input_keyword(self, event):
        keyword = self.textctrl.GetValue()
        self.soundwindow.search_sounddata(keyword)

    def hide(self):
        self.Hide()
        self.textctrl.SetValue('')
        self.soundwindow.search_sounddata('')  # If searching, reset at switch timing.
