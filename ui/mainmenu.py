from game.game import *
from ui.basemenu import *
from ui.configurationmenu import *
from ui.overviewcanvas import *
from userdata import persistency
from .styles import STYLES


import tkinter as tk
from tkinter import ttk


class MainMenu(Menu):
    basemenu = None  # type: BaseMenu

    def __init__(self, window: Window, parent, game: Game):
        super(MainMenu, self).__init__(window, parent, game)

        self.upd = OverviewCanvas(self.window.left_pane, self, game)
        self.upd.update()

        self.frame = self.window.right_pane
        self.frame.rowconfigure(0, weight=0)
        self.frame.rowconfigure(1, weight=1)

    def display(self):
        persistency.save_game(self.game)
        self.window.clear_right_pane()
        self.upd.update()

        header = Frame(self.frame, **STYLES["header"])
        header.grid(column=0, row=0, sticky=NSEW)

    def pass_turn(self):
        self.game.pass_turn(no_action=True)
        self.display()

    def configuration_menu(self):
        ConfigurationMenu(self.window, self, self.game).display()

    def start_event(self, event) -> typing.Callable:
        EventMenu(self.window, self, self.game, event).display()

    def go_cp(self, cp: ControlPoint):
        if not cp.captured:
            return

        if self.basemenu:
            self.basemenu.dismiss()
            self.basemenu = None

        self.basemenu = BaseMenu(self.window, self, self.game, cp)
        self.basemenu.display()




