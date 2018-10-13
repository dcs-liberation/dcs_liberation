import os
from tkinter import *
from tkinter.ttk import *

from ui.window import *
from .styles import STYLES


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

        self.sams = BooleanVar()
        self.sams.set(1)

        self.multiplier = StringVar()
        self.multiplier.set("1")

        self.midgame = BooleanVar()
        self.midgame.set(0)

    @property
    def player_country_name(self):
        if self.selected_country.get() == 0:
            return "USA"
        else:
            return "Russia"

    @property
    def enemy_country_name(self):
        if self.selected_country.get() == 1:
            return "USA"
        else:
            return "Russia"

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

        # Country Selection
        country = LabelFrame(body, text="Player Side", **STYLES["label-frame"])
        country.grid(row=0, column=0, sticky=NW, padx=5)
        Radiobutton(country, variable=self.selected_country, value=0, **STYLES["radiobutton"]).grid(row=0, column=0,
                                                                                                    sticky=W)
        Label(country, text="USA", **STYLES["widget"]).grid(row=0, column=1, sticky=W)
        Radiobutton(country, variable=self.selected_country, value=1, **STYLES["radiobutton"]).grid(row=1, column=0,
                                                                                                    sticky=W)
        Label(country, text="Russia", **STYLES["widget"]).grid(row=1, column=1, sticky=W)

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

        # Misc Options
        options = LabelFrame(body, text="Misc Options", **STYLES["label-frame"])
        options.grid(row=0, column=2, sticky=NE, padx=5)

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
                      float(self.multiplier.get()))
