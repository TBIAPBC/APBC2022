import sys
from PyQt5.QtWidgets import QApplication
from UI.windows import StartWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StartWindow()
    sys.exit(app.exec_())
