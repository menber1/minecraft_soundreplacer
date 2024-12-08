import os
import wx
from source.config_manager import ConfigManager

from source.panel.panel_creative import PanelCreative
from source.panel.panel_end import PanelEnd
from source.panel.panel_game import PanelGame
from source.panel.panel_input import PanelInput
from source.panel.panel_menu import PanelMenu
from source.panel.panel_nether import PanelNether
from source.panel.panel_note import PanelNote
from source.panel.panel_bgm import PanelBGM
from source.panel.panel_records import PanelRecords
from source.panel.panel_se import PanelSE
from source.panel.panel_water import PanelWater
from source.searchbar import SearchBar


class SoundWindow(wx.Frame):

    def __init__(self, startwindow, newsourcelist=None, data_for_panelinput=None):
        wx.Frame.__init__(self, startwindow, -1)

        self.SetBackgroundColour(wx.WHITE)
        self.SetSize(ConfigManager().get_size_soundwindow())
        self.SetMinSize((1000, 525))
        self.SetMaxSize((1936, 1056))
        icon = wx.Icon('./image/icon_frame.ico')
        self.SetIcon(icon)
        if data_for_panelinput is None:
            windowtitle = 'new resourcepack'
        else:
            windowtitle = data_for_panelinput[1]
        self.SetTitle('SoundReplacer :  ' + windowtitle)
        x, y = startwindow.GetPosition()
        self.SetPosition((x + 50, y + 50))
        self.startwindow = startwindow

        element_array = (
        'records', 'menu', 'game', 'creative', 'end', 'nether', 'water', 'note', 'bgm ( original )', 'se ( original )')
        self.combobox = wx.ComboBox(self, wx.ID_ANY, choices=element_array, style=wx.CB_DROPDOWN | wx.CB_READONLY,
                                    pos=(25, 10), size=(110, 25))
        self.combobox.Select(0)
        self.combobox.Bind(wx.EVT_COMBOBOX, self.select_combobox)

        self.button_next = wx.BitmapButton(self, -1, wx.Bitmap('./image/button_export.png'), pos=(165, 12),
                                           size=(16, 16))
        self.button_next.SetBitmapPressed(wx.Bitmap('./image/button_export_on.png'))
        self.button_next.SetBitmapCurrent(wx.Bitmap('./image/button_export_hover.png'))
        self.button_next.SetToolTip('エクスポート画面へ')
        self.button_next.Bind(wx.EVT_BUTTON, self.click_next)

        self.searchbar = SearchBar(self, pos=(850, 13))

        self.panel_records = PanelRecords(self)
        self.panel_menu = PanelMenu(self)
        self.panel_game = PanelGame(self)
        self.panel_creative = PanelCreative(self)
        self.panel_end = PanelEnd(self)
        self.panel_nether = PanelNether(self)
        self.panel_water = PanelWater(self)
        self.panel_note = PanelNote(self)
        self.panel_bgm = PanelBGM(self)
        self.panel_se = PanelSE(self)
        self.panel_input = PanelInput(self, data_for_panelinput)

        self.switch_panel(self.panel_records)

        if newsourcelist != None:
            self.newsourcelist_in_panel_sounddata(newsourcelist)

        self.Bind(wx.EVT_CLOSE, self.close_frame)
        self.Bind(wx.EVT_SIZE, self.resize_frame)

    def close_frame(self, event):
        self.startwindow.destroy_soundwindow()

    def resize_frame(self, event):
        self.panel_records.resize()
        self.panel_menu.resize()
        self.panel_game.resize()
        self.panel_creative.resize()
        self.panel_end.resize()
        self.panel_nether.resize()
        self.panel_water.resize()
        self.panel_note.resize()
        self.panel_bgm.resize()
        self.panel_se.resize()

    def select_combobox(self, event):

        self.button_next.Show()
        name = self.combobox.GetStringSelection()

        if name == 'records':
            self.switch_panel(self.panel_records)
        elif name == 'menu':
            self.switch_panel(self.panel_menu)
        elif name == 'game':
            self.switch_panel(self.panel_game)
        elif name == 'creative':
            self.switch_panel(self.panel_creative)
        elif name == 'end':
            self.switch_panel(self.panel_end)
        elif name == 'nether':
            self.switch_panel(self.panel_nether)
        elif name == 'water':
            self.switch_panel(self.panel_water)
        elif name == 'note':
            self.switch_panel(self.panel_note)
        elif name == 'bgm ( original )':
            self.switch_panel(self.panel_bgm)
        elif name == 'se ( original )':
            self.switch_panel(self.panel_se)

    def click_next(self, event):
        self.button_next.Hide()
        self.switch_panel(self.panel_input)

    def switch_panel(self, panel):

        self.searchbar.hide()
        self.panel_menu.Hide()
        self.panel_end.Hide()
        self.panel_game.Hide()
        self.panel_water.Hide()
        self.panel_nether.Hide()
        self.panel_creative.Hide()
        self.panel_records.Hide()
        self.panel_note.Hide()
        self.panel_input.Hide()
        self.panel_bgm.Hide()
        self.panel_se.Hide()
        panel.Show()

        if isinstance(panel, PanelBGM) or isinstance(panel, PanelSE):
            self.searchbar.Show()

        self.Update()

    def get_size(self):
        size = ConfigManager().get_size_soundwindow()
        return size[0], size[1]

    def get_newsourcelist(self):
        all = []
        all.extend(self.panel_records.get_newsourcelist())
        all.extend(self.panel_menu.get_newsourcelist())
        all.extend(self.panel_game.get_newsourcelist())
        all.extend(self.panel_creative.get_newsourcelist())
        all.extend(self.panel_end.get_newsourcelist())
        all.extend(self.panel_nether.get_newsourcelist())
        all.extend(self.panel_water.get_newsourcelist())
        all.extend(self.panel_note.get_newsourcelist())
        all.extend(self.panel_bgm.get_newsourcelist())
        all.extend(self.panel_se.get_newsourcelist())
        return all

    def newsourcelist_in_panel_sounddata(self, list_source_and_ogg):
        '''
        Rewritten to sort only bgm and se.
        The variable list_source_and_ogg contains all the data for each panel,
        so it is split into three lists: bgm, se, others. Sorting is done only for bgm and se.
        '''
        list_source_and_ogg_bgm = []
        list_source_and_ogg_se = []
        list_source_and_ogg_others = []

        for source, ogg in list_source_and_ogg:
            panel_sounddata = self._get_panelsounddata(ogg)

            if self.panel_bgm is panel_sounddata:
                list_source_and_ogg_bgm.append([source, ogg])
            elif self.panel_se is panel_sounddata:
                list_source_and_ogg_se.append([source, ogg])
            else:
                list_source_and_ogg_others.append([source, ogg])

        if list_source_and_ogg_bgm != []:
            _list_source_and_ogg_bgm = sorted(list_source_and_ogg_bgm, key=lambda x: x[1])
            for source, ogg in _list_source_and_ogg_bgm:
                panel_sounddata = self._get_panelsounddata(ogg)
                panel_sounddata.create_sounddata(ogg, source)

        if list_source_and_ogg_se != []:
            _list_source_and_ogg_se = sorted(list_source_and_ogg_se, key=lambda x: x[1])
            for source, ogg in _list_source_and_ogg_se:
                panel_sounddata = self._get_panelsounddata(ogg)
                panel_sounddata.create_sounddata(ogg, source)

        if list_source_and_ogg_others != []:
            for source, ogg in list_source_and_ogg_others:
                panel_sounddata = self._get_panelsounddata(ogg)
                list_sounddata = panel_sounddata.get_sounddatalist()
                for sounddata in list_sounddata:
                    if sounddata.get_oggfilepath() == ogg:
                        sounddata.set_sourcepath(source)

    def _get_panelsounddata(self, path_ogg):

        category, index = os.path.splitext(path_ogg)

        if category == 'bgm' or category == 'se':  # bgm, seはカテゴリーをoggの代用
            oggdir = category
        else:
            oggdir = os.path.basename(os.path.dirname(path_ogg))

        if oggdir == 'menu':
            return self.panel_menu
        elif oggdir == 'game':
            return self.panel_game
        elif oggdir == 'records':
            return self.panel_records
        elif oggdir == 'creative':
            return self.panel_creative
        elif oggdir == 'end':
            return self.panel_end
        elif oggdir == 'nether':
            return self.panel_nether
        elif oggdir == 'water':
            return self.panel_water
        elif oggdir == 'note':
            return self.panel_note
        elif oggdir == 'bgm':
            return self.panel_bgm
        elif oggdir == 'se':
            return self.panel_se
        else:
            return False

    def get_startwindow(self):
        return self.startwindow

    def get_inputpanel(self):
        return self.panel_input

    def search_sounddata(self, keyword):
        if self.panel_bgm.IsShown():
            self.panel_bgm.search(keyword)
        elif self.panel_se.IsShown():
            self.panel_se.search(keyword)
