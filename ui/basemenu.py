from shop import db

from tkinter import *
from ui.window import *
from ui.eventmenu import *

from game.game import *


class BaseMenu:
    def __init__(self, window: Window, parent, game: Game, base: Base):
        self.window = window
        self.frame = window.right_pane
        self.parent = parent
        self.game = game
        self.base = base

        self.update()

    def go_back(self):
        self.parent.update()

    def buy(self, unit_type):
        def action():
            price = db.PRICES[unit_type]
            if self.game.budget > price:
                self.base.commision_units({unit_type: 1})
                self.game.budget -= price

            self.update()

        return action

    def update(self):
        self.window.clear_right_pane()
        row = 0

        def purchase_row(unit_type, unit_price):
            nonlocal row

            existing_units = self.base.total_units_of_type(unit_type)
            Label(self.frame, text=db.unit_type_name(unit_type)).grid(column=0, row=row, sticky=W)
            Label(self.frame, text="{}m {}".format(unit_price, existing_units)).grid(column=1, row=row)
            Button(self.frame, text="Buy", command=self.buy(unit_type)).grid(column=2, row=row)
            row += 1

        units = {
            CAP: db.find_unittype(CAP, self.game.player),
            CAS: db.find_unittype(CAS, self.game.player),
            FighterSweep: db.find_unittype(FighterSweep, self.game.player),
            AirDefence: db.find_unittype(AirDefence, self.game.player),
        }

        Label(self.frame, text="Budget: {}m".format(self.game.budget)).grid(column=0, row=row, sticky=W)
        Button(self.frame, text="Back", command=self.go_back).grid(column=2, row=row)
        row += 1

        for task_type, units in units.items():
            Label(self.frame, text="{}".format(db.task_name(task_type))).grid(column=0, row=row, columnspan=3); row += 1
            for unit_type in units:
                purchase_row(unit_type, db.PRICES[unit_type])

