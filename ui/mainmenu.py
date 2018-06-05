from tkinter import *
from tkinter.ttk import *

from ui.window import *
from ui.eventmenu import *
from ui.basemenu import *

from game.game import *


class MainMenu(Menu):
    def __init__(self, window: Window, parent, game: Game):
        super(MainMenu, self).__init__(window, parent, game)

        self.image = PhotoImage(file="resources/caumap.gif")
        map = Label(window.left_pane, image=self.image)
        map.grid()

        self.frame = self.window.right_pane
        self.frame.grid_columnconfigure(0, weight=1)

    def display(self):
        self.window.clear_right_pane()

        row = 1

        def label(text):
            nonlocal row
            Label(self.frame, text=text).grid(row=row, sticky=NW)
            row += 1

        def event_button(event, text):
            nonlocal row
            Button(self.frame, text=text, command=self.start_event(event)).grid(row=row, sticky=N)
            row += 1

        def cp_button(cp):
            nonlocal row
            title = "{}{}{}{}".format(
                cp.name,
                "^" * cp.base.total_planes,
                "." * cp.base.total_armor,
                "*" * cp.base.total_aa)
            Button(self.frame, text=title, command=self.go_cp(cp)).grid(row=row, sticky=NW)
            row += 1

        Label(self.frame, text="Budget: {}m".format(self.game.budget)).grid(column=0, row=0, sticky=NW)
        Button(self.frame, text="Pass turn", command=self.pass_turn).grid(column=1, row=0, sticky=NE)
        row += 1

        for event in self.game.events:
            if not event.informational:
                continue
            label(str(event))

        for event in self.game.events:
            if event.informational:
                continue

            event_button(event, "{} {}".format(event.attacker.name != self.game.player and "!" or " ", event))

        Separator(self.frame, orient='horizontal').grid(row=row, sticky=EW); row += 1
        for cp in self.game.theater.player_points():
            cp_button(cp)

        Separator(self.frame, orient='horizontal').grid(row=row, sticky=EW); row += 1
        for cp in self.game.theater.enemy_bases():
            title = "[{}] {}{}{}{}".format(
                int(cp.base.strength * 10),
                cp.name,
                "^" * cp.base.total_planes,
                "." * cp.base.total_armor,
                "*" * cp.base.total_aa)
            Label(self.frame, text=title).grid(row=row, sticky=NE)
            row += 1

    def pass_turn(self):
        self.game.pass_turn(no_action=True)
        self.display()

    def start_event(self, event) -> typing.Callable:
        return lambda: EventMenu(self.window, self, self.game, event).display()

    def go_cp(self, cp: ControlPoint) -> typing.Callable:
        return lambda: BaseMenu(self.window, self, self.game, cp).display()
