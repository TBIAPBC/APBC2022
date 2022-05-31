"""
Widget to show map
"""
from UI.misc_widgets import *


class WidgetMap(QWidget, DarkQSS):
    def __init__(self, parent_ui):
        super().__init__()
        self.parent_ui = parent_ui

        self.__setup()

    def __setup(self):
        # main layout
        self.lay_main = QVBoxLayout()
        self.lay_main.setSpacing(0)
        self.lay_main.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.lay_main)

        # display label
        self.label_img = QLabel()
        self.lay_main.addWidget(self.label_img, 1, Qt.AlignCenter)

    def display_img_round(self, round_no):
        pixmap = QPixmap(f"./Tmp/sim_{round_no}.png")
        self.label_img.setPixmap(pixmap)

