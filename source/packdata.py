import wx
import os
from source.database_helper import DatabaseHelper
from source.message import Message


class PackData(wx.Panel):
    HEIGHT = 148
    ICON_DEFAULT = './image/pack_icon_default.png'

    def __init__(self, scrolledwindow, startwindow, data, pos_):
        wx.Panel.__init__(self, scrolledwindow, pos=pos_)

        self.startwindow = startwindow
        self.startwindow.GetSize()[0]
        width = self.startwindow.GetSize()[0] - 60
        self.SetSize(width, self.HEIGHT)
        self.index = data[0]
        self.name = data[1]
        self.icon = data[2]
        self.description = data[3]
        self.header_uuid = data[4]
        self.modules_uuid = data[5]
        self.version = data[6]
        self.list_source_and_ogg = data[7]
        self.bundle = data[8]

        self.SetBackgroundColour('WHITE')
        line = wx.Panel(self, pos=(0, self.HEIGHT - 1), size=(width, 1))
        line.SetBackgroundColour('#969696')

        bmp = self.get_bitmap(self.icon)
        self.bitmap_icon = wx.StaticBitmap(self, -1, wx.Bitmap(bmp), pos=(0, 0), size=(self.HEIGHT, self.HEIGHT))

        self.button_edit = wx.BitmapButton(self, -1, wx.Bitmap('./image/button_pen.png'), pos=(self.HEIGHT + 10, 118),
                                           size=(16, 16))
        self.button_edit.SetBitmapPressed(wx.Bitmap('./image/button_pen_on.png'))
        self.button_edit.SetBitmapCurrent(wx.Bitmap('./image/button_pen_hover.png'))
        self.button_edit.SetToolTip('データ編集')
        self.button_edit.Bind(wx.EVT_BUTTON, self.click_edit)

        self.button_delete = wx.BitmapButton(self, -1, wx.Bitmap('./image/button_cancel.png'),
                                             pos=(self.HEIGHT + 40, 118), size=(16, 16))
        self.button_delete.SetBitmapPressed(wx.Bitmap('./image/button_cancel_on.png'))
        self.button_delete.SetBitmapCurrent(wx.Bitmap('./image/button_cancel_hover.png'))
        self.button_delete.SetToolTip('データ削除')
        self.button_delete.Bind(wx.EVT_BUTTON, self.click_delete)

        wx.StaticText(self, -1, 'name :', pos=(240, 12))
        wx.StaticText(self, -1, 'description :', pos=(240, 36))
        wx.StaticText(self, -1, 'header uuid :', pos=(240, 60))
        wx.StaticText(self, -1, 'modules uuid :', pos=(240, 84))
        wx.StaticText(self, -1, 'version :', pos=(240, 108))

        self.statictext_name = wx.StaticText(self, -1, self.name, pos=(330, 12))
        self.statictext_description = wx.StaticText(self, -1, self.description, pos=(330, 36))
        self.statictext_header_uuid = wx.StaticText(self, -1, self.header_uuid, pos=(330, 60))
        self.statictext_modules_uuid = wx.StaticText(self, -1, self.modules_uuid, pos=(330, 84))
        self.statictext_version = wx.StaticText(self, -1, self.version, pos=(330, 108))

    def click_edit(self, event):
        self.startwindow.destroy_soundwindow()
        data_soundwindow = self.list_source_and_ogg
        data_panelinput = [self.index, self.name, self.icon, self.description, self.header_uuid, self.modules_uuid,
                           self.version, self.bundle]
        self.startwindow.show_soundwindow(data_soundwindow, data_panelinput)

    def click_delete(self, event):
        if Message().yes_no(self, 'データを削除しますか？'):
            DatabaseHelper().delete_record(self.index)
            self.startwindow.updatelist()

    def get_bitmap(self, icon):
        if os.path.exists(icon):
            return icon
        else:
            return self.ICON_DEFAULT
