"""
Widget to set up game
"""
import os
from UI.misc_widgets import *
from Game.register_robots import robot_module_names


class WidgetSettings(QWidget, DarkQSS):
    def __init__(self, parent_ui):
        super().__init__()
        self.parent_ui = parent_ui
        self.setup_widget()

    def setup_widget(self):
        ### main layout
        self.main_lay = QVBoxLayout()
        self.main_lay.setSpacing(9)
        self.main_lay.setContentsMargins(6, 6, 6, 6)
        self.setLayout(self.main_lay)

        ### settings group box
        # setup gb
        self.gb_settings = QGroupBox()
        self.gb_settings.setTitle("Settings")
        self.gb_settings.setFont(self.font_2)
        self.gb_settings.setStyleSheet(self.subgroupboxStyleSheet)
        # add to layout
        self.main_lay.addWidget(self.gb_settings)

        # layout to groupbox
        self.lay_gb = QFormLayout()
        self.lay_gb.setSpacing(12)
        self.setContentsMargins(9, 9, 9, 9)
        self.gb_settings.setLayout(self.lay_gb)

        ### add items to widget
        # select robots -> label - custom robot select widget
        self.label_robots = QLabel()
        self.label_robots.setFont(self.font_0)
        self.label_robots.setText("Select Robots")
        self.label_robots.setStyleSheet(self.disableStyleSheet)

        self.widget_robots = WidgetRobots()

        # select map -> label - (combobox - combobox/(x, y, d))

        self.label_map = QLabel()
        self.label_map.setFont(self.font_0)
        self.label_map.setText("Select Map")
        self.label_map.setStyleSheet(self.disableStyleSheet)

        self.widget_map = MapWidget()

        # set rounds -> label - line edit
        self.label_rounds = QLabel()
        self.label_rounds.setFont(self.font_0)
        self.label_rounds.setText("Set Rounds")
        self.label_rounds.setStyleSheet(self.disableStyleSheet)

        self.line_rounds = QLineEdit()
        self.line_rounds.setFont(self.font_2)
        self.line_rounds.setPlaceholderText("Enter Number of Rounds to play")
        self.line_rounds.setStyleSheet(self.basicWidgetStyleSheet)

        # set seed -> label - line edit
        """planned"""

        # spacer
        self.spacer = QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # add to layout
        self.lay_gb.addRow(self.label_robots, self.widget_robots)
        self.lay_gb.addRow(self.label_map, self.widget_map)
        self.lay_gb.addRow(self.label_rounds, self.line_rounds)
        self.lay_gb.addItem(self.spacer)

    def validate_input(self):
        pass


class WidgetRobots(QScrollArea, DarkQSS):
    # custom robot select widget
    def __init__(self):
        super().__init__()
        self.bots = []
        self.loaded_bots = robot_module_names
        self.check_bots = []

        self.__setup()

    def __setup(self):
        ### scroll widget
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setWidgetResizable(True)
        self.setStyleSheet(self.scrollStyleSheet)

        self.scrollWidget = QWidget()
        self.scrollWidget.setStyleSheet(self.disableStyleSheet)
        self.setWidget(self.scrollWidget)

        ### scroll layout
        self.lay_scroll = QFormLayout()
        self.lay_scroll.setContentsMargins(9, 9, 9, 9)
        self.lay_scroll.setSpacing(6)
        self.scrollWidget.setLayout(self.lay_scroll)

        # set bots as checkboxes
        for key in self.loaded_bots:
            tmp_check = QCheckBox()
            tmp_check.setFont(self.font_0)
            tmp_check.setText(key)
            tmp_check.setStyleSheet(self.checkBoxStyleSheet)
            tmp_check.setCursor((QCursor(Qt.PointingHandCursor)))
            self.check_bots.append(tmp_check)
            self.lay_scroll.addWidget(tmp_check)

    def read_checked_bots(self):
        pass


