from tkinter import *
from tkinter.ttk import *

from ui.window import *


class ConfigurationMenu(Menu):
    def __init__(self, window: Window, parent, game: Game):
        super(ConfigurationMenu, self).__init__(window, parent, game)
        self.frame = window.right_pane
        self.player_skill_var = StringVar()
        self.player_skill_var.set(self.game.settings.player_skill)

        self.enemy_skill_var = StringVar()
        self.enemy_skill_var.set(self.game.settings.enemy_skill)

        self.takeoff_var = BooleanVar()
        self.takeoff_var.set(self.game.settings.only_player_takeoff)

        self.night_var = BooleanVar()
        self.night_var.set(self.game.settings.night_disabled)

    def dismiss(self):
        self.game.settings.player_skill = self.player_skill_var.get()
        self.game.settings.enemy_skill = self.enemy_skill_var.get()
        self.game.settings.only_player_takeoff = self.takeoff_var.get()
        self.game.settings.night_disabled = self.night_var.get()
        super(ConfigurationMenu, self).dismiss()

    def display(self):
        self.window.clear_right_pane()

        Label(self.frame, text="Player coalition skill").grid(row=0, column=0)
        Label(self.frame, text="Enemy coalition skill").grid(row=1, column=0)

        OptionMenu(self.frame, self.player_skill_var, "Average", "Good", "High", "Excellent").grid(row=0, column=1)
        OptionMenu(self.frame, self.enemy_skill_var, "Average", "Good", "High", "Excellent").grid(row=1, column=1)

        Checkbutton(self.frame, text="Takeoff only for player group", variable=self.takeoff_var).grid(row=2, column=0, columnspan=2)
        Checkbutton(self.frame, text="Disable night missions", variable=self.night_var).grid(row=3, column=0, columnspan=2)

        Button(self.frame, text="Back", command=self.dismiss).grid(row=4, column=0, columnspan=1)
        Button(self.frame, text="Cheat +200m", command=self.cheat_money).grid(row=5, column=0)

    def cheat_money(self):
        self.game.budget += 200
