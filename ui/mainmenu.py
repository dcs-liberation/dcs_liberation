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

        # Header :
        header = Frame(self.frame, **STYLES["header"])
        Button(header, text="Configuration", command=self.configuration_menu, **STYLES["btn-primary"]).grid(column=0, row=0, sticky=NW)
        Label(header, text="Budget: {}m (+{}m)".format(self.game.budget, self.game.budget_reward_amount), **STYLES["strong"]).grid(column=1, row=0, sticky=N+EW, padx=50)
        Button(header, text="Pass turn", command=self.pass_turn, **STYLES["btn-primary"]).grid(column=2, row=0, sticky=NE)
        header.grid(column=0, row=0, sticky=N+EW)

        content = Frame(self.frame, **STYLES["body"])
        content.grid(column=0, row=1, sticky=NSEW)
        column = 0
        row = 0

        def label(text):
            nonlocal row, body
            frame = LabelFrame(body, **STYLES["label-frame"])
            frame.grid(row=row, sticky=N+EW, columnspan=2)
            Label(frame, text=text, **STYLES["widget"]).grid(row=row, sticky=NS)
            row += 1

        def event_button(event):
            nonlocal row, body
            frame = LabelFrame(body, **STYLES["label-frame"])
            frame.grid(row=row, sticky=N+EW)
            Message(frame, text="{}".format(
                event
            ), aspect=1600, **STYLES["widget"]).grid(column=0, row=0, sticky=N+EW)
            Button(body, text=">", command=self.start_event(event), **STYLES["btn-primary"]).grid(column=1, row=row, sticky=E)
            row += 1

        def departure_header(text, style="strong"):
            nonlocal row, body
            Label(body, text=text, **STYLES[style]).grid(column=0, columnspan=2, row=row, sticky=N+EW, pady=(0, 5))
            row += 1

        def destination_header(text):
            nonlocal row, body
            Label(body, text=text, **STYLES["substrong"]).grid(column=0, columnspan=2, row=row, sticky=N+EW)
            row += 1

        events = self.game.events
        events.sort(key=lambda x: x.to_cp.name)
        events.sort(key=lambda x: x.from_cp.name)
        events.sort(key=lambda x: x.informational and 1 or (self.game.is_player_attack(x) and 2 or 0))

        destination = None
        departure = None

        for event in events:
            if event.informational:
                new_departure = "Deliveries"
            elif not self.game.is_player_attack(event):
                new_departure = "Enemy attack"
            else:
                new_departure = event.from_cp.name

            if new_departure != departure:
                body = Frame(content, **STYLES["body"])
                body.grid(column=column, row=1, sticky=N+EW)
                row = 0
                column += 1

                departure = new_departure
                departure_header(new_departure, style="strong" if self.game.is_player_attack(event) else "supstrong")
                destination = None

            if not event.informational:
                new_destination = "At {}".format(event.to_cp.name)
                if destination != new_destination:
                    destination_header(new_destination)
                    destination = new_destination

            if event.informational:
                label(str(event))
            else:
                event_button(event)

    def pass_turn(self):
        self.game.pass_turn(no_action=True)
        self.display()

    def configuration_menu(self):
        ConfigurationMenu(self.window, self, self.game).display()

    def start_event(self, event) -> typing.Callable:
        return lambda: EventMenu(self.window, self, self.game, event).display()

    def go_cp(self, cp: ControlPoint):
        if not cp.captured:
            return

        if self.basemenu:
            self.basemenu.dismiss()
            self.basemenu = None

        self.basemenu = BaseMenu(self.window, self, self.game, cp)
        self.basemenu.display()




