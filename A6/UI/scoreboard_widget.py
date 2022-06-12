"""
Widget to show stats
"""
from UI.misc_widgets import *


class WidgetScoreboard(QWidget, DarkQSS):
    def __init__(self, parent_ui,  player_count):
        super().__init__()
        self.parent_ui = parent_ui
        self.player_count = player_count

        self.score_widgets = []

        self.qss_first = "QWidget{background-color: rgba(0, 0, 0, 0);border: 2px solid rgba(0, 0, 0, 0); " \
                         "border-radius: 0px; color: rgb(3, 255, 233);}"
        self.qss_secod = "QWidget{background-color: rgba(0, 0, 0, 0);border: 2px solid rgba(0, 0, 0, 0); " \
                         "border-radius: 0px; color: rgb(187, 134, 252);}"
        self.qss_third = "QWidget{background-color: rgba(0, 0, 0, 0);border: 2px solid rgba(0, 0, 0, 0); " \
                         "border-radius: 0px; color: rgb(230, 230, 230);}"

        # might use this later for setting color of bot in scoreboard
        self.qss_replace = "QWidget{background-color: rgba(0, 0, 0, 0);border: 2px solid rgba(0, 0, 0, 0); " \
                           "border-radius: 0px; color: $color_replace$;}"

        self.__setup()

    def __setup(self):
        ### main layout
        self.lay_main = QVBoxLayout()
        self.lay_main.setSpacing(6)
        self.lay_main.setContentsMargins(9, 9, 9, 9)
        self.setLayout(self.lay_main)

        ### round widget
        self.widget_round = QWidget()
        self.lay_main.addWidget(self.widget_round)

        # layout
        self.lay_round = QHBoxLayout()
        self.lay_round.setContentsMargins(0, 0, 0, 0)
        self.lay_round.setSpacing(0)
        self.widget_round.setLayout(self.lay_round)

        # title
        self.label_title = QLabel()
        self.label_title.setText("Round:")
        self.label_title.setFont(self.font_1)
        self.label_title.setStyleSheet(self.disableStyleSheet)

        # spacer
        self.spacer_round = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)

        # round nr
        self.label_number = QLabel()
        self.label_number.setFont(self.font_1)
        self.label_number.setStyleSheet(self.disableStyleSheet)

        # add to widget
        self.lay_round.addWidget(self.label_title)
        self.lay_round.addItem(self.spacer_round)
        self.lay_round.addWidget(self.label_number)

        ### create scoreboard in gb
        self.gb_scoreboard = QGroupBox()
        self.gb_scoreboard.setTitle("Scoreboard")
        self.gb_scoreboard.setFont(self.font_2)
        self.gb_scoreboard.setStyleSheet(self.subgroupboxStyleSheet)
        self.lay_main.addWidget(self.gb_scoreboard)

        self.lay_gb = QFormLayout()
        self.lay_gb.setSpacing(9)
        self.lay_gb.setContentsMargins(9, 9, 9, 9)
        self.gb_scoreboard.setLayout(self.lay_gb)

        for i in range(self.player_count):
            label_place = QLabel()

            if i == 0:
                label_place.setStyleSheet(self.qss_first)
                label_score = LabelScore(self.qss_first)
            elif i == 1 or i == 2:
                label_place.setStyleSheet(self.qss_secod)
                label_score = LabelScore(self.qss_secod)
            else:
                label_score = LabelScore(self.qss_third)
                label_place.setStyleSheet(self.qss_third)

            label_place.setFont(self.font_0)
            label_place.setText(f"{i + 1}")

            self.score_widgets.append(label_score)
            self.lay_gb.addRow(label_place, label_score)

    def update_scoreboard(self, scores, round_nr):
        """
        sorted scores dummy input
        scores = [
            ["GodBot", 120030],
            ["DeepBot", 14842],
            ["SmartBot", 9387],
            ["DumBot", 1]
        ]
        """
        self.label_number.setText(str(round_nr))
        for i in range(len(self.score_widgets)):
            name = scores[i][0]
            score = str(scores[i][1])
            self.score_widgets[i].update(name, score)


class LabelScore(QWidget, DarkQSS):
    def __init__(self, qss):
        super().__init__()

        self.qss = qss

        self.setup()

    def setup(self):
        self.lay_main = QHBoxLayout()
        self.lay_main.setSpacing(0)
        self.lay_main.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.lay_main)

        self.label_name = QLabel()
        self.label_name.setStyleSheet(self.qss)
        self.label_name.setFont(self.font_0)

        self.spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.label_score = QLabel()
        self.label_score.setStyleSheet(self.qss)
        self.label_score.setFont(self.font_0)

        self.lay_main.addWidget(self.label_name)
        self.lay_main.addItem(self.spacer)
        self.lay_main.addWidget(self.label_score)

    def update(self, name, score):
        self.label_score.setText(score)
        self.label_name.setText(name)
