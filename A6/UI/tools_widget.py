"""
Widget for tools
"""
from UI.misc_widgets import *


class WidgetTools(QWidget, DarkQSS):
    def __init__(self):
        super().__init__()
        self.paused = False

        self.__setup_ui()

    def __setup_ui(self):
        self.setFixedHeight(100)

        self.lay_main = QHBoxLayout()
        self.lay_main.setSpacing(0)
        self.lay_main.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.lay_main)

        self.gb_main = QGroupBox()
        self.gb_main.setTitle("Tools")
        self.gb_main.setFont(self.font_2)
        self.gb_main.setStyleSheet(self.subgroupboxStyleSheet)
        self.lay_main.addWidget(self.gb_main)

        self.lay_gb = QHBoxLayout()
        self.lay_gb.setSpacing(6)
        self.lay_gb.setContentsMargins(9, 9, 9, 9)
        self.gb_main.setLayout(self.lay_gb)

        ### buttons
        self.button_play = QPushButton()
        self.button_play.setFixedWidth(41)
        self.button_play.setFixedHeight(41)
        self.button_play.setStyleSheet(self.qss_button_pause)   # img

        self.button_break = QPushButton()
        self.button_break.setFixedWidth(41)
        self.button_break.setFixedHeight(41)
        self.button_break.setStyleSheet(self.qss_button_break)   # img

        self.button_reset = QPushButton()
        self.button_reset.setFixedWidth(41)
        self.button_reset.setFixedHeight(41)
        self.button_reset.setStyleSheet(self.qss_button_reset)   # img

        self.spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)

        # add layout
        self.lay_gb.addWidget(self.button_play)
        self.lay_gb.addWidget(self.button_break)
        self.lay_gb.addWidget(self.button_reset)
        self.lay_gb.addItem(self.spacer)

    def change_play_pause(self):
        if self.paused:
            self.button_play.setStyleSheet(self.qss_button_pause)
            self.paused = False

        else:
            self.paused = True
            self.button_play.setStyleSheet(self.qss_button_play)



