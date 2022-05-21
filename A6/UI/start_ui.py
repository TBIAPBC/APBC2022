"""
UI for start screen
"""
from UI.misc_widgets import *


class Start_UI(DarkQML):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setup_ui(self.parent)

    def setup_ui(self, start_screen):
        start_screen.resize(680, 400)
        start_screen.setMinimumSize(QSize(680, 400))
        start_screen.setMaximumSize(QSize(680, 400))

        ### central widget
        self.central_widget = QWidget(start_screen)
        self.verticalLayout = QVBoxLayout(self.central_widget)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)

        ### shadow frame
        self.shadow_frame = QFrame(self.central_widget)
        self.shadow_frame.setStyleSheet(self.start_screen_StyleSheet)
        self.shadow_frame.setFrameShape(QFrame.StyledPanel)
        self.shadow_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout.addWidget(self.shadow_frame)

        ### main widget
        self.verticalLayout_2 = QVBoxLayout(self.shadow_frame)
        self.main_widget = QWidget(self.shadow_frame)
        self.verticalLayout_2.addWidget(self.main_widget)

        ### main items
        # layout
        self.lay_main = QVBoxLayout(self.main_widget)
        self.lay_main.setAlignment(Qt.AlignHCenter)

        # top spacer
        spacer_top = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Minimum)

        # label title
        self.label_title = QLabel(self.main_widget)
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.setStyleSheet(self.disableStyleSheet)
        self.label_title.setText("Robot Race")
        self.label_title.setFont(self.font_4)

        # mid spacer
        spacer_mid = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # button play
        self.button_play = QPushButton(self.main_widget)
        self.button_play.setText("Play")
        self.button_play.setFont(self.font_1)
        self.button_play.setStyleSheet(self.craftStyleSheet)
        self.button_play.setMinimumSize(120, 60)
        self.button_play.setMaximumSize(120, 60)
        self.button_play.setCursor(QCursor(Qt.PointingHandCursor))

        # button spacer
        spacer_bottom = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Minimum)

        # add items
        self.lay_main.addItem(spacer_top)
        self.lay_main.addWidget(self.label_title)
        self.lay_main.addItem(spacer_mid)
        self.lay_main.addWidget(self.button_play, 0, Qt.AlignHCenter)
        self.lay_main.addItem(spacer_bottom)

        #########################
        # connect ui
        start_screen.setCentralWidget(self.central_widget)
        QMetaObject.connectSlotsByName(start_screen)

        ##########################
        # connect buttons
        self.button_play.clicked.connect(self.btn_play)

    def btn_play(self):
        return self.parent.play()
