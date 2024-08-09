import wx


class Message():

    def __init__(self):
        pass

    def show(self, parent, message):
        dialog = wx.MessageDialog(parent, message, 'メッセージ', style=wx.OK)
        dialog.ShowModal()
        dialog.Destroy()

    def yes_no(self, parent, message):
        dialog = wx.MessageDialog(parent, message, 'メッセージ', style=wx.YES_NO)
        ans = dialog.ShowModal()
        dialog.Destroy()
        if ans == 5104:  # YES 5103 NO 5104
            return False
        else:
            return True

    def error(self, parent, message):
        dialog = wx.MessageDialog(parent, message, 'エラー', style=wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
