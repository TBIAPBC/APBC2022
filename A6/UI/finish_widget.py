"""
Widget to show finish screen
"""
from UI.misc_widgets import *


class WidgetFinish(QWidget, DarkQSS):
    def __init__(self, parent_ui):
        super().__init__()
        self.parent_ui = parent_ui
        self.winner_qss = "QWidget{background-color: rgba(0, 0, 0, 0);border: 2px solid rgba(0, 0, 0, 0); " \
                          "border-radius: 0px; color: rgb(3, 255, 233);}"

        self.__setup()

    def __setup(self):
        ### layout
        self.lay_main = QVBoxLayout()
        self.lay_main.setContentsMargins(9, 9, 9, 9)
        self.lay_main.setSpacing(6)
        self.setLayout(self.lay_main)

        ### spacer 1
        self.spacer_1 = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)

        ### label text
        self.label_text = QLabel()
        self.label_text.setText("The Winner is")
        self.label_text.setFont(self.font_4)
        self.label_text.setStyleSheet(self.disableStyleSheet)

        ### spacer 2
        self.spacer_2 = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)

        ### label winner
        self.label_winner = QLabel()
        self.label_winner.setFont(self.font_1)
        self.label_winner.setStyleSheet(self.winner_qss)

        ### spacer 3
        self.spacer_3 = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)

        ### button play again
        self.button_again = QPushButton()
        self.button_again.setFont(self.font_1)
        self.button_again.setText("Play Again")
        self.button_again.setFixedHeight(50)
        self.button_again.setFixedWidth(250)
        self.button_again.setStyleSheet(self.buttonStyleSheet)

        ### button back to settings
        self.button_back = QPushButton()
        self.button_back.setFont(self.font_1)
        self.button_back.setText("Back to Settings")
        self.button_back.setFixedHeight(50)
        self.button_back.setFixedWidth(250)
        self.button_back.setStyleSheet(self.buttonStyleSheet)

        ### spacer 4
        self.spacer_4 = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)

        # add to layout
        self.lay_main.addItem(self.spacer_1)
        self.lay_main.addWidget(self.label_text, 0, Qt.AlignHCenter)
        self.lay_main.addItem(self.spacer_2)
        self.lay_main.addWidget(self.label_winner, 0, Qt.AlignHCenter)
        self.lay_main.addItem(self.spacer_3)
        self.lay_main.addWidget(self.button_again, 0, Qt.AlignHCenter)
        self.lay_main.addWidget(self.button_back, 0, Qt.AlignHCenter)
        self.lay_main.addItem(self.spacer_4)

    def display_winner(self, winner):
        self.label_winner.setText(winner)
