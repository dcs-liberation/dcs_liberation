import webbrowser

from tkinter import *
from tkinter.ttk import *
from .styles import STYLES

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

        self.cold_start_var = BooleanVar()
        self.cold_start_var.set(self.game.settings.cold_start)

    def dismiss(self):
        self.game.settings.player_skill = self.player_skill_var.get()
        self.game.settings.enemy_skill = self.enemy_skill_var.get()
        self.game.settings.only_player_takeoff = self.takeoff_var.get()
        self.game.settings.night_disabled = self.night_var.get()
        self.game.settings.cold_start = self.cold_start_var.get()
        super(ConfigurationMenu, self).dismiss()

    def display(self):
        self.window.clear_right_pane()

        # Header
        head = Frame(self.frame, **STYLES["header"])
        head.grid(row=0, column=0, columnspan=2, sticky=NSEW)
        Label(head, text="Configuration", **STYLES["title"]).grid()

        # Body
        body = Frame(self.frame, **STYLES["body"])
        body.grid(row=1, column=0, sticky=NSEW)

        Label(body, text="Player coalition skill", **STYLES["widget"]).grid(row=0, column=0, sticky=W)
        Label(body, text="Enemy coalition skill", **STYLES["widget"]).grid(row=1, column=0, sticky=W)

        p_skill = OptionMenu(body, self.player_skill_var, "Average", "Good", "High", "Excellent")
        p_skill.grid(row=0, column=1, sticky=E, pady=5)
        p_skill.configure(**STYLES["btn-primary"])

        e_skill = OptionMenu(body, self.enemy_skill_var, "Average", "Good", "High", "Excellent")
        e_skill.grid(row=1, column=1, sticky=E)
        e_skill.configure(**STYLES["btn-primary"])

        Label(body, text="Aircraft cold start", **STYLES["widget"]).grid(row=2, column=0, sticky=W)
        Label(body, text="Takeoff only for player group", **STYLES["widget"]).grid(row=3, column=0, sticky=W)
        Label(body, text="Disable night missions", **STYLES["widget"]).grid(row=4, column=0, sticky=W)

        Checkbutton(body, variable=self.cold_start_var, **STYLES["radiobutton"]).grid(row=2, column=1, sticky=E)
        Checkbutton(body, variable=self.takeoff_var, **STYLES["radiobutton"]).grid(row=3, column=1, sticky=E)
        Checkbutton(body, variable=self.night_var, **STYLES["radiobutton"]).grid(row=4, column=1, sticky=E)

        Button(body, text="Back", command=self.dismiss, **STYLES["btn-primary"]).grid(row=5, column=1, sticky=E, pady=30)

        Label(body, text="Contributors: ", **STYLES["widget"]).grid(row=6, column=0, sticky=W)

        Label(body, text="shdwp - author, maintainer", **STYLES["widget"]).grid(row=7, column=0, sticky=W)
        Button(body, text="[github]", command=lambda: webbrowser.open_new_tab("http://github.com/shdwp"), **STYLES["widget"]).grid(row=7, column=1, sticky=E)

        Label(body, text="Khopa - contributions", **STYLES["widget"]).grid(row=8, column=0, sticky=W)
        Button(body, text="[github]", command=lambda: webbrowser.open_new_tab("http://github.com/Khopa"), **STYLES["widget"]).grid(row=8, column=1, sticky=E)

        Button(body, text="Cheat +200m", command=self.cheat_money, **STYLES["btn-danger"]).grid(row=10, column=1, pady=30)

    def cheat_money(self):
        self.game.budget += 200
