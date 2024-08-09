import math
import os
import subprocess

import wx

from source.message import Message
from source.window_path_setting import PathSettingWindow


class WrapStaticText(wx.StaticText):

    def __init__(self, parent, text, pos):
        wx.StaticText.__init__(self, parent, -1, text, pos=pos)

        self.parent = parent
        self.text = text

        width, height = self.get_nowsize()
        self.SetSize(width, height)

        self.SetBackgroundColour(wx.WHITE)
        self.font = wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "console")
        self.SetFont(self.font)
        self.Bind(wx.EVT_LEFT_DCLICK, self.doubleclick)

    def doubleclick(self, event):
        if self.text == '':
            return
        elif os.path.exists(self.text):
            path = os.path.dirname(self.text)
            path = os.path.normpath(path)
            subprocess.Popen(['explorer', path])
        else:
            PathSettingWindow(self.parent, self.text, '無効なパス：音声ファイルを指定してください。')

    def resize(self, size):

        # Subtract the offset from the parent's size to get its own size.
        width, height = self.get_nowsize()
        self.SetSize((width, height))

        # Gets the width of the entire string in pixels.
        textwidth, textheight = self.GetTextExtent(self.text)
        # If the text width is smaller than the text width, it will be displayed in one line.
        if textwidth <= width:
            self.SetLabel(self.text)
            return

        # Calculate how many lines it will take to display the current width
        rowcount = math.ceil(textwidth / width)

        '''
        Calculate how many lines it will take to display it with its current width. 
        Get a list with the px width of one character added to the length of the string. [10,20,30,....]
        '''
        dc = wx.ScreenDC()
        dc.SetFont(self.font)
        text_widths = dc.GetPartialTextExtents(self.text)

        # How to get the part of a string, line by line
        # Obtain the line of text that has been retrieved and the starting position of the next line to be retrieved.
        startindex = 0
        lines = []
        margin = 0
        for row in range(1, rowcount + 1):
            line, startindex, margin, text_widths = self.get_line(self.text, startindex, width, row, text_widths,
                                                                  margin)
            lines.append(line)

        # Each line is concatenated with a line break and displayed.
        worpping_text = ''
        for line in lines:
            worpping_text = worpping_text + line + '\n'
        worpping_text = worpping_text.rstrip('\n')
        self.SetLabel(worpping_text)
        self.Refresh()

    def get_line(self, text, startindex, linewidth, row, text_widths, margin):

        # Add the remaining margin to each px width and shift the starting px.
        if 1 < row:
            for i in range(startindex, len(text_widths)):
                text_widths[i] += margin

        # Final px width to next line
        linewidth = linewidth * row
        # Check the list where the px width of the string is added up until it exceeds the line width
        worpindex = startindex
        for w in text_widths[startindex:]:
            if w < linewidth:
                worpindex = worpindex + 1
            else:
                break;

        if worpindex < len(text_widths):
            margin = linewidth - text_widths[worpindex - 1]
        else:
            margin = 0

        return text[startindex:worpindex], worpindex, margin, text_widths

    def set_label(self, text):
        self.text = text
        self.resize(self.get_nowsize())

    def get_nowsize(self):
        size = self.parent.GetSize()
        width = size[0] - 250
        height = size[1] - 22
        return (width, height)

    def get_text(self):
        return self.text
