from tkinter import *
from tkinter.ttk import *

from ui.window import *
from ui.eventmenu import *
from ui.basemenu import *

from game.game import *

class MainMenu:
    def __init__(self, game: Game, window: Window):
        self.image = PhotoImage(file="resources/caumap.gif")
        self.game = game
        self.window = window

        map = Label(window.left_pane, image=self.image)
        map.grid(column=0, row=0)

        self.frame = self.window.right_pane
        self.frame.grid_columnconfigure(0, weight=1)
        self.update()

    def pass_turn(self):
        self.game.pass_turn()
        self.update()

    def start_event(self, event) -> typing.Callable:
        return lambda: EventMenu(self.window, self, self.game, event)

    def go_cp(self, cp: ControlPoint) -> typing.Callable:
        return lambda: BaseMenu(self.window, self, self.game, cp.base)

    def update(self):
        self.window.clear_right_pane()

        row = 1

        def label(text):
            nonlocal row
            Label(self.frame, text=text).grid(column=0, row=row, sticky=NW)
            row += 1

        def event_button(event, text):
            nonlocal row
            Button(self.frame, text=text, command=self.start_event(event)).grid(column=0, row=row, sticky=N)
            row += 1

        def cp_button(cp):
            nonlocal row
            title = "{}{}{}{}".format(
                cp.name,
                "^" * cp.base.total_planes,
                "." * cp.base.total_armor,
                "*" * cp.base.total_aa)
            Button(self.frame, text=title, command=self.go_cp(cp)).grid(column=0, row=row, sticky=NW)
            row += 1

        Button(self.frame, text="Pass turn", command=self.pass_turn).grid(column=0, row=row, sticky=N); row += 1
        label("Budget: {}m".format(self.game.budget))

        for event in self.game.events:
            event_button(event, "{} {}".format(event.attacker.name != self.game.player and "!" or " ", event))

        Separator(self.frame, orient='horizontal').grid(column=0, row=row, sticky=EW); row += 1
        for cp in self.game.theater.player_points():
            cp_button(cp)

        Separator(self.frame, orient='horizontal').grid(column=0, row=row, sticky=EW); row += 1
        for cp in self.game.theater.enemy_bases():
            title = "[{}] {}{}{}{}".format(
                int(cp.base.strength * 10),
                cp.name,
                "^" * cp.base.total_planes,
                "." * cp.base.total_armor,
                "*" * cp.base.total_aa)
            Label(self.frame, text=title).grid(column=0, row=row, sticky=NE)
            row += 1

