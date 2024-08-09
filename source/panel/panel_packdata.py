import wx
from source.database_helper import DatabaseHelper
from source.packdata import PackData


class PackdataPanel(wx.Panel):
    HEIGHT_PACKDATA = 148
    WIDTH_OFFSET = 33
    HEIGHT_OFFSET = 90

    def __init__(self, startwindow):
        wx.Panel.__init__(self, startwindow, pos=(15, 48))

        self.SetBackgroundColour(wx.WHITE)
        self.startwindow = startwindow
        self.list_packdata = []
        self.scrolledwindow = wx.ScrolledWindow(self, -1, style=wx.HSCROLL | wx.VERTICAL, pos=(0, 0))
        self.update()

    def resize(self):
        size = self.startwindow.GetSize()
        width = size[0] - self.WIDTH_OFFSET
        height = size[1] - self.HEIGHT_OFFSET
        self.SetSize((width, height))
        self.scrolledwindow.SetSize((width, height))

    def update(self):
        self._remove_child_all()
        packdatas = DatabaseHelper().get_packdatalist()
        i = 0
        for data in packdatas:
            pos_packdata = (0, self.HEIGHT_PACKDATA * i)
            packdata = PackData(self.scrolledwindow, self.startwindow, data, pos_packdata)
            self.list_packdata.append(packdata)
            i = i + 1
        count = len(self.list_packdata)
        totalheight = self.HEIGHT_PACKDATA * count
        self.scrolledwindow.SetScrollbars(0, self.HEIGHT_PACKDATA, 0, int(totalheight / self.HEIGHT_PACKDATA))
        self.resize()

    def _remove_child_all(self):
        for child in self.scrolledwindow.GetChildren():
            child.Destroy()
        self.list_packdata = []
