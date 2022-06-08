"""
Misc Widgets to import PyQt
"""
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class DragNDropWidget(QListWidget):
    def __init__(self, endswith=None, parent=None, maxItems=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setViewMode(QListWidget.IconMode)
        self.endswith = endswith  # str, data type extension
        self.maxItems = maxItems

        self.links = []

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()

            for url in event.mimeData().urls():
                if url.isLocalFile() and url.toLocalFile() not in self.links:
                    if self.endswith is None:
                        self.links.append(url.toLocalFile())
                        self.addItem(url.toLocalFile())
                    else:
                        if str(url.toLocalFile()).endswith(self.endswith):
                            self.links.append(url.toLocalFile())
                            self.addItem(url.toLocalFile())
        else:
            event.ignore()


class AppFinishWidget(QWidget):
    # class to call after running App1Widget to get back to App Selection Screen
    def __init__(self, finish_line):
        super(AppFinishWidget, self).__init__()

        # text properties
        self.font_0 = QFont()
        self.font_0.setFamily("Segoe UI")
        self.font_0.setPointSize(70)
        self.font_0.setWeight(75)

        self.font_1 = QFont()
        self.font_1.setFamily("Segoe UI")
        self.font_1.setPointSize(20)
        self.font_1.setWeight(75)

        self.buttonStyleSheet = "QPushButton{background-color: rgb(46, 46, 46);color: rgb(230, 230, 230);" \
                                "border: 2px solid rgb(69,69,69);border-radius: 5px;}" \
                                "QPushButton:hover{background-color: rgb(67, 67, 67);color: rgb(230, 230, 230);" \
                                "border: 2px solid rgb(69,69,69);border-radius: 5px;}" \
                                "QPushButton:pressed{background-color: rgb(93, 93, 93);color: rgb(230, 230, 230);" \
                                "border: 2px solid rgb(93, 93, 93);border-radius: 5px;}"


        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(12, 12, 9, 29)
        self.mainLayout.setSpacing(5)
        self.setLayout(self.mainLayout)

        spacer1 = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.mainLayout.addItem(spacer1)

        self.label_done = QLabel()
        self.label_done.setText(finish_line)
        self.label_done.setFont(self.font_0)
        self.label_done.setWordWrap(True)
        self.mainLayout.addWidget(self.label_done, 0, Qt.AlignHCenter)

        spacer2 = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.mainLayout.addItem(spacer2)

        self.button_apps = QPushButton()
        self.button_apps.setText("Return to Apps")
        self.button_apps.setFont(self.font_1)
        self.button_apps.setStyleSheet(self.buttonStyleSheet)
        self.button_apps.setMinimumSize(QSize(240, 60))
        self.mainLayout.addWidget(self.button_apps, 0, Qt.AlignHCenter)

        spacer3 = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.mainLayout.addItem(spacer3)

        # return to main window
        self.button_apps.clicked.connect(self.return_toApps)

    def return_toApps(self):
        self.parent().parent().ui.openAppSelection()


class DragNDropItemLabelButton(QWidget):
    # widget for only one item
    def __init__(self, font, spacing=0, margins=[0, 0, 0, 0], endswith=None, labelSS="", buttonSS=""):
        super().__init__()
        self.setAcceptDrops(True)
        self.endswith = endswith  # str, data type extension
        self.item = ""

        self.font = font
        self.labelSS = labelSS
        self.buttonSS = buttonSS

        self.spacing = spacing
        self.margins = margins

        self.setupUI()

    def setupUI(self):
        # set layout
        self.layH = QHBoxLayout()
        self.layH.setSpacing(self.spacing)
        self.layH.setContentsMargins(self.margins[0], self.margins[1], self.margins[2], self.margins[3])
        self.setLayout(self.layH)

        # set label
        self.label_display = QLabel()
        self.label_display.setFont(self.font)
        self.label_display.setText("")
        self.label_display.setStyleSheet(self.labelSS)
        self.label_display.setWordWrap(True)
        self.layH.addWidget(self.label_display)

        # set button
        self.button_browse = QPushButton()
        self.button_browse.setFont(self.font)
        self.button_browse.setText(" ... ")
        self.button_browse.setMaximumWidth(50)
        self.button_browse.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_browse.setStyleSheet(self.buttonSS)
        self.layH.addWidget(self.button_browse)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()

            for url in event.mimeData().urls():
                if url.isLocalFile():
                    if self.endswith is None:
                        self.item = url.toLocalFile()
                        self.label_display.setText(url.toLocalFile())

                    elif self.endswith is not None and type(self.endswith) != str:
                        for ending in self.endswith:
                            if str(url.toLocalFile()).endswith(ending):
                                self.item = url.toLocalFile()
                                self.label_display.setText(url.toLocalFile())

                    else:
                        if str(url.toLocalFile()).endswith(self.endswith):
                            self.item = url.toLocalFile()
                            self.label_display.setText(url.toLocalFile())
        else:
            event.ignore()


class DragNDropListBrowseResetWidget(QWidget):
    def __init__(self, font, margin=[0, 0, 0, 0], spacing=0, endswith=None, SS_basic="", SS_button=""):
        super(DragNDropListBrowseResetWidget, self).__init__()
        ### app properties
        self.endswith = endswith

        ### main widget
        # layot
        self.lay_main = QHBoxLayout()
        self.lay_main.setContentsMargins(margin[0], margin[1], margin[2], margin[3])
        self.lay_main.setSpacing(spacing)
        self.setLayout(self.lay_main)

        # dnd listwidget
        self.listWidget = DragNDropWidget(endswith=endswith)
        self.listWidget.setStyleSheet(SS_basic)
        self.listWidget.setFont(font)

        # button widget
        self.button_widget = QWidget()

        # add to layout
        self.lay_main.addWidget(self.listWidget)
        self.lay_main.addWidget(self.button_widget)

        ### fill button widget
        # layout
        self.lay_button = QVBoxLayout()
        self.lay_button.setContentsMargins(0, 0, 0, 0)
        self.lay_button.setSpacing(spacing)
        self.button_widget.setLayout(self.lay_button)

        # browse button
        self.button_browse = QPushButton()
        self.button_browse.setFont(font)
        self.button_browse.setText(" ... ")
        self.button_browse.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_browse.setStyleSheet(SS_button)
        self.button_browse.setMaximumWidth(50)

        # reset button
        self.button_reset = QPushButton()
        self.button_reset.setFont(font)
        self.button_reset.setText(" Reset ")
        self.button_reset.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_reset.setStyleSheet(SS_button)
        self.button_reset.setMaximumWidth(50)

        # spacer to push buttons up when list gets bigger
        spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # add to layout
        self.lay_button.addWidget(self.button_browse)
        self.lay_button.addWidget(self.button_reset)
        self.lay_button.addItem(spacer)

        ### connect buttons
        self.button_browse.clicked.connect(self.browse)
        self.button_reset.clicked.connect(self.reset)

    def browse(self):
        file_filter = "Resource Files (*{})".format(self.endswith)
        paths = QFileDialog.getOpenFileNames(parent=self, caption="Select Files", filter=file_filter,
                                             initialFilter=file_filter)
        for path in paths[0]:
            if path not in self.listWidget.links:
                self.listWidget.links.append(path)
                self.listWidget.addItem(path)

    def reset(self):
        self.listWidget.links = []
        self.listWidget.clear()


class AntiScrollQComboBox(QComboBox):
    def __init__(self):
        super(AntiScrollQComboBox, self).__init__()

    def wheelEvent(self, event):
        event.ignore()


class SizeGripRight(QWidget):
    def __init__(self, window):
        super(SizeGripRight, self).__init__()

        self.main_window = window
        self.resizing = False
        self.init_geo = self.main_window.geometry()
        self.point_init = None

    def mousePressEvent(self, event):
        if not self.resizing:
            self.resizing = True
            self.point_init = event.globalPos()
            self.init_geo = self.main_window.geometry()

    def mouseReleaseEvent(self, event):
        if not self.resizing:
            return
        self.resizing = False

    def mouseMoveEvent(self, event):
        if not self.resizing:
            return

        if self.main_window.minimumWidth() == self.main_window.geometry().width():
            if self.main_window.geometry().x() + self.main_window.width() > event.globalPos().x():
                return

        # resize
        current_pos = event.globalPos()
        distance = current_pos.x() - self.point_init.x()
        self.main_window.resize(self.main_window.width() + distance, self.main_window.height())

        # init new reference position
        self.point_init = event.globalPos()


class SizeGripBottom(QWidget):
    def __init__(self, window):
        super(SizeGripBottom, self).__init__()

        self.main_window = window
        self.resizing = False
        self.point_init = QPoint(0, 0)
        self.init_geo = self.main_window.geometry()

    def mousePressEvent(self, event):
        if not self.resizing:
            self.resizing = True
            self.point_init = event.globalPos()
            self.init_geo = self.main_window.geometry()
        else:
            self.point_init = QPoint(0, 0)

    def mouseReleaseEvent(self, event):
        if not self.resizing:
            return
        self.resizing = False

    def mouseMoveEvent(self, event):
        if not self.resizing:
            return

        if self.main_window.minimumHeight() == self.main_window.geometry().height():
            if self.main_window.geometry().y() + self.main_window.height() > event.globalPos().y():
                return

        # resize
        current_pos = event.globalPos()
        distance = current_pos.y() - self.point_init.y()
        self.main_window.resize(self.main_window.width(), self.main_window.height() + distance)

        # init new reference position
        self.point_init = event.globalPos()


class SizeGripTop(QWidget):
    def __init__(self, window):
        super(SizeGripTop, self).__init__()

        self.main_window = window
        self.resizing = False
        self.point_init = None
        self.init_geo = self.main_window.geometry()

    def mousePressEvent(self, event):
        if not self.resizing:
            self.resizing = True
            self.point_init = event.globalPos()
            self.init_geo = self.main_window.geometry()

    def mouseReleaseEvent(self, event):
        if not self.resizing:
            return
        self.resizing = False

    def mouseMoveEvent(self, event):
        if not self.resizing:
            return

        if self.main_window.minimumHeight() == self.main_window.geometry().height():
            if self.main_window.geometry().y() < event.globalPos().y():
                return

        # resize
        current_pos = event.globalPos()
        distance = current_pos.y() - self.point_init.y()
        self.main_window.setGeometry(self.main_window.geometry().adjusted(0, distance, 0, 0))

        # init new reference position
        self.point_init = event.globalPos()


class SizeGripLeft(QWidget):
    def __init__(self, window):
        super(SizeGripLeft, self).__init__()

        self.main_window = window
        self.resizing = False
        self.point_init = None
        self.init_geo = self.main_window.geometry()

    def mousePressEvent(self, event):
        if not self.resizing:
            self.resizing = True
            self.point_init = event.globalPos()
            self.init_geo = self.main_window.geometry()

    def mouseReleaseEvent(self, event):
        if not self.resizing:
            return
        self.resizing = False

    def mouseMoveEvent(self, event):
        if not self.resizing:
            return

        if self.main_window.minimumWidth() == self.main_window.geometry().width():
            if self.main_window.geometry().x() < event.globalPos().x():
                return

        # resize
        current_pos = event.globalPos()
        distance = current_pos.x() - self.point_init.x()
        self.main_window.setGeometry(self.main_window.geometry().adjusted(distance, 0, 0, 0))

        # init new reference position
        self.point_init = event.globalPos()


class DarkQSS:
    def __init__(self):
        ####################################################################
        # font
        ####################################################################
        # normal text
        self.font_0 = QFont()
        self.font_0.setFamily("Segoe UI")
        self.font_0.setPointSize(12)
        self.font_0.setWeight(75)
        self.font_0.setBold(False)
        # craft button
        self.font_1 = QFont()
        self.font_1.setFamily("Segoe UI")
        self.font_1.setPointSize(18)
        self.font_1.setBold(True)
        self.font_1.setWeight(75)
        # subtitles
        self.font_2 = QFont()
        self.font_2.setFamily("Segoe UI")
        self.font_2.setPointSize(13)
        self.font_2.setWeight(75)
        self.font_2.setBold(False)
        # titles
        self.font_3 = QFont()
        self.font_3.setFamily("Segoe UI")
        self.font_3.setPointSize(16)
        self.font_3.setBold(True)
        # big title
        self.font_4 = QFont()
        self.font_4.setFamily("Segoe UI")
        self.font_4.setPointSize(60)
        self.font_4.setBold(True)

        ####################################################################
        # style sheets
        ####################################################################
        self.windowbarStyleSheet = "QWidget{background-color: black;}"
        self.mainUIStyleSheet = "QWidget{background-color: rgb(22, 22, 22);color: rgb(230, 230, 230);" \
                                "border: 0px solid rgb(230,230,230);}"
        self.start_screen_StyleSheet = "QWidget{background-color: rgb(22, 22, 22);color: rgb(230, 230, 230);" \
                                       "border-radius: 16px;}"

        self.hoverFrameStyleSheet = "QFrame{color: rgb(230, 230, 230);}" \
                                    "QFrame:hover{background-color: rgb(39, 39, 39);color: rgb(230, 230, 230);" \
                                    "border: 1px solid rgb(230,230,230); border-radius: 0px;}"

        self.selectWidgetStyleSheet = "QWidget{background-color: rgb(22, 22, 22);; border-radius: 0px;}"

        self.buttonStyleSheet = "QPushButton{background-color: rgb(46, 46, 46);color: rgb(230, 230, 230);" \
                                "border: 2px solid rgb(69,69,69);border-radius: 2px;}" \
                                "QPushButton:hover{background-color: rgb(187, 134, 252);color: rgb(0, 0, 0);" \
                                "border: 1px solid rgb(22, 22, 22);border-radius: 2px;}" \
                                "QPushButton:pressed{background-color: rgb(211, 175, 255);color: rgb(0, 0, 0);" \
                                "border: 2px solid rgb(22, 22, 22);border-radius: 2px;}"

        self.mainStyleSheet = "QWidget{background-color: rgb(31, 31, 32);color: rgb(230, 230, 230); " \
                              "border-radius: 0px;}"

        self.basicWidgetStyleSheet = "QWidget{background-color: rgb(39, 39, 39);color: rgb(230, 230, 230);" \
                                     "border: 2px solid rgb(69,69,69); border-radius: 0px;}" \
                                     "QWidget:hover{background-color: rgb(54, 54, 54);color: rgb(230, 230, 230);" \
                                     "border: 2px solid rgb(76,76,76); border-radius: 0px;}"

        self.basicWidgetStyleSheetNoHover = "QWidget{background-color: rgb(39, 39, 39);color: rgb(230, 230, 230);" \
                                            "border: 2px solid rgb(69,69,69); border-radius: 0px;}"

        self.disableStyleSheet = "QWidget{background-color: rgba(0, 0, 0, 0);border: 2px solid rgba(0, 0, 0, 0); " \
                                 "border-radius: 0px;}"

        self.craftStyleSheet = "QPushButton{background-color: rgb(46, 46, 46);" \
                               "color: rgb(187, 134, 252);border: 2px solid rgb(69,69,69);border-radius: 5px;}" \
                               "QPushButton:hover{background-color: rgb(187, 134, 252);color: rgb(0, 0, 0);" \
                               "border: 2px solid rgb(187, 134, 252);border-radius: 5px;}" \
                               "QPushButton:pressed{background-color: rgb(211, 175, 255);color: rgb(0, 0, 0);" \
                               "border: 2px solid rgb(211, 175, 255);border-radius: 5px;}"

        self.groupboxStyleSheet = "QGroupBox {border: 1px solid silver;border-radius: " \
                                  "2px;margin-top: 16px; border-radius: 0px;}" \
                                  "QGroupBox::title {subcontrol-origin: margin;left: 7px;padding: 0px 5px 0px 5px;}"

        self.subgroupboxStyleSheet = "QGroupBox {border-top: 1px solid rgb(145, 145, 145);" \
                                     "border-right: 0px solid silver;" \
                                     "border-left: 0px solid silver;border-bottom: 0px solid silver;" \
                                     "border-radius: 0px;margin-top: 16px;}" \
                                     "QGroupBox::title {subcontrol-origin: margin;left: 7px;padding: 0px 5px 0px 5px;" \
                                     "color: rgb(145, 145, 145);}"

        self.basicBorderStyleSheet = "QWidget{color: rgb(230, 230, 230);border: 2px solid rgb(69,69,69);" \
                                     "border-radius: 0px;}"

        self.checkBoxStyleSheet = "QCheckBox::indicator {width: 13px;height: 13px; border-radius: 0px;}" \
                                  "QCheckBox::indicator:unchecked {image: " \
                                  "url(./UI/resources/images/checkbox/empty_nohover.png);}" \
                                  "QCheckBox::indicator:unchecked:hover " \
                                  "{image: url(./UI/resources/images/checkbox/empty_hover.png);}" \
                                  "QCheckBox::indicator:checked {image: " \
                                  "url(./UI/resources/images/checkbox/filled_nohover.png);}" \
                                  "QCheckBox::indicator:checked:hover {image: " \
                                  "url(./UI/resources/images/checkbox/filled_hover2.png);}"

        self.scrollStyleSheet = "QWidget{border-top: 1px solid rgb(230, 230, 230);" \
                                "border-bottom: 1px solid rgb(230, 230, 230);}" \
                                "QScrollBar:vertical {border-left: 1px solid rgb(230, 230, 230);" \
                                "border-top: 0px solid rgb(230, 230, 230);" \
                                "border-bottom: 0px solid rgb(230, 230, 230);" \
                                "border-right: 1px solid rgb(230, 230, 230);background: rgb(39,39,39);" \
                                "width: 15px;margin: 15px 0 15px 0; border-radius: 0px;}" \
                                "QScrollBar::handle:vertical {background: rgb(210, 210, 210);min-height: 15px;}" \
 \
                                "QScrollBar::add-line:vertical {border-top: 0px solid rgb(230, 230, 230);" \
                                "border-right: 1px solid rgb(230, 230, 230);" \
                                "border-left: 1px solid rgb(230, 230, 230);" \
                                "background: rgb(39,39,39);height: 15px;subcontrol-position: bottom;" \
                                "subcontrol-origin: margin;image: url(./resources/images/misc/arrow_downs.png);}" \
 \
                                "QScrollBar::sub-line:vertical {border-left: 1px solid rgb(230, 230, 230);" \
                                "border-right: 1px solid rgb(230, 230, 230);" \
                                "border-bottom: 0px solid rgb(230, 230, 230);" \
                                "background: rgb(39,39,39);height: 15px;subcontrol-position: top;" \
                                "subcontrol-origin: margin;image: url(./resources/images/misc/arrow_ups.png);}" \
 \
                                "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {background: none;}"

        self.scrollStyleSheetFull = "QWidget{border-top: 1px solid rgb(230, 230, 230);" \
                                    "border-bottom: 1px solid rgb(230, 230, 230);" \
                                    "border-left: 1px solid rgb(230, 230, 230);" \
                                    "border-right: 1px solid rgb(230, 230, 230);}" \
                                    "QScrollBar:vertical {border-top: 1px solid rgb(230, 230, 230);" \
                                    "border-bottom: 1px solid rgb(230, 230, 230);background: rgb(39,39,39);" \
                                    "width: 15px;margin: 15px 0 15px 0; border-radius: 0px;}" \
                                    "QScrollBar::handle:vertical {background: white;min-height: 15px;}" \
 \
                                    "QScrollBar::add-line:vertical {border-top: 1px solid rgb(230, 230, 230);" \
                                    "border-left: 1px solid rgb(230, 230, 230);" \
                                    "background: rgb(69,69,69);height: 15px;subcontrol-position: bottom;" \
                                    "subcontrol-origin: margin;image: url(./resources/images/misc/arrow_downs.png);}" \
 \
                                    "QScrollBar::sub-line:vertical {border-left: 1px solid rgb(230, 230, 230);" \
                                    "border-bottom: 1px solid rgb(230, 230, 230);" \
                                    "background: rgb(69,69,69);height: 15px;subcontrol-position: top;" \
                                    "subcontrol-origin: margin;image: url(./resources/images/misc/arrow_ups.png);}" \
 \
                                    "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {background: none;}"

        self.listStyleSheet ="QWidget{background-color: rgb(39, 39, 39);color: rgb(230, 230, 230);" \
                             "border: 2px solid rgb(69,69,69); border-radius: 0px;}" \
                             "QScrollBar::add-line:vertical {border-left: 0px solid rgb(230, 230, 230);" \
                             "border-right: 0px solid rgb(230, 230, 230);border-top: 0px solid rgb(230, 230, 230);" \
                             "border-bottom: 0px solid rgb(230, 230, 230);" \
                             "background: rgb(69,69,69);height: 15px;subcontrol-position: bottom;" \
                             "subcontrol-origin: margin;image: url(./UI/resources/images/misc/arrow_downs.png);}" \
 \
                             "QScrollBar::sub-line:vertical {border-left: 0px solid rgb(230, 230, 230);" \
                             "border-top: 0px solid rgb(230, 230, 230);border-right: 0px solid rgb(230, 230, 230);" \
                             "border-bottom: 0px solid rgb(230, 230, 230);" \
                             "background: rgb(69,69,69);height: 15px;subcontrol-position: top;" \
                             "subcontrol-origin: margin;image: url(./UI/resources/images/misc/arrow_ups.png);}" \
 \
                             "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {background: none;}"

        self.resizeStyleSheet = "QWidget{color: rgb(230, 230, 230); border-radius: 0px;}" \
                                "QWidget:hover{color: rgb(187, 134, 252); border-radius: 0px;}"

        self.windowbarLabelStyleSheet = "QLabel{padding: 0px 0px 5px 0px; border-radius: 0px;}"

        self.WBminimizeStyleSheet = "QPushButton{background-color: rgb(22, 22, 22);color: rgb(200, 200, 200);" \
                                    "border: 0px solid rgb(69,69,69);padding: 0px 0px 4px 0px;}" \
                                    "QPushButton:hover{background-color: rgb(56, 56, 56);color: rgb(230, 230, 230);" \
                                    "border: 0px solid rgb(69,69,69);}" \
                                    "QPushButton:pressed{background-color: rgb(69, 69, 69);color: rgb(250, 250, 250);" \
                                    "border: 0px solid rgb(250, 250, 250);}"
        self.WBmaximizeStyleSheet = "QPushButton{background-color: rgb(22, 22, 22);color: rgb(200, 200, 200);" \
                                    "border: 0px solid rgb(69,69,69);padding: 0px 0px 4px 0px;}" \
                                    "QPushButton:hover{background-color: rgb(56, 56, 56);" \
                                    "color: rgb(230, 230, 230);border: 0px solid rgb(69,69,69);}" \
                                    "QPushButton:pressed{background-color: rgb(69, 69, 69);color: rgb(250, 250, 250);" \
                                    "border: 0px solid rgb(250, 250, 250);}"

        self.WBexitStyleSheet = "QPushButton{background-color: rgb(22, 22, 22);color: rgb(200, 200, 200);" \
                                "border: 0px solid rgb(69,69,69);padding: 0px 0px 4px 0px;}" \
                                "QPushButton:hover{background-color: #f12b2b;color: rgb(230, 230, 230);" \
                                "border: 0px solid rgb(69,69,69);}" \
                                "QPushButton:pressed{background-color: #ff5757;color: rgb(250, 250, 250);" \
                                "border: 0px solid rgb(250, 250, 250);}"

        self.comboboxStyleSheet = "QWidget{background-color: rgb(39, 39, 39);color: rgb(230, 230, 230);" \
                                  "border: 2px solid rgb(69,69,69); border-radius: 0px;}" \
                                  "QWidget:hover{background-color: rgb(54, 54, 54);color: rgb(230, 230, 230);" \
                                  "border: 2px solid rgb(76,76,76);}" \
                                  "QComboBox::down-arrow {image: url(./UI/resources/images/misc/arrow_downs.png);}" \
                                  "QComboBox::drop-down {border: 0px solid black;subcontrol-origin: padding;" \
                                  "subcontrol-position: top right;width: 20px;}"

        self.tabStyleSheet = "QTabWidget:pane{border: 1px solid rgb(230, 230, 230); border-radius: 0px;}" \
                             "QTabBar:tab{background-color: rgb(39, 39, 39);color: rgb(230, 230, 230);" \
                             "border-top: 1px solid rgb(230, 230, 230);border-left: 1px solid rgb(230, 230, 230);" \
                             "border-right: 1px solid rgb(230, 230, 230);border-top-left-radius: 4px;" \
                             "border-top-right-radius: 2px;min-width: 8ex;padding: 4px;}" \
                             "QTabBar::tab:!selected {background-color: rgb(39, 39, 39);" \
                             "border-bottom 2px solid rgb(39, 39, 39);}" \
                             "QTabBar::tab:selected {background-color: rgb(69, 69, 69);margin-left: -4px;" \
                             "margin-right: -4px;}" \
                             "QTabBar::tab:!selected {margin-top: 3px;}" \
                             "QTabBar::tab:first:selected {margin-left: 0;}" \
                             "QTabBar::tab:last:selected {margin-right: 0;}" \
                             "QTabBar::tab:only-one {margin: 0;}"

        self.backStyleSheet = "QPushButton{color: rgb(69, 69, 69); border-radius: 0px;}" \
                              "QPushButton:hover{color: rgb(187, 134, 252);}" \
                              "QPushButton:pressed{color: rgb(211, 175, 255);}"

        self.creditsStyleSheet = "QWidget{color: rgb(22, 22, 22);padding-left: 9px; border-radius: 0px;}" \
                                 "QWidget:hover{color: rgb(39, 39, 39);}"

        self.qss_debug = "QWidget{background-color: rgb(255, 0, 0);}"

        self.qss_button_play = "QPushButton{ background-image: url(./UI/resources/images/button/play_idle.png);}" \
                               "QPushButton::hover{ background-image: url(./UI/resources/images/button/play_hover.png);}" \
                               "QPushButton::pressed{ background-image: url(./UI/resources/images/button/play_press.png);}"

        self.qss_button_pause = "QPushButton{ background-image: url(./UI/resources/images/button/pause_idle.png);}" \
                                "QPushButton::hover{ background-image: url(./UI/resources/images/button/pause_hover.png);}" \
                                "QPushButton::pressed{ background-image: url(./UI/resources/images/button/pause_press.png);}"

        self.qss_button_break = "QPushButton{ background-image: url(./UI/resources/images/button/break_idle.png);}" \
                                "QPushButton::hover{ background-image: url(./UI/resources/images/button/break_hover.png);}" \
                                "QPushButton::pressed{ background-image: url(./UI/resources/images/button/break_press.png);}"

        self.qss_button_reset = "QPushButton{ background-image: url(./UI/resources/images/button/reset_idle.png);}" \
                                "QPushButton::hover{ background-image: url(./UI/resources/images/button/reset_hover_pressed.png);}" \
                                "QPushButton::pressed{ background-image: url(./UI/resources/images/button/reset_hover_pressed.png);}"