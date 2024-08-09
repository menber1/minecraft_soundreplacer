import wx
from source.window_start import StartWindow

if __name__ == '__main__':
    app = wx.App()
    frame = StartWindow()
    frame.Show()
    app.MainLoop()