class MapWidget(QWidget, DarkQSS):
    def __init__(self):
        super().__init__()
        self.random_map = True
        self.chosen_map = None
        self.random_x_y_d = []

        self.options_select = ["Random Map", "Preset Map"]
        self.options_map = []

        self.__read_maps()
        self.__setup()
        self.__connect()

    def __setup(self):
        ### main widget
        # main layout
        self.lay_main = QFormLayout()
        self.lay_main.setSpacing(9)
        self.lay_main.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.lay_main)

        # select combobox
        self.cbox_select = AntiScrollQComboBox()
        self.cbox_select.setFont(self.font_0)
        self.cbox_select.setStyleSheet(self.comboboxStyleSheet)
        self.cbox_select.addItems(self.options_select)
        self.cbox_select.setMaximumWidth(120)
        self.cbox_select.setMinimumWidth(120)
        self.cbox_select.setCursor(QCursor(Qt.PointingHandCursor))

        # switch widget
        self.widget_switch = QWidget()
        self.lay_swidget = QVBoxLayout()
        self.lay_swidget.setSpacing(9)
        self.lay_swidget.setContentsMargins(0, 0, 0, 0)
        self.widget_switch.setLayout(self.lay_swidget)

        # add them to main layout
        self.lay_main.addRow(self.cbox_select, self.widget_switch)

        ### fill swidget
        # random
        self.swidget_random = QWidget()
        self.lay_swidget_random = QHBoxLayout()
        self.lay_swidget_random.setContentsMargins(0, 0, 0, 0)
        self.lay_swidget_random.setSpacing(6)
        self.swidget_random.setLayout(self.lay_swidget_random)

        self.label_width = QLabel()
        self.label_width.setText("Width:")
        self.label_width.setMaximumWidth(60)
        self.label_width.setMinimumWidth(60)
        self.label_width.setStyleSheet(self.disableStyleSheet)
        self.label_width.setFont(self.font_0)

        self.label_height = QLabel()
        self.label_height.setText("Height:")
        self.label_height.setMaximumWidth(60)
        self.label_height.setMinimumWidth(60)
        self.label_height.setStyleSheet(self.disableStyleSheet)
        self.label_height.setFont(self.font_0)

        self.label_density = QLabel()
        self.label_density.setText("Density:")
        self.label_density.setMaximumWidth(70)
        self.label_density.setMinimumWidth(70)
        self.label_density.setStyleSheet(self.disableStyleSheet)
        self.label_density.setFont(self.font_0)

        self.line_width = QLineEdit()
        self.line_width.setPlaceholderText("int: width")
        self.line_width.setFont(self.font_0)
        self.line_width.setStyleSheet(self.basicWidgetStyleSheet)

        self.line_height = QLineEdit()
        self.line_height.setPlaceholderText("int: height")
        self.line_height.setFont(self.font_0)
        self.line_height.setStyleSheet(self.basicWidgetStyleSheet)

        self.line_density = QLineEdit()
        self.line_density.setPlaceholderText("float: density")
        self.line_density.setFont(self.font_0)
        self.line_density.setStyleSheet(self.basicWidgetStyleSheet)

        self.lay_swidget_random.addWidget(self.label_width)
        self.lay_swidget_random.addWidget(self.line_width)
        self.lay_swidget_random.addWidget(self.label_height)
        self.lay_swidget_random.addWidget(self.line_height)
        self.lay_swidget_random.addWidget(self.label_density)
        self.lay_swidget_random.addWidget(self.line_density)

        # preset swidget
        self.swidget_preset = AntiScrollQComboBox()
        self.swidget_preset.setStyleSheet(self.comboboxStyleSheet)
        self.swidget_preset.setCursor(QCursor(Qt.PointingHandCursor))
        self.swidget_preset.addItems(self.options_map)
        self.swidget_preset.setFont(self.font_0)

        # add to swidget layou
        self.lay_swidget.addWidget(self.swidget_random)
        self.lay_swidget.addWidget(self.swidget_preset)

        # hide preset
        self.swidget_preset.hide()

    def __connect(self):
        self.cbox_select.currentIndexChanged.connect(self.__select_swidget)

    def __select_swidget(self):
        if self.random_map is True:
            self.random_map = False
            self.swidget_random.hide()
            self.swidget_preset.show()
        else:
            self.random_map = True
            self.swidget_random.show()
            self.swidget_preset.hide()

    def __read_maps(self):
        map_dir = os.fsencode("./Maps")
        for file in os.listdir(map_dir):
            file_name = os.fsencode(file).decode("utf-8")
            self.options_map.append(file_name)

