import pickle

from ui.basemenu import *
from ui.overviewcanvas import *

from game.game import *
from userdata import persistency


class MainMenu(Menu):
    basemenu = None  # type: BaseMenu

    def __init__(self, window: Window, parent, game: Game):
        super(MainMenu, self).__init__(window, parent, game)

        self.upd = OverviewCanvas(self.window.left_pane, self, game)
        self.upd.update()

        self.frame = self.window.right_pane
        self.frame.grid_columnconfigure(0, weight=1)

    def display(self):
        persistency.save_game(self.game)

        self.window.clear_right_pane()
        self.upd.update()
        row = 1

        def label(text):
            nonlocal row
            Label(self.frame, text=text).grid(row=row, sticky=NW)
            row += 1

        def event_button(event, text):
            nonlocal row
            Button(self.frame, text=text, command=self.start_event(event)).grid(row=row, sticky=N)
            row += 1

        Button(self.frame, text="Pass turn", command=self.pass_turn).grid(column=0, row=0, sticky=NE)
        Label(self.frame, text="Budget: {}m (+{}m)".format(self.game.budget, self.game.budget_reward_amount)).grid(column=0, row=0, sticky=NW)
        Separator(self.frame, orient='horizontal').grid(row=row, sticky=EW); row += 1

        for event in self.game.events:
            if not event.informational:
                continue

            label(str(event))

        for event in self.game.events:
            if event.informational:
                continue

            prefix = ""
            if event.attacker_name != self.game.player:
                prefix += "!"
            elif event.from_cp.is_global:
                prefix += "CARRIER"

            event_button(event, "{} {}".format(prefix, event))

    def pass_turn(self):
        self.game.pass_turn(no_action=True)
        self.display()

    def start_event(self, event) -> typing.Callable:
        return lambda: EventMenu(self.window, self, self.game, event).display()

    def go_cp(self, cp: ControlPoint):
        if self.basemenu:
            self.basemenu.dismiss()
            self.basemenu = None

        self.basemenu = BaseMenu(self.window, self, self.game, cp)
        self.basemenu.display()
