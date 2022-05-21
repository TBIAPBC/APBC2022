"""
UI for main screen
"""
import sys

from UI.misc_widgets import *
from UI.settings_widget import WidgetSettings
from UI.scoreboard_widget import WidgetScoreboard
from UI.map_widget import WidgetMap
from UI.finish_widget import WidgetFinish
from UI.tools_widget import WidgetTools


class MainUI(DarkQML):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setup_ui()

        ### save widgets in ui
        self.widget_settings = None
        self.widget_map = None
        self.widget_finish = None
        self.widget_tools = None
        self.widget_scoreboard = None

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
        self.resize_TR.setMinimumSize(QSize(4, 4))
        self.resize_TR.setMaximumSize(QSize(4, 4))
        self.resize_TR.setCursor(QCursor(Qt.SizeBDiagCursor))
        self.resize_TR.setStyleSheet(self.disableStyleSheet)

        self.resize_R = QWidget(self.centralwidget)
        self.resize_R.setMinimumSize(QSize(4, 0))
        self.resize_R.setMaximumSize(QSize(4, 16777215))
        self.resize_R.setCursor(QCursor(Qt.SizeHorCursor))
        self.resize_R.setStyleSheet(self.disableStyleSheet)

        self.resize_TL = QSizeGrip(self.centralwidget)
        self.resize_TL.setMinimumSize(QSize(4, 4))
        self.resize_TL.setMaximumSize(QSize(4, 4))
        self.resize_TL.setCursor(QCursor(Qt.SizeFDiagCursor))
        self.resize_TL.setStyleSheet(self.disableStyleSheet)

        self.resize_L = QWidget(self.centralwidget)
        self.resize_L.setMinimumSize(QSize(4, 0))
        self.resize_L.setMaximumSize(QSize(4, 16777215))
        self.resize_L.setCursor(QCursor(Qt.SizeHorCursor))
        self.resize_L.setStyleSheet(self.disableStyleSheet)

        self.resize_T = QWidget(self.centralwidget)
        self.resize_T.setMinimumSize(QSize(0, 4))
        self.resize_T.setMaximumSize(QSize(16777215, 4))
        self.resize_T.setCursor(QCursor(Qt.SizeVerCursor))
        self.resize_T.setStyleSheet(self.disableStyleSheet)

        self.resize_B = QWidget(self.centralwidget)
        self.resize_B.setMinimumSize(QSize(0, 4))
        self.resize_B.setMaximumSize(QSize(16777215, 4))
        self.resize_B.setCursor(QCursor(Qt.SizeVerCursor))
        self.resize_B.setStyleSheet(self.disableStyleSheet)

        self.resize_BR = QSizeGrip(self.centralwidget)
        self.resize_BR.setMinimumSize(QSize(4, 4))
        self.resize_BR.setMaximumSize(QSize(4, 4))
        self.resize_BR.setCursor(QCursor(Qt.SizeFDiagCursor))
        self.resize_BR.setFocusPolicy(Qt.TabFocus)
        self.resize_BR.setStyleSheet(self.disableStyleSheet)

        self.resize_BL = QSizeGrip(self.centralwidget)
        self.resize_BL.setMinimumSize(QSize(4, 4))
        self.resize_BL.setMaximumSize(QSize(4, 4))
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
        self.frame_shadow.setStyleSheet(self.disableStyleSheet)
        self.frame_shadow.setFrameShape(QFrame.StyledPanel)
        self.frame_shadow.setFrameShadow(QFrame.Raised)
        self.lay_shadow_frame = QVBoxLayout(self.frame_shadow)
        self.lay_shadow_frame.setContentsMargins(1, 1, 1, 1)
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
        self.content_widget = QWidget(self.widget_main)
        self.lay_main.addWidget(self.content_widget)
        self.lay_shadow_frame.addWidget(self.widget_main)
        self.lay_central_grid.addWidget(self.frame_shadow, 1, 3, 1, 1)

        self.parent.setCentralWidget(self.centralwidget)
        QMetaObject.connectSlotsByName(self.parent)

        ##################################
        # connect buttons
        self.button_title_bar_minimize.clicked.connect(self.btn_minimize)
        self.button_title_bar_exit.clicked.connect(self.btn_exit)
        self.button_title_bar_maximize.clicked.connect(self.btn_maximize)

    def btn_exit(self):
        sys.exit(self.parent.app.exec_())

    def btn_maximize(self):
        if self.is_maximized is False:
            self.parent.showMaximized()
            self.is_maximized = True
        else:
            self.parent.showNormal()
            self.is_maximized = False

    def btn_minimize(self):
        self.parent.showMinimized()


