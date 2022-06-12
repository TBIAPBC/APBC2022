"""
UI for main screen
"""
import sys
import time
import os
from importlib import import_module

from UI.misc_widgets import *
from UI.settings_widget import WidgetSettings
from UI.game_widget import WidgetGame
from UI.scoreboard_widget import WidgetScoreboard
from UI.map_widget import WidgetMap
from UI.finish_widget import WidgetFinish
from UI.tools_widget import WidgetTools
from Game import game_utils
from Game.register_robots import robot_module_names
from Game import threads


class MainUI(DarkQSS):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setup_ui()

        # stuff
        self.is_maximized = False
        self.stats = []
        self.robots = []

    def setup_ui(self):
        self.parent.resize(900, 600)
        self.parent.setMinimumSize(QSize(900, 600))

        ### central widget
        self.centralwidget = QWidget(self.parent)
        self.lay_central_grid = QGridLayout(self.centralwidget)
        self.lay_central_grid.setContentsMargins(5, 5, 5, 5)
        self.lay_central_grid.setSpacing(0)

        ### resize widget
        self.resize_TR = QSizeGrip(self.centralwidget)
        self.resize_TR.setMinimumSize(QSize(5, 5))
        self.resize_TR.setMaximumSize(QSize(5, 5))
        self.resize_TR.setCursor(QCursor(Qt.SizeBDiagCursor))
        self.resize_TR.setStyleSheet(self.disableStyleSheet)

        self.resize_R = SizeGripRight(self.parent)
        self.resize_R.setMinimumSize(QSize(5, 0))
        self.resize_R.setMaximumSize(QSize(5, 16777215))
        self.resize_R.setCursor(QCursor(Qt.SizeHorCursor))
        self.resize_R.setStyleSheet(self.disableStyleSheet)

        self.resize_TL = QSizeGrip(self.centralwidget)
        self.resize_TL.setMinimumSize(QSize(5, 5))
        self.resize_TL.setMaximumSize(QSize(5, 5))
        self.resize_TL.setCursor(QCursor(Qt.SizeFDiagCursor))
        self.resize_TL.setStyleSheet(self.disableStyleSheet)

        self.resize_L = SizeGripLeft(self.parent)
        self.resize_L.setMinimumSize(QSize(5, 0))
        self.resize_L.setMaximumSize(QSize(5, 16777215))
        self.resize_L.setCursor(QCursor(Qt.SizeHorCursor))
        self.resize_L.setStyleSheet(self.disableStyleSheet)

        self.resize_T = SizeGripTop(self.parent)
        self.resize_T.setMinimumSize(QSize(0, 5))
        self.resize_T.setMaximumSize(QSize(16777215, 5))
        self.resize_T.setCursor(QCursor(Qt.SizeVerCursor))
        self.resize_T.setStyleSheet(self.disableStyleSheet)

        self.resize_B = SizeGripBottom(self.parent)
        self.resize_B.setMinimumSize(QSize(0, 5))
        self.resize_B.setMaximumSize(QSize(16777215, 5))
        self.resize_B.setCursor(QCursor(Qt.SizeVerCursor))
        self.resize_B.setStyleSheet(self.disableStyleSheet)

        self.resize_BR = QSizeGrip(self.centralwidget)
        self.resize_BR.setMinimumSize(QSize(5, 5))
        self.resize_BR.setMaximumSize(QSize(5, 5))
        self.resize_BR.setCursor(QCursor(Qt.SizeFDiagCursor))
        self.resize_BR.setFocusPolicy(Qt.TabFocus)
        self.resize_BR.setStyleSheet(self.disableStyleSheet)

        self.resize_BL = QSizeGrip(self.centralwidget)
        self.resize_BL.setMinimumSize(QSize(5, 5))
        self.resize_BL.setMaximumSize(QSize(5, 5))
        self.resize_BL.setCursor(QCursor(Qt.SizeBDiagCursor))
        self.resize_BL.setStyleSheet(self.disableStyleSheet)

        # add to layout
        self.lay_central_grid.addWidget(self.resize_TR, 0, 4, 1, 1)
        self.lay_central_grid.addWidget(self.resize_R, 1, 4, 1, 1)
        self.lay_central_grid.addWidget(self.resize_TL, 0, 1, 1, 1)
        self.lay_central_grid.addWidget(self.resize_L, 1, 1, 1, 1)
        self.lay_central_grid.addWidget(self.resize_T, 0, 3, 1, 1)
        self.lay_central_grid.addWidget(self.resize_B, 2, 3, 1, 1)
        self.lay_central_grid.addWidget(self.resize_BR, 2, 4, 1, 1)
        self.lay_central_grid.addWidget(self.resize_BL, 2, 1, 1, 1)

        ### shadow frame
        self.frame_shadow = QFrame(self.centralwidget)
        self.frame_shadow.setStyleSheet(self.mainUIStyleSheet)
        self.frame_shadow.setFrameShape(QFrame.StyledPanel)
        self.frame_shadow.setFrameShadow(QFrame.Raised)
        self.lay_shadow_frame = QVBoxLayout(self.frame_shadow)
        self.lay_shadow_frame.setContentsMargins(0, 0, 0, 0)
        self.lay_shadow_frame.setSpacing(0)

        ### main widget
        self.widget_main = QWidget(self.frame_shadow)
        self.widget_main.setStyleSheet(self.mainUIStyleSheet)
        self.lay_main = QVBoxLayout(self.widget_main)
        self.lay_main.setContentsMargins(0, 0, 0, 0)
        self.lay_main.setSpacing(0)

        ### title bar
        # layout
        self.title_bar = QWidget(self.widget_main)
        self.title_bar.setMinimumSize(QSize(0, 25))
        self.title_bar.setMaximumSize(QSize(16777215, 25))
        self.lay_title_bar = QHBoxLayout(self.title_bar)
        self.lay_title_bar.setContentsMargins(0, 0, 0, 0)
        self.lay_title_bar.setSpacing(0)
        self.lay_main.addWidget(self.title_bar)
        # icon
        self.label_title_bar_icon = QLabel(self.title_bar)
        self.label_title_bar_icon.setMinimumSize(QSize(25, 25))
        self.label_title_bar_icon.setMaximumSize(QSize(25, 25))
        self.label_title_bar_icon.setAlignment(Qt.AlignCenter)
        self.label_title_bar_icon.setText("#")
        self.label_title_bar_icon.setFont(self.font_0)
        # title
        self.lable_title_bar_title = QLabel(self.title_bar)
        self.lable_title_bar_title.setFont(self.font_0)
        self.lable_title_bar_title.setText("Robot Race")
        # spacer
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        # button minimize
        self.button_title_bar_minimize = QPushButton(self.title_bar)
        self.button_title_bar_minimize.setMinimumSize(QSize(50, 25))
        self.button_title_bar_minimize.setMaximumSize(QSize(50, 25))
        self.button_title_bar_minimize.setFont(self.font_0)
        self.button_title_bar_minimize.setText("-")
        self.button_title_bar_minimize.setStyleSheet(self.WBminimizeStyleSheet)
        # button maximize
        self.button_title_bar_maximize = QPushButton(self.title_bar)
        self.button_title_bar_maximize.setMinimumSize(QSize(50, 25))
        self.button_title_bar_maximize.setMaximumSize(QSize(50, 25))
        self.button_title_bar_maximize.setText("o")
        self.button_title_bar_maximize.setFont(self.font_0)
        self.button_title_bar_maximize.setStyleSheet(self.WBmaximizeStyleSheet)
        # button exit
        self.button_title_bar_exit = QPushButton(self.title_bar)
        self.button_title_bar_exit.setMinimumSize(QSize(50, 25))
        self.button_title_bar_exit.setMaximumSize(QSize(50, 25))
        self.button_title_bar_exit.setText("x")
        self.button_title_bar_exit.setFont(self.font_0)
        self.button_title_bar_exit.setStyleSheet(self.WBexitStyleSheet)
        # add to layout
        self.lay_title_bar.addWidget(self.label_title_bar_icon)
        self.lay_title_bar.addWidget(self.lable_title_bar_title)
        self.lay_title_bar.addItem(spacerItem)
        self.lay_title_bar.addWidget(self.button_title_bar_minimize)
        self.lay_title_bar.addWidget(self.button_title_bar_maximize)
        self.lay_title_bar.addWidget(self.button_title_bar_exit)

        ### content widget
        # setup
        self.content_widget = QWidget(self.widget_main)
        self.lay_main.addWidget(self.content_widget)
        self.lay_shadow_frame.addWidget(self.widget_main)
        self.lay_central_grid.addWidget(self.frame_shadow, 1, 3, 1, 1)
        # create layout
        self.lay_content = QVBoxLayout()
        self.lay_content.setContentsMargins(0, 0, 0, 0)
        self.lay_content.setSpacing(0)
        self.content_widget.setLayout(self.lay_content)

        self.content_widget.setStyleSheet(self.mainStyleSheet)

        ##### content widgets #####
        ### settings
        self.widget_settings = WidgetSettings(self)
        self.lay_content.addWidget(self.widget_settings)

        ### game
        self.widget_game = WidgetGame(self)
        self.lay_content.addWidget(self.widget_game)
        self.widget_game.hide()

        ### Map
        self.map_widget = WidgetMap(self, self.widget_game.widget_left)
        self.widget_game.lay_left.addWidget(self.map_widget)

        ### scoreboard
        self.widget_scoreboard = WidgetScoreboard(self)
        self.widget_game.lay_right.addWidget(self.widget_scoreboard)

        # spacer
        self.spacer_right = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.widget_game.lay_right.addItem(self.spacer_right)

        ### tools
        self.tools = WidgetTools()
        self.widget_game.lay_right.addWidget(self.tools)

        ### finish screen widget
        self.widget_finish = WidgetFinish(self)
        self.widget_game.lay_left.addWidget(self.widget_finish)
        self.widget_finish.hide()

        ##### window-ui / signal-slot connections #####
        self.parent.setCentralWidget(self.centralwidget)
        QMetaObject.connectSlotsByName(self.parent)

        ####################################################################################
        # connect buttons
        ####################################################################################
        # title bar
        self.button_title_bar_minimize.clicked.connect(self.btn_minimize)
        self.button_title_bar_exit.clicked.connect(self.btn_exit)
        self.button_title_bar_maximize.clicked.connect(self.btn_maximize)

        # widgets
        self.widget_settings.button_play.clicked.connect(self.__btn_wdgt_settings_play)
        self.tools.button_play.clicked.connect(self.__btn_tools_play)
        self.tools.button_break.clicked.connect(self.__btn_tools_break)
        self.tools.button_reset.clicked.connect(self.__btn_tools_reset)
        self.widget_finish.button_again.clicked.connect(self.__btn_wdgt_finish_play_again)
        self.widget_finish.button_back.clicked.connect(self.__btn_wdgt_finish_change_settings)

    ####################################################################################
    # BUTTONS and METHODS
    ####################################################################################
    def btn_exit(self):
        self.__del_images()
        sys.exit(self.parent.app.exec_())

    def btn_maximize(self):
        if self.is_maximized is False:
            self.parent.showMaximized()
            self.is_maximized = True
            self.__hide_resize()
        else:
            self.parent.showNormal()
            self.is_maximized = False
            self.__show_resize()

    def btn_minimize(self):
        self.parent.showMinimized()

    def __btn_tools_play(self):
        self.tools.change_play_pause()

    def __btn_tools_break(self):
        print("-----------------------\nBREAK\n-----------------------")
        self.break_game()

    def __btn_tools_reset(self):
        print("-----------------------\nRESET\n-----------------------")
        self.reset_game()

    def __show_resize(self):
        self.lay_central_grid.setContentsMargins(5, 5, 5, 5)

        self.resize_BR.show()
        self.resize_B.show()
        self.resize_L.show()
        self.resize_R.show()
        self.resize_T.show()
        self.resize_BL.show()
        self.resize_TL.show()
        self.resize_TR.show()

    def __hide_resize(self):
        self.lay_central_grid.setContentsMargins(0, 0, 0, 0)

        self.resize_BR.hide()
        self.resize_B.hide()
        self.resize_L.hide()
        self.resize_R.hide()
        self.resize_T.hide()
        self.resize_BL.hide()
        self.resize_TL.hide()
        self.resize_TR.hide()

    def __btn_wdgt_settings_play(self):
        if self.widget_settings.validator() is False:
            return
        self.settings = self.widget_settings.get_settings()

        self.widget_settings.hide()
        self.widget_game.show()

        self.game_play()

    def __btn_wdgt_finish_play_again(self):
        print("-----------------------\nPLAY AGAIN\n-----------------------")
        self.play_again()

    def __btn_wdgt_finish_change_settings(self):
        print("-----------------------\nBACK TO SETTINGS\n-----------------------")
        self.back_settings()

    def __block_tools(self):
        self.tools.button_play.blockSignals(True)
        self.tools.button_break.blockSignals(True)
        self.tools.button_reset.blockSignals(True)

    def __unblock_tools(self):
        self.tools.button_reset.blockSignals(False)
        self.tools.button_play.blockSignals(False)
        self.tools.button_break.blockSignals(False)

    ###########################################################################################
    # Game Methods
    ###########################################################################################
    def game_show(self):
        ##### testing:

        # get settings for game
        round_numbers = int(self.settings.rounds)
        fps = 6

        # init and reset scoreboard widgets
        QCoreApplication.processEvents()
        for widget in self.widget_scoreboard.score_widgets:
            widget.close()
        for widget in self.widget_scoreboard.place_widgets:
            widget.close()
        self.widget_scoreboard.build_scoreboard(len(self.robots))

        # display game
        for round_no in range(1, round_numbers + 1):
            QCoreApplication.processEvents()

            # check if paused
            paused = self.tools.paused
            while paused is True:
                QCoreApplication.processEvents()
                paused = self.tools.paused

            # set time to get exact
            time_round_start = time.time()

            # display internals !!!
            while not os.path.exists(f"./Tmp/sim_{round_no}.png"):
                # trap here until img of current round exists
                QCoreApplication.processEvents()
            self.map_widget.display_img_round(round_no)

            while len(self.stats) < round_no:
                # trap here to wait for stats from game thread
                QCoreApplication.processEvents()

            stats_updated = sorted(self.stats[round_no - 1], key=lambda x: -x[1])
            self.widget_scoreboard.update_scoreboard(stats_updated, self.robots, round_no)

            # remove old image
            if round_no > 1:
                self.__del_image(round_no - 1)

            # end time and fps calculation
            time_round_end = time.time()
            time_used = time_round_end - time_round_start
            time_to_sleep = (1/fps) - time_used
            if time_to_sleep > 0:
                time.sleep(time_to_sleep)

            # while time_to_sleep > 0:
            #     time.sleep(0.1)
            #     time_to_sleep -= 0.1

        # end of game
        self.__del_image(round_numbers + 1)  # delete last image
        self.__block_tools()  # block tools to avoid unintended behavior
        self.map_widget.hide()
        self.widget_finish.show()

        # get winner and display
        self.widget_finish.display_winner("Marcel")

    def game_play(self):
        ### run game internally, get stats and imgs
        self.stats = []

        # setup map
        if self.settings.random_map is True:
            game_map = game_utils.Map.makeRandom(width=self.settings.random_width, height=self.settings.random_height,
                                                 p=self.settings.random_density)
        else:
            game_map = game_utils.Map.read(f"./Maps/{self.settings.preset_map}")

        # run
        self.thread_simulator = threads.BackgroundGameThread(map_=game_map, fps=16, rounds=self.settings.rounds)

        robots_for_game = {robot: robot_module_names[robot] for robot in self.settings.robots}

        robot_modules = {m: import_module(m) for m in robots_for_game.values()}
        for name, module_name in robot_module_names.items():
            for p in robot_modules[module_name].players:
                p.player_modname = name
                self.thread_simulator.add_player(p)

        self.thread_simulator.start()
        self.thread_simulator.stats_round.connect(self.slot_append_stats)
        self.thread_simulator.robot_list.connect(self.slot_set_robots)

        QCoreApplication.processEvents()
        time.sleep(2.5)
        self.map_widget.label_img.show()
        self.game_show()

    def play_again(self):
        # after finish: delete stats, restart with same settings
        self.__unblock_tools()
        self.widget_finish.hide()
        self.map_widget.label_img.hide()
        self.map_widget.show()
        self.game_play()

    def back_settings(self):
        # after finish: delete stats, go back to settings
        self.__unblock_tools()
        self.widget_finish.hide()
        self.map_widget.label_img.hide()
        self.map_widget.show()
        self.widget_game.hide()
        self.widget_settings.show()

    def reset_game(self):
        # stop game, delete stats and imgs, restart with same settings
        self.__del_images()
        self.play_again()

    def break_game(self):
        # stop game, delete stats and imgs, go back to settings
        self.__del_images()
        self.back_settings()

    def __del_image(self, round_):
        # del specific image in Tmp
        img = f"./Tmp/sim_{round_}.png"
        if os.path.exists(img):
            os.remove(img)

    def __del_images(self):
        # delete all images in Tmp
        for file in os.listdir("./Tmp/"):
            os.remove(f"./Tmp/{file}")

    def __create_scoreboard(self, round_):
        pass

    def slot_append_stats(self, val):
        self.stats.append(val)

    def slot_set_robots(self, val):
        self.robots = val