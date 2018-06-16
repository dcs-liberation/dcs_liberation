from tkinter import *
from tkinter.ttk import *

from ui.window import *


class ConfigurationMenu(Menu):
    def __init__(self, window: Window, parent, game: Game):
        super(ConfigurationMenu, self).__init__(window, parent, game)
        self.frame = window.right_pane
        self.player_skill_var = StringVar()
        self.player_skill_var.set(self.game.player_skill)

        self.enemy_skill_var = StringVar()
        self.enemy_skill_var.set(self.game.enemy_skill)

    def dismiss(self):
        self.game.player_skill = self.player_skill_var.get()
        self.game.enemy_skill = self.enemy_skill_var.get()
        super(ConfigurationMenu, self).dismiss()

    def display(self):
        self.window.clear_right_pane()

        Label(self.frame, text="Player coalition skill").grid(row=0, column=0)
        Label(self.frame, text="Enemy coalition skill").grid(row=1, column=0)

        OptionMenu(self.frame, self.player_skill_var, "Average", "Good", "High", "Excellent").grid(row=0, column=1)
        OptionMenu(self.frame, self.enemy_skill_var, "Average", "Good", "High", "Excellent").grid(row=1, column=1)

        Button(self.frame, text="Back", command=self.dismiss).grid(row=2, column=0, columnspan=1)

