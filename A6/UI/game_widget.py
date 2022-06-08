"""
Widget to display the game
"""
from UI.misc_widgets import *


class WidgetGame(QWidget, DarkQSS):
    def __init__(self, parent_ui):
        super().__init__()

        self.parent_ui = parent_ui
        self.setup_widget()

    def setup_widget(self):
        # own properties
        self.setStyleSheet(self.disableStyleSheet)

        ### main layout
        self.lay_main = QHBoxLayout()
        self.lay_main.setSpacing(0)
        self.lay_main.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.lay_main)

        ### left widget
        # widget
        self.widget_left = QWidget()

        # layout
        self.lay_left = QVBoxLayout()
        self.lay_left.setSpacing(0)
        self.lay_left.setContentsMargins(0, 0, 0, 0)
        self.widget_left.setLayout(self.lay_left)

        ### right widget
        # widget
        self.widget_right = QWidget()

        # layout
        self.lay_right = QVBoxLayout()
        self.lay_right.setSpacing(0)
        self.lay_right.setContentsMargins(0, 0, 0, 0)
        self.widget_right.setLayout(self.lay_right)

        ### add to main widget
        self.lay_main.addWidget(self.widget_left, 2)
        self.lay_main.addWidget(self.widget_right, 1)