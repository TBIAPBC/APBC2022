"""
UI for main screen
"""
import sys

from UI.misc_widgets import *
from UI.settings_widget import WidgetSettings
from UI.game_widget import WidgetGame
from UI.scoreboard_widget import WidgetScoreboard
from UI.map_widget import WidgetMap
from UI.finish_widget import WidgetFinish
from UI.tools_widget import WidgetTools


class MainUI(DarkQSS):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setup_ui()

        # stuff
        self.is_maximized = False

    def setup_ui(self):
        self.parent.resize(900, 600)
        self.parent.setMinimumSize(QSize(900, 600))

        ### central widget
        self.centralwidget = QWidget(self.parent)
        self.lay_central_grid = QGridLayout(self.centralwidget)
        self.lay_central_grid.setContentsMargins(5, 5, 5, 5)
        self.lay_central_grid.setSpacing(0)

        ### resize widget
        self.resize_TR = QSizeGrip(self.centralwidget)
        self.resize_TR.setMinimumSize(QSize(5, 5))
        self.resize_TR.setMaximumSize(QSize(5, 5))
        self.resize_TR.setCursor(QCursor(Qt.SizeBDiagCursor))
        self.resize_TR.setStyleSheet(self.disableStyleSheet)

        self.resize_R = SizeGripRight(self.parent)
        self.resize_R.setMinimumSize(QSize(5, 0))
        self.resize_R.setMaximumSize(QSize(5, 16777215))
        self.resize_R.setCursor(QCursor(Qt.SizeHorCursor))
        self.resize_R.setStyleSheet(self.disableStyleSheet)

        self.resize_TL = QSizeGrip(self.centralwidget)
        self.resize_TL.setMinimumSize(QSize(5, 5))
        self.resize_TL.setMaximumSize(QSize(5, 5))
        self.resize_TL.setCursor(QCursor(Qt.SizeFDiagCursor))
        self.resize_TL.setStyleSheet(self.disableStyleSheet)

        self.resize_L = SizeGripLeft(self.parent)
        self.resize_L.setMinimumSize(QSize(5, 0))
        self.resize_L.setMaximumSize(QSize(5, 16777215))
        self.resize_L.setCursor(QCursor(Qt.SizeHorCursor))
        self.resize_L.setStyleSheet(self.disableStyleSheet)

        self.resize_T = SizeGripTop(self.parent)
        self.resize_T.setMinimumSize(QSize(0, 5))
        self.resize_T.setMaximumSize(QSize(16777215, 5))
        self.resize_T.setCursor(QCursor(Qt.SizeVerCursor))
        self.resize_T.setStyleSheet(self.disableStyleSheet)

        self.resize_B = SizeGripBottom(self.parent)
        self.resize_B.setMinimumSize(QSize(0, 5))
        self.resize_B.setMaximumSize(QSize(16777215, 5))
        self.resize_B.setCursor(QCursor(Qt.SizeVerCursor))
        self.resize_B.setStyleSheet(self.disableStyleSheet)

        self.resize_BR = QSizeGrip(self.centralwidget)
        self.resize_BR.setMinimumSize(QSize(5, 5))
        self.resize_BR.setMaximumSize(QSize(5, 5))
        self.resize_BR.setCursor(QCursor(Qt.SizeFDiagCursor))
        self.resize_BR.setFocusPolicy(Qt.TabFocus)
        self.resize_BR.setStyleSheet(self.disableStyleSheet)

        self.resize_BL = QSizeGrip(self.centralwidget)
        self.resize_BL.setMinimumSize(QSize(5, 5))
        self.resize_BL.setMaximumSize(QSize(5, 5))
        self.resize_BL.setCursor(QCursor(Qt.SizeBDiagCursor))
        self.resize_BL.setStyleSheet(self.disableStyleSheet)

        # add to layout
        self.lay_central_grid.addWidget(self.resize_TR, 0, 4, 1, 1)
        self.lay_central_grid.addWidget(self.resize_R, 1, 4, 1, 1)
        self.lay_central_grid.addWidget(self.resize_TL, 0, 1, 1, 1)
        self.lay_central_grid.addWidget(self.resize_L, 1, 1, 1, 1)
        self.lay_central_grid.addWidget(self.resize_T, 0, 3, 1, 1)
        self.lay_central_grid.addWidget(self.resize_B, 2, 3, 1, 1)
        self.lay_central_grid.addWidget(self.resize_BR, 2, 4, 1, 1)
        self.lay_central_grid.addWidget(self.resize_BL, 2, 1, 1, 1)

        ### shadow frame
        self.frame_shadow = QFrame(self.centralwidget)
        self.frame_shadow.setStyleSheet(self.mainUIStyleSheet)
        self.frame_shadow.setFrameShape(QFrame.StyledPanel)
        self.frame_shadow.setFrameShadow(QFrame.Raised)
        self.lay_shadow_frame = QVBoxLayout(self.frame_shadow)
        self.lay_shadow_frame.setContentsMargins(0, 0, 0, 0)
        self.lay_shadow_frame.setSpacing(0)

        ### main widget
        self.widget_main = QWidget(self.frame_shadow)
        self.widget_main.setStyleSheet(self.mainUIStyleSheet)
        self.lay_main = QVBoxLayout(self.widget_main)
        self.lay_main.setContentsMargins(0, 0, 0, 0)
        self.lay_main.setSpacing(0)

        ### title bar
        # layout
        self.title_bar = QWidget(self.widget_main)
        self.title_bar.setMinimumSize(QSize(0, 25))
        self.title_bar.setMaximumSize(QSize(16777215, 25))
        self.lay_title_bar = QHBoxLayout(self.title_bar)
        self.lay_title_bar.setContentsMargins(0, 0, 0, 0)
        self.lay_title_bar.setSpacing(0)
        self.lay_main.addWidget(self.title_bar)
        # icon
        self.label_title_bar_icon = QLabel(self.title_bar)
        self.label_title_bar_icon.setMinimumSize(QSize(25, 25))
        self.label_title_bar_icon.setMaximumSize(QSize(25, 25))
        self.label_title_bar_icon.setAlignment(Qt.AlignCenter)
        self.label_title_bar_icon.setText("#")
        self.label_title_bar_icon.setFont(self.font_0)
        # title
        self.lable_title_bar_title = QLabel(self.title_bar)
        self.lable_title_bar_title.setFont(self.font_0)
        self.lable_title_bar_title.setText("Robot Race")
        # spacer
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        # button minimize
        self.button_title_bar_minimize = QPushButton(self.title_bar)
        self.button_title_bar_minimize.setMinimumSize(QSize(50, 25))
        self.button_title_bar_minimize.setMaximumSize(QSize(50, 25))
        self.button_title_bar_minimize.setFont(self.font_0)
        self.button_title_bar_minimize.setText("-")
        self.button_title_bar_minimize.setStyleSheet(self.WBminimizeStyleSheet)
        # button maximize
        self.button_title_bar_maximize = QPushButton(self.title_bar)
        self.button_title_bar_maximize.setMinimumSize(QSize(50, 25))
        self.button_title_bar_maximize.setMaximumSize(QSize(50, 25))
        self.button_title_bar_maximize.setText("o")
        self.button_title_bar_maximize.setFont(self.font_0)
        self.button_title_bar_maximize.setStyleSheet(self.WBmaximizeStyleSheet)
        # button exit
        self.button_title_bar_exit = QPushButton(self.title_bar)
        self.button_title_bar_exit.setMinimumSize(QSize(50, 25))
        self.button_title_bar_exit.setMaximumSize(QSize(50, 25))
        self.button_title_bar_exit.setText("x")
        self.button_title_bar_exit.setFont(self.font_0)
        self.button_title_bar_exit.setStyleSheet(self.WBexitStyleSheet)
        # add to layout
        self.lay_title_bar.addWidget(self.label_title_bar_icon)
        self.lay_title_bar.addWidget(self.lable_title_bar_title)
        self.lay_title_bar.addItem(spacerItem)
        self.lay_title_bar.addWidget(self.button_title_bar_minimize)
        self.lay_title_bar.addWidget(self.button_title_bar_maximize)
        self.lay_title_bar.addWidget(self.button_title_bar_exit)

        ### content widget
        # setup
        self.content_widget = QWidget(self.widget_main)
        self.lay_main.addWidget(self.content_widget)
        self.lay_shadow_frame.addWidget(self.widget_main)
        self.lay_central_grid.addWidget(self.frame_shadow, 1, 3, 1, 1)
        # create layout
        self.lay_content = QVBoxLayout()
        self.lay_content.setContentsMargins(0, 0, 0, 0)
        self.lay_content.setSpacing(0)
        self.content_widget.setLayout(self.lay_content)

        self.content_widget.setStyleSheet(self.mainStyleSheet)

        ##### content widgets #####
        ### settings
        self.widget_settings = WidgetSettings(self)
        self.lay_content.addWidget(self.widget_settings)

        ### game
        self.widget_game = WidgetGame(self)
        self.lay_content.addWidget(self.widget_game)
        self.widget_game.hide()

        ### Map
        self.map_widget = WidgetMap(self, self.widget_game.widget_left)
        self.widget_game.lay_left.addWidget(self.map_widget)
        self.map_widget.hide()

        ### scoreboard
        self.widget_scoreboard = WidgetScoreboard(self, player_count=4)
        self.widget_game.lay_right.addWidget(self.widget_scoreboard)

        # spacer
        self.spacer_right = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.widget_game.lay_right.addItem(self.spacer_right)

        ### tools
        self.tools = WidgetTools()
        self.widget_game.lay_right.addWidget(self.tools)

        ### finish screen widget
        self.widget_finish = WidgetFinish(self)
        self.widget_game.lay_left.addWidget(self.widget_finish)
        #self.widget_finish.hide()

        ##### window-ui / signal-slot connections #####
        self.parent.setCentralWidget(self.centralwidget)
        QMetaObject.connectSlotsByName(self.parent)

        ####################################################################################
        # connect buttons
        ####################################################################################
        # title bar
        self.button_title_bar_minimize.clicked.connect(self.btn_minimize)
        self.button_title_bar_exit.clicked.connect(self.btn_exit)
        self.button_title_bar_maximize.clicked.connect(self.btn_maximize)

        # widgets
        self.widget_settings.button_play.clicked.connect(self.__btn_wdgt_settings_play)
        self.tools.button_play.clicked.connect(self.__btn_tools_play)
        self.tools.button_break.clicked.connect(self.__btn_tools_break)
        self.tools.button_reset.clicked.connect(self.__btn_tools_reset)
        self.widget_finish.button_again.clicked.connect(self.__btn_wdgt_finish_play_again)
        self.widget_finish.button_back.clicked.connect(self.__btn_wdgt_finish_change_settings)

        #####################################################################################
        # main game loop
        #####################################################################################
        ### start...

        """TEST"""
        round_ = 1
        score_list = [
            ["GodBot", 120030],
            ["DeepBot", 14842],
            ["SmartBot", 9387],
            ["DumBot", 1]
        ]
        self.widget_scoreboard.update_scoreboard(score_list, round_)
        self.map_widget.display_img_round(round_)

    ### button functions
    def btn_exit(self):
        sys.exit(self.parent.app.exec_())

    def btn_maximize(self):
        if self.is_maximized is False:
            self.parent.showMaximized()
            self.is_maximized = True
            self.__hide_resize()
        else:
            self.parent.showNormal()
            self.is_maximized = False
            self.__show_resize()

    def btn_minimize(self):
        self.parent.showMinimized()

    def __btn_tools_play(self):
        self.tools.change_play_pause()

    def __btn_tools_break(self):
        print("-----------------------\nBREAK\n-----------------------")

    def __btn_tools_reset(self):
        print("-----------------------\nRESET\n-----------------------")

    def __show_resize(self):
        self.lay_central_grid.setContentsMargins(5, 5, 5, 5)

        self.resize_BR.show()
        self.resize_B.show()
        self.resize_L.show()
        self.resize_R.show()
        self.resize_T.show()
        self.resize_BL.show()
        self.resize_TL.show()
        self.resize_TR.show()

    def __hide_resize(self):
        self.lay_central_grid.setContentsMargins(0, 0, 0, 0)

        self.resize_BR.hide()
        self.resize_B.hide()
        self.resize_L.hide()
        self.resize_R.hide()
        self.resize_T.hide()
        self.resize_BL.hide()
        self.resize_TL.hide()
        self.resize_TR.hide()

    def __btn_wdgt_settings_play(self):
        if self.widget_settings.validator() is False:
            return
        self.settings = self.widget_settings.get_settings()

        self.widget_settings.hide()
        self.widget_game.show()

    def __btn_wdgt_finish_play_again(self):
        print("-----------------------\nPLAY AGAIN\n-----------------------")

    def __btn_wdgt_finish_change_settings(self):
        print("-----------------------\nBACK TO SETTINGS\n-----------------------")

    def __block_tools(self): ...
    def __unblock_tools(self): ...