import pickle

from ui.basemenu import *
from ui.overviewcanvas import *
from ui.configurationmenu import *

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

        def event_button(event):
            nonlocal row
            Message(self.frame, text="{}{}".format(
                event.defender_name == self.game.player and "Enemy attacking: " or "",
                event
            ), aspect=800).grid(column=0, row=row, sticky=NW)
            Button(self.frame, text=">", command=self.start_event(event)).grid(column=0, row=row, sticky=NE+S)
            row += 1
            Separator(self.frame, orient='horizontal').grid(row=row, sticky=EW); row += 1

        Button(self.frame, text="Configuration", command=self.configuration_menu).grid(column=0, row=0, sticky=NE)
        Button(self.frame, text="Pass turn", command=self.pass_turn).grid(column=0, row=0, sticky=N)
        Label(self.frame, text="Budget: {}m (+{}m)".format(self.game.budget, self.game.budget_reward_amount)).grid(column=0, row=0, sticky=NW)
        Separator(self.frame, orient='horizontal').grid(row=row, sticky=EW); row += 1

        events = self.game.events
        events.sort(key=lambda x: x.informational and 2 or (self.game.is_player_attack(x) and 1 or 0))

        for event in events:
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
