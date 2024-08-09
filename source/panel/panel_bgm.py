import os
import wx
from source.sounddata_bgm import SoundDataBGM


class PanelBGM(wx.Panel):

    HEIGHT_SOUNDDATA = 72
    WIDTH_OFFSET = 27
    HEIGHT_OFFSET = 92
    CATEGORY = 'bgm.'

    def __init__(self, soundwindow):
        wx.Panel.__init__(self, soundwindow, pos=(10,45))

        self.SetBackgroundColour(wx.WHITE)
        self.soundwindow = soundwindow
        self.list_sounddata = []
        self.scrolledwindow = wx.ScrolledWindow(self, -1, style=wx.HSCROLL|wx.VERTICAL, pos=(0,0))
        self.resize()
        
        sounddata = SoundDataBGM(self.scrolledwindow, self, self.CATEGORY + '1', (0, 0))
        self.list_sounddata.append(sounddata)


    def create_sounddata(self, title, resourcepath):

        first_resourcepath = self.list_sounddata[0].get_sourcepath()

        if first_resourcepath == '':
            self.list_sounddata[0].Destroy()
            self.list_sounddata = []

        count = len(self.list_sounddata)
        pos_sounddata = (0, self.HEIGHT_SOUNDDATA * count)
        sounddata = SoundDataBGM(self.scrolledwindow, self, title, pos_sounddata)
        self.list_sounddata.append(sounddata)
        totalheight = self.HEIGHT_SOUNDDATA * (count + 1)
        self.scrolledwindow.SetScrollbars(0, self.HEIGHT_SOUNDDATA, 0, int(totalheight / self.HEIGHT_SOUNDDATA))
        self._switch_plusbutton()
        sounddata.set_sourcepath(resourcepath)


    def get_newsourcelist(self):
        new_sourcelist = []
        for sounddata in self.list_sounddata:
            source, title = sounddata.get_source_and_title()
            if source != '':
                new_sourcelist.append([source, title])

        return new_sourcelist

    def get_sounddatalist(self):
        return self.list_sounddata

    def set_sourcepathlist(self, pathlist):
        for path, sounddata in zip(pathlist, self.list_sounddata):
            sounddata.set_sourcepath(path)

    def add_sounddata(self):
        # code explanation : 1
        title = self.CATEGORY + str(self._get_maxindex() + 1)
        pos = (0, len(self.list_sounddata) * self.HEIGHT_SOUNDDATA)

        self.scrolledwindow.Scroll(0, 0)
        new_sounddata = SoundDataBGM(self.scrolledwindow, self, title, pos)
        self.list_sounddata.append(new_sounddata)

        totalheight = len(self.list_sounddata) * self.HEIGHT_SOUNDDATA # 追加後にもう一度全体の高さを取得
        self.scrolledwindow.SetScrollbars(0, self.HEIGHT_SOUNDDATA, 0, int(totalheight / self.HEIGHT_SOUNDDATA))
        self._switch_plusbutton()
        self.scrolledwindow.Scroll(0, self.scrolledwindow.GetVirtualSize().GetHeight())  # スクロールを末尾へ

    def delete_sounddata(self, sounddata):

        self.scrolledwindow.Scroll(0, 0)

        if len(self.list_sounddata) == 1:
            sounddata.Destroy()
            sounddata = SoundDataBGM(self.scrolledwindow, self, self.CATEGORY + '1', (0, 0))
            self.list_sounddata.clear()
            self.list_sounddata.append(sounddata)
            self.Refresh()
        else:
            for sounddata_ in self.list_sounddata:

                if sounddata_ is sounddata:
                    self.list_sounddata.remove(sounddata)
                    sounddata.Destroy()
                    break
            count = 0
            for sounddata_ in self.list_sounddata:
                sounddata_.SetPosition((0, self.HEIGHT_SOUNDDATA * count))
                count = count + 1
            totalheight = len(self.list_sounddata) * self.HEIGHT_SOUNDDATA
            self.scrolledwindow.SetScrollbars(0, self.HEIGHT_SOUNDDATA, 0, int(totalheight / self.HEIGHT_SOUNDDATA))
            self._switch_plusbutton()
            self.Refresh()

    def _get_index(self, title):
        index =  title.replace(self.CATEGORY, '')
        if self._check_int(index):
            return int(index)
        else:
            return None

    def _check_int(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def _switch_plusbutton(self):
        for sounddata in self.list_sounddata:
            sounddata.hide_addbutton()
        self.list_sounddata[-1].show_addbutton()


    def check_duplicatetitle(self, newtitle):
        for sounddata in self.list_sounddata:
            category, nowtitle = sounddata.get_title().split('.')
            if nowtitle == newtitle:
                return False
        return True

    def _get_maxindex(self):
        maxindex = 0
        for sounddata in self.list_sounddata:
            category, index = sounddata.get_title().split('.')
            if self._check_int(index):
                index_ = int(index)
                if maxindex < index_:
                    maxindex = index_
        return maxindex

    '''
    The search will search both command names and file names.
    If you start with '/', it will search only the file name.
    '/' is a symbol that cannot be used in command names or file names.
    '''
    def search(self, keyword):

        self.list_sounddata[-1].hide_addbutton() # 検索時はaddbuttonは非表示
        self.scrolledwindow.Scroll(0, 0)
        posy = 0

        if keyword == '':
            for sounddata in self.list_sounddata:
                sounddata.show()
                sounddata.SetPosition((0, posy))
                posy = posy + sounddata.HEIGHT

            self._switch_plusbutton()
            totalheight = len(self.list_sounddata) * self.HEIGHT_SOUNDDATA
            self.scrolledwindow.SetScrollbars(0, self.HEIGHT_SOUNDDATA, 0, int(totalheight / self.HEIGHT_SOUNDDATA))

        else:
            for sounddata in self.list_sounddata:
                title = sounddata.get_title()
                title = title[title.index('.') + 1:] # Title without bgm. se.

                basename = os.path.basename(sounddata.get_sourcepath())
                title_basename = title + '/' + basename 
                if keyword in title_basename:
                    sounddata.show()
                    sounddata.SetPosition((0, posy))
                    posy = posy + self.HEIGHT_SOUNDDATA
                else:
                    sounddata.hide()
                    sounddata.SetPosition((0, posy))

            self.scrolledwindow.SetScrollbars(0, self.HEIGHT_SOUNDDATA, 0, int(posy / self.HEIGHT_SOUNDDATA))

        self.Refresh()


    def resize(self):
        size = self.soundwindow.GetSize()
        width = size[0] - self.WIDTH_OFFSET
        height = size[1] - self.HEIGHT_OFFSET
        self.SetSize((width, height))
        self.scrolledwindow.SetSize((width, height))
        '''
        TextCtrl.Get_NumberOfLines()取得前にTextCtrlの描画を終わらせないと、
        変化前の値を取得してしまう問題に対処
        '''
        wx.CallAfter(self.callafter_sounddatalist_resize)

    def callafter_sounddatalist_resize(self):
        for sounddata in self.list_sounddata:
            sounddata.resize()
