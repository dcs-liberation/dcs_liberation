import webbrowser

from tkinter import *
from tkinter.ttk import *
from .styles import STYLES

from userdata.logging import ShowLogsException
from ui.window import *


class ConfigurationMenu(Menu):
    def __init__(self, window: Window, parent, game: Game):
        super(ConfigurationMenu, self).__init__(window, parent, game)
        self.frame = window.right_pane
        self.player_skill_var = StringVar()
        self.player_skill_var.set(self.game.settings.player_skill)

        self.enemy_skill_var = StringVar()
        self.enemy_skill_var.set(self.game.settings.enemy_skill)

        self.enemy_vehicle_var = StringVar()
        self.enemy_vehicle_var.set(self.game.settings.enemy_vehicle_skill)

        self.map_coalition_visibility_var = StringVar()
        self.map_coalition_visibility_var.set(self.game.settings.map_coalition_visibility)

        self.labels_var = StringVar()
        self.labels_var.set(self.game.settings.labels)

        self.takeoff_var = BooleanVar()
        self.takeoff_var.set(self.game.settings.only_player_takeoff)

        self.night_var = BooleanVar()
        self.night_var.set(self.game.settings.night_disabled)

        self.cold_start_var = BooleanVar()
        self.cold_start_var.set(self.game.settings.cold_start)

    def dismiss(self):
        self.game.settings.player_skill = self.player_skill_var.get()
        self.game.settings.enemy_skill = self.enemy_skill_var.get()
        self.game.settings.enemy_vehicle_skill = self.enemy_vehicle_var.get()
        self.game.settings.map_coalition_visibility = self.map_coalition_visibility_var.get()
        self.game.settings.labels = self.labels_var.get()
        self.game.settings.only_player_takeoff = self.takeoff_var.get()
        self.game.settings.night_disabled = self.night_var.get()
        self.game.settings.cold_start = self.cold_start_var.get()
        super(ConfigurationMenu, self).dismiss()

    def display(self):
        self.window.clear_right_pane()

        # Header
        head = Frame(self.frame, **STYLES["header"])
        head.grid(row=0, column=0, sticky=NSEW)
        head.grid_columnconfigure(0, weight=100)
        Label(head, text="Configuration", **STYLES["title"]).grid(row=0, sticky=W)
        Button(head, text="Back", command=self.dismiss, **STYLES["btn-primary"]).grid(row=0, column=1, sticky=E)

        # Body
        body = Frame(self.frame, **STYLES["body"])
        body.grid(row=1, column=0, sticky=NSEW)
        row = 0

        Label(body, text="Player coalition skill", **STYLES["widget"]).grid(row=row, column=0, sticky=W)
        p_skill = OptionMenu(body, self.player_skill_var, "Average", "Good", "High", "Excellent")
        p_skill.grid(row=row, column=1, sticky=E, pady=5)
        p_skill.configure(**STYLES["btn-primary"])
        row += 1

        Label(body, text="Enemy coalition skill", **STYLES["widget"]).grid(row=row, column=0, sticky=W)
        e_skill = OptionMenu(body, self.enemy_skill_var, "Average", "Good", "High", "Excellent")
        e_skill.grid(row=row, column=1, sticky=E)
        e_skill.configure(**STYLES["btn-primary"])
        row += 1

        Label(body, text="Enemy AA and vehicle skill", **STYLES["widget"]).grid(row=row, column=0, sticky=W)
        e_skill = OptionMenu(body, self.enemy_vehicle_var, "Average", "Good", "High", "Excellent")
        e_skill.grid(row=row, column=1, sticky=E)
        e_skill.configure(**STYLES["btn-primary"])
        row += 1

        Label(body, text="F10 Map Coalition Visibility", **STYLES["widget"]).grid(row=row, column=0, sticky=W)
        map_vis = OptionMenu(body, self.map_coalition_visibility_var, "All Units", "Allied Units", "Own Aircraft", "None")
        map_vis.grid(row=row, column=1, sticky=E)
        map_vis.configure(**STYLES["btn-primary"])
        row += 1

        Label(body, text="In Game Labels", **STYLES["widget"]).grid(row=row, column=0, sticky=W)
        g_labels = OptionMenu(body, self.labels_var, "Full", "Abbreviated", "Dot Only", "Off")
        g_labels.grid(row=row, column=1, sticky=E)
        g_labels.configure(**STYLES["btn-primary"])
        row += 1

        Label(body, text="Aircraft cold start", **STYLES["widget"]).grid(row=row, column=0, sticky=W)
        Checkbutton(body, variable=self.cold_start_var, **STYLES["radiobutton"]).grid(row=row, column=1, sticky=E)
        row += 1

        Label(body, text="Takeoff only for player group", **STYLES["widget"]).grid(row=row, column=0, sticky=W)
        Checkbutton(body, variable=self.takeoff_var, **STYLES["radiobutton"]).grid(row=row, column=1, sticky=E)
        row += 1

        Label(body, text="Disable night missions", **STYLES["widget"]).grid(row=row, column=0, sticky=W)
        Checkbutton(body, variable=self.night_var, **STYLES["radiobutton"]).grid(row=row, column=1, sticky=E)
        row += 1

        Label(body, text="Contributors: ", **STYLES["strong"]).grid(row=row, column=0, columnspan=2, sticky=EW)
        row += 1

        Label(body, text="shdwp - author, maintainer", **STYLES["widget"]).grid(row=row, column=0, sticky=W)
        Button(body, text="[github]", command=lambda: webbrowser.open_new_tab("http://github.com/shdwp"), **STYLES["widget"]).grid(row=row, column=1, sticky=E)
        row += 1

        Label(body, text="Khopa - contributions", **STYLES["widget"]).grid(row=row, column=0, sticky=W)
        Button(body, text="[github]", command=lambda: webbrowser.open_new_tab("http://github.com/Khopa"), **STYLES["widget"]).grid(row=row, column=1, sticky=E)
        row += 1

        Button(body, text="Display logs", command=self.display_logs, **STYLES["btn-primary"]).grid(row=row, column=0, pady=5)
        Button(body, text="Cheat +200m", command=self.cheat_money, **STYLES["btn-danger"]).grid(row=row, column=1)

    def display_logs(self):
        raise ShowLogsException()

    def cheat_money(self):
        self.game.budget += 200
