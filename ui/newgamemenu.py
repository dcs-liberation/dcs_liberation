import os
from tkinter import *
from tkinter.ttk import *

from ui.window import *
from .styles import STYLES
from game import db

class NewGameMenu(Menu):
    selected_country = None  # type: IntVar
    selected_terrain = None  # type: IntVar
    sams = None
    midgame = None
    multiplier = None

    def __init__(self, window: Window, callback: typing.Callable):
        super(NewGameMenu, self).__init__(window, None, None)
        self.frame = window.right_pane
        window.left_pane.configure(background="black")
        self.callback = callback

        self.selected_country = IntVar()
        self.selected_country.set(0)

        self.selected_terrain = IntVar()
        self.selected_terrain.set(0)

        self.selected_time_period = StringVar()

        self.selected_blue_faction = StringVar()
        self.selected_red_faction = StringVar()

        self.sams = BooleanVar()
        self.sams.set(1)

        self.multiplier = StringVar()
        self.multiplier.set("1")

        self.midgame = BooleanVar()
        self.midgame.set(0)

    @property
    def player_country_name(self):
        if self.selected_country.get() == 0:
            return self.selected_blue_faction.get()
        else:
            return self.selected_red_faction.get()

    @property
    def enemy_country_name(self):
        if self.selected_country.get() == 1:
            return self.selected_blue_faction.get()
        else:
            return self.selected_red_faction.get()

    @property
    def terrain_name(self) -> str:
        if self.selected_terrain.get() == 0:
            return "caucasus"
        elif self.selected_terrain.get() == 1:
            return "nevada"
        else:
            return "persiangulf"

    def display(self):
        self.window.clear_right_pane()

        # Header
        head = Frame(self.frame, **STYLES["header"])
        head.grid(row=0, column=0, sticky=NSEW)
        Label(head, text="Start a new game", **STYLES["title"]).grid()

        # Body
        body = Frame(self.frame, **STYLES["body"])
        body.grid(row=1, column=0, sticky=NSEW)

        # Side Selection
        side = LabelFrame(body, text="Player Side", **STYLES["label-frame"])
        side.grid(row=2, column=0, sticky=NW, padx=5)
        Radiobutton(side, variable=self.selected_country, value=0, **STYLES["radiobutton"]).grid(row=0, column=0,
                                                                                                    sticky=W)
        Label(side, text="BLUEFOR", **STYLES["widget"]).grid(row=0, column=1, sticky=W)
        Radiobutton(side, variable=self.selected_country, value=1, **STYLES["radiobutton"]).grid(row=1, column=0,
                                                                                                    sticky=W)
        Label(side, text="REDFOR", **STYLES["widget"]).grid(row=1, column=1, sticky=W)

        # Country Selection

        blues = [c for c in db.FACTIONS if db.FACTIONS[c]["side"] == "blue"]
        reds = [c for c in db.FACTIONS if db.FACTIONS[c]["side"] == "red"]

        factions = LabelFrame(body, text="Factions", **STYLES["label-frame"])
        factions.grid(row=0, column=0, sticky=NW, padx=5)

        Label(factions, text="Blue Faction", **STYLES["widget"]).grid(row=1, column=0, sticky=SE)

        self.selected_blue_faction.set(blues[0])
        blue_select = OptionMenu(factions, self.selected_blue_faction, *blues)
        blue_select.configure(**STYLES["btn-primary"])
        blue_select.grid(row=1, column=1, sticky=W)

        self.selected_red_faction.set(reds[1])
        Label(factions, text="Red Faction", **STYLES["widget"]).grid(row=2, column=0, sticky=W)
        red_select = OptionMenu(factions, self.selected_red_faction, *reds)
        red_select.configure(**STYLES["btn-primary"])
        red_select.grid(row=2, column=1, sticky=W)

        # Terrain Selection
        terrain = LabelFrame(body, text="Terrain", **STYLES["label-frame"])
        terrain.grid(row=0, column=1, sticky=N, padx=5)

        Radiobutton(terrain, variable=self.selected_terrain, value=0, **STYLES["radiobutton"]) \
            .grid(row=0, column=0, sticky=W)
        Label(terrain, text="Caucasus", **STYLES["widget"]).grid(row=0, column=1, sticky=W)
        self.create_label_image(terrain, "terrain_caucasus.gif").grid(row=0, column=2, padx=5)

        Radiobutton(terrain, variable=self.selected_terrain, value=1, **STYLES["radiobutton"]) \
            .grid(row=1, column=0, sticky=W)
        Label(terrain, text="Nevada", **STYLES["widget"]).grid(row=1, column=1, sticky=W)
        self.create_label_image(terrain, "terrain_nevada.gif").grid(row=1, column=2, padx=5)

        Radiobutton(terrain, variable=self.selected_terrain, value=2, **STYLES["radiobutton"]) \
            .grid(row=2, column=0, sticky=W)
        Label(terrain, text="Persian Gulf", **STYLES["widget"]).grid(row=2, column=1, sticky=W)
        self.create_label_image(terrain, "terrain_pg.gif").grid(row=2, column=2, padx=5)

        # Period selection
        period = LabelFrame(body, text="Time Period", **STYLES["label-frame"])
        period.grid(row=0, column=2, sticky=N, padx=5)

        vals = list(db.TIME_PERIODS)
        self.selected_time_period.set(vals[21])
        period_select = OptionMenu(period, self.selected_time_period, *vals)
        period_select.configure(**STYLES["btn-primary"])
        period_select.grid(row=0, column=0, sticky=W)
        #Label(terrain, text="Caucasus", **STYLES["widget"]).grid(row=0, column=1, sticky=W)

        # Misc Options
        options = LabelFrame(body, text="Misc Options", **STYLES["label-frame"])
        options.grid(row=0, column=3, sticky=NE, padx=5)

        Checkbutton(options, variable=self.sams, **STYLES["radiobutton"]).grid(row=0, column=0, sticky=W)
        Label(options, text="SAMs", **STYLES["widget"]).grid(row=0, column=1, sticky=W)

        Checkbutton(options, variable=self.midgame, **STYLES["radiobutton"]).grid(row=1, column=0, sticky=W)
        Label(options, text="Mid Game", **STYLES["widget"]).grid(row=1, column=1, sticky=W)

        Label(options, text="Multiplier", **STYLES["widget"]).grid(row=2, column=0, sticky=W)
        Entry(options, textvariable=self.multiplier).grid(row=2, column=1, sticky=W)

        # Footer with Proceed Button
        footer = Frame(self.frame, **STYLES["header"])
        footer.grid(row=2, sticky=N + E + W)
        Button(footer, text="Proceed", command=self.proceed, **STYLES["btn-primary"]).grid(row=0, column=0, sticky=SE,
                                                                                           padx=5, pady=5)

    @staticmethod
    def create_label_image(parent, image):
        im = PhotoImage(file=os.path.join("resources", "ui", image))
        label = Label(parent, image=im)
        label.image = im
        return label

    def proceed(self):
        self.callback(self.player_country_name,
                      self.enemy_country_name,
                      self.terrain_name,
                      bool(self.sams.get()),
                      bool(self.midgame.get()),
                      float(self.multiplier.get()),
                      db.TIME_PERIODS[self.selected_time_period.get()])
