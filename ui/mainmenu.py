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
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

    def display(self):
        persistency.save_game(self.game)

        self.window.clear_right_pane()
        self.upd.update()
        row = 0

        # Header :
        header = Frame(self.frame, **STYLES["header"])
        Button(header, text="Configuration", command=self.configuration_menu, **STYLES["btn-primary"]).grid(column=0, row=0, sticky=NE)
        Label(header, text="Budget: {}m (+{}m)".format(self.game.budget, self.game.budget_reward_amount), **STYLES["strong"]).grid(column=1, row=0, sticky=NSEW, padx=50)
        Button(header, text="Pass turn", command=self.pass_turn, **STYLES["btn-primary"]).grid(column=2, row=0, sticky=NW)
        header.grid(column=0, row=0, sticky=N+EW)

        body = LabelFrame(self.frame, **STYLES["body"])
        body.grid(column=0, row=1, sticky=NSEW)

        def label(text):
            nonlocal row, body
            frame = LabelFrame(body, **STYLES["label-frame"])
            frame.grid(row=row, sticky=NSEW, columnspan=2)
            Label(frame, text=text, **STYLES["widget"]).grid(row=row, sticky=NS)
            row += 1

        def event_button(event):
            nonlocal row, body
            frame = LabelFrame(body, **STYLES["label-frame"])
            frame.grid(row=row, sticky=NSEW)
            Message(frame, text="{}{} at {}".format(
                event.defender_name == self.game.player and "Enemy attacking: " or "",
                event,
                event.to_cp,
            ), aspect=1600, **STYLES["widget"]).grid(column=0, row=0, sticky=NSEW)
            Button(body, text=">", command=self.start_event(event), **STYLES["btn-primary"]).grid(column=1, row=row, sticky=E)
            row += 1

        def destination_header(text, pady=0):
            nonlocal row, body
            Label(body, text=text, **STYLES["strong"]).grid(column=0, columnspan=2, row=row, sticky=N+EW, pady=(pady,0)); row += 1

        #Separator(self.frame, orient='horizontal').grid(row=row, sticky=EW); row += 1

        events = self.game.events
        events.sort(key=lambda x: x.from_cp.name)
        events.sort(key=lambda x: x.informational and 2 or (self.game.is_player_attack(x) and 1 or 0))

        destination = None
        deliveries = False
        for event in events:
            if not event.informational:
                if self.game.is_player_attack(event):
                    new_destination = event.from_cp.name
                else:
                    new_destination = "Enemy attack"
                if destination != new_destination:
                    destination_header(new_destination)
                    destination = new_destination

            if event.informational:
                if not deliveries:
                    deliveries = True
                    destination_header("Deliveries", 15)
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




