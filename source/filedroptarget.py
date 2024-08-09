import wx


class FileDropTarget(wx.FileDropTarget):

    def __init__(self, sounddata, statictext):
        wx.FileDropTarget.__init__(self)
        self.sounddata = sounddata
        self.statictext = statictext

    def OnDropFiles(self, x, y, pathlist):

        # Multiple path specification ---------------------------------------------------------

        if 1 < len(pathlist):
            for resource in pathlist:
                if not self.sounddata.check_ext(resource):
                    dialog = wx.MessageDialog(self.sounddata, 'サポートされない拡張子が含まれています。', 'メッセージ',
                                              style=wx.OK)
                    dialog.ShowModal()
                    dialog.Destroy()
                    return False

            pathlist_ = sorted(pathlist)
            self.sounddata.get_parentpanel().set_sourcepathlist(pathlist_)
            return True

        # One path specification ---------------------------------------------------------

        path = pathlist[0]
        path = self.sounddata.replace_escape(path)

        if self.sounddata.check_ext(path):
            self.sounddata.set_sourcepath(path)
            return True
        else:
            dialog = wx.MessageDialog(self.sounddata, 'サポートされない拡張子です。', 'メッセージ', style=wx.OK)
            dialog.ShowModal()
            dialog.Destroy()
            return False
