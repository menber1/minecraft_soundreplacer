import wx
from source.sounddata import SoundData


class PanelSoundData(wx.Panel):
    HEIGHT_SOUNDDATA = 72
    WIDTH_OFFSET = 27
    HEIGHT_OFFSET = 92

    def __init__(self, soundwindow, path_oggfiles):
        wx.Panel.__init__(self, soundwindow, pos=(10, 45))

        self.soundwindow = soundwindow
        self.list_sounddata = []
        self.scrolledwindow = wx.ScrolledWindow(self, -1, style=wx.HSCROLL | wx.VERTICAL, pos=(0, 0))
        self.resize()
        i = 0
        for path_ogg in path_oggfiles:
            pos_sounddata = (0, self.HEIGHT_SOUNDDATA * i)
            sounddata = SoundData(self.scrolledwindow, self, path_ogg, pos_sounddata)
            self.list_sounddata.append(sounddata)
            i = i + 1

        count = len(self.list_sounddata)
        totalheight = self.HEIGHT_SOUNDDATA * count
        self.scrolledwindow.SetScrollbars(0, self.HEIGHT_SOUNDDATA, 0, int(totalheight / self.HEIGHT_SOUNDDATA))

    def get_newsourcelist(self):
        new_sourcelist = []
        for sounddata in self.list_sounddata:
            source, ogg = sounddata.get_source_and_ogg()
            if source != '':
                new_sourcelist.append([source, ogg])
        return new_sourcelist

    def get_sounddatalist(self):
        return self.list_sounddata

    # Bulk path specification by D&D
    def set_sourcepathlist(self, pathlist):
        for path, sounddata in zip(pathlist, self.list_sounddata):
            sounddata.set_sourcepath(path)

    def resize(self):

        size = self.soundwindow.GetSize()
        width = size[0] - self.WIDTH_OFFSET
        height = size[1] - self.HEIGHT_OFFSET
        self.SetSize((width, height))
        self.scrolledwindow.SetSize((width, height))

        # TextCtrl.Get_NumberOfLines()を取得前にTextCtrlの描画を終わらせておかないと、
        # 変化前の値を取得してしまう問題に対処
        wx.CallAfter(self.callafter_sounddatalist_resize)

    def callafter_sounddatalist_resize(self):
        for sounddata in self.list_sounddata:
            sounddata.resize()
