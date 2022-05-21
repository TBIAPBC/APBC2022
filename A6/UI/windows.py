"""
Main Windows
"""
from UI.misc_widgets import *
from UI.start_ui import Start_UI


class MainWindow(QMainWindow, DarkQML):
    def __init__(self):
        QMainWindow.__init__(self)
        # self.ui = Ui_MainWindow()
        # self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # self.setWindowIcon(QtGui.QIcon("./main.ico"))

        self.show()
        self.pressing = False
        self.start = QPoint(0, 0)
        self.center()
        self.oldPos = self.pos()

        # shadow to main window -> no margins
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.setGraphicsEffect(self.shadow)

    def mouseReleaseEvent(self, QMouseEvent):
        if self.ui.is_maximized is False:
            self.pressing = False

    def mousePressEvent(self, event):
        if self.ui.is_maximized is False:
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.ui.is_maximized is False:
            if event.pos().y() > 25:
                return
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class StartWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # init ui
        self.start_ui = Start_UI(self)

        # remove title bar
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # drop shadow
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 100))
        self.start_ui.shadow_frame.setGraphicsEffect(self.shadow)

        # show
        self.show()

    def play(self):
        self.main = MainWindow()
        self.close()

