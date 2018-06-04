from shop import db

from tkinter import *
from ui.window import *
from ui.eventmenu import *

from game.game import *


class BaseMenu(Menu):
    def __init__(self, window: Window, parent, game: Game, cp: ControlPoint):
        super(BaseMenu, self).__init__(window, parent, game)

        self.cp = cp
        self.base = cp.base
        self.frame = window.right_pane
        self.event = self.game.units_delivery_event(cp)

    def display(self):
        self.window.clear_right_pane()
        row = 0

        def purchase_row(unit_type, unit_price):
            nonlocal row

            existing_units = self.base.total_units_of_type(unit_type)
            scheduled_units = self.event.units.get(unit_type, 0)

            Label(self.frame, text="{}".format(db.unit_type_name(unit_type))).grid(row=row, sticky=W)
            Label(self.frame, text="({})".format(existing_units)).grid(column=1, row=row)
            Label(self.frame, text="{}m {}".format(unit_price, scheduled_units and "(bought {})".format(scheduled_units) or "")).grid(column=2, row=row)
            Button(self.frame, text="Buy", command=self.buy(unit_type)).grid(column=3, row=row)
            Button(self.frame, text="Sell", command=self.sell(unit_type)).grid(column=4, row=row)
            row += 1

        units = {
            CAP: db.find_unittype(CAP, self.game.player),
            CAS: db.find_unittype(CAS, self.game.player),
            FighterSweep: db.find_unittype(FighterSweep, self.game.player),
            AirDefence: db.find_unittype(AirDefence, self.game.player),
        }

        Label(self.frame, text="Budget: {}m".format(self.game.budget)).grid(row=row, sticky=W)
        Button(self.frame, text="Back", command=self.dismiss).grid(column=2, row=row)
        row += 1

        for task_type, units in units.items():
            Label(self.frame, text="{}".format(db.task_name(task_type))).grid(row=row, columnspan=5); row += 1
            for unit_type in units:
                purchase_row(unit_type, db.PRICES[unit_type])

    def buy(self, unit_type):
        def action():
            price = db.PRICES[unit_type]
            if self.game.budget >= price:
                self.event.deliver({unit_type: 1})
                self.game.budget -= price

            self.display()

        return action

    def sell(self, unit_type):
        def action():
            if self.base.total_units_of_type(unit_type) > 0:
                price = db.PRICES[unit_type]
                self.game.budget += price
                self.base.commit_losses({unit_type: 1})
            self.display()

        return action