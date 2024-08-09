from source.panel.panel_bgm import PanelBGM


class PanelSE(PanelBGM):
    CATEGORY = 'se.'

    def __init__(self, soundwindow):
        super().__init__(soundwindow)
