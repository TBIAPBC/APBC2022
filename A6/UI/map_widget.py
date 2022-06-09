"""
Widget to show map
"""
from UI.misc_widgets import *


# class WidgetMap2(QLabel, DarkQSS):
#     def __init__(self, parent_ui, parent_widget):
#         super().__init__()
#         self.parent_ui = parent_ui
#         self.parent_widget = parent_widget
#
#         self.__setup()
#
#     def __setup(self):
#         self.setStyleSheet("QLabel:{background-color: rgb(120, 120, 120);}")
#         self.setScaledContents(True)
#
#     def display_img_round(self, round_no):
#         pixmap = QPixmap(f"./Tmp/sim_{round_no}.png")
#         self.setPixmap(pixmap)
#
#     def resizeEvent(self, event):
#         min_dim = min(self.parent_widget.width(), self.parent_widget.height())
#         print(min_dim, self.parent_widget.width(), self.parent_widget.height())
#
#         rect = self.label_img.geometry()
#         x, y = self.parent_widget.geometry().x(), self.parent_widget.geometry().y()
#         print(self.rect())
#
#         rect.setHeight(min_dim)
#         rect.setWidth(min_dim)
#         rect.setX(x)
#         rect.setY(y)
#         self.setGeometry(rect)
#         self.label_img.setGeometry(rect)
#         print(rect, self.label_img.geometry())
#         event.accept()


class WidgetMap(QWidget, DarkQSS):
    def __init__(self, parent_ui, parent_widget):
        super().__init__()
        self.parent_ui = parent_ui
        self.parent_widget = parent_widget

        self.__setup()

    def __setup(self):
        # main layout
        self.lay_main = QVBoxLayout()
        self.lay_main.setSpacing(0)
        self.lay_main.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.lay_main)

        # display label
        self.label_img = QLabel()
        self.label_img.setScaledContents(True)
        self.lay_main.addWidget(self.label_img, 0, Qt.AlignCenter)

        self.setStyleSheet("QWidget:{background-color: rgb(100, 100, 100);}")

    def display_img_round(self, round_no):
        pixmap = QPixmap(f"./Tmp/sim_{round_no}.png")
        self.label_img.setPixmap(pixmap)

    def resizeEvent(self, event):
        min_dim = min(self.parent_widget.width(), self.parent_widget.height())

        self.resize(min_dim, min_dim)
        self.label_img.resize(min_dim, min_dim)
        self.parent_widget.resize(min_dim, min_dim)
        self.label_img.move(0, 0)
