from ui.eventmenu import *

from game.game import *
from .styles import STYLES


class BaseMenu(Menu):
    bought_amount_labels = None  # type: typing.Collection[Label]
    budget_label = None  # type: Label

    def __init__(self, window: Window, parent, game: Game, cp: ControlPoint):
        super(BaseMenu, self).__init__(window, parent, game)
        self.cp = cp
        self.base = cp.base
        self.frame = window.right_pane
        self.event = self.game.units_delivery_event(cp)
        self.bought_amount_labels = {}

    def display(self):
        self.window.clear_right_pane()
        units = {
            CAP: db.find_unittype(CAP, self.game.player_name),
            Embarking: db.find_unittype(Embarking, self.game.player_name),
            AirDefence: db.find_unittype(AirDefence, self.game.player_name),
            CAS: db.find_unittype(CAS, self.game.player_name),
            PinpointStrike: db.find_unittype(PinpointStrike, self.game.player_name),
        }

        # Header
        head = Frame(self.frame, **STYLES["header"])
        head.grid(row=0, column=0, columnspan=99, sticky=NSEW, pady=5)
        Label(head, text=self.cp.name, **STYLES["title"]).grid(row=0, column=0, sticky=NW+S)
        units_title = "{}/{}/{}".format(self.cp.base.total_planes, self.cp.base.total_armor, self.cp.base.total_aa)
        Label(head, text=units_title, **STYLES["strong-grey"]).grid(row=0, column=1, sticky=NE+S)

        self.budget_label = Label(self.frame, text="Budget: {}m".format(self.game.budget), **STYLES["widget"])
        self.budget_label.grid(row=1, sticky=W)
        Button(self.frame, text="Back", command=self.dismiss, **STYLES["btn-primary"]).grid(column=9, row=1, padx=(0,15), pady=(0,5))

        tasks = list(units.keys())
        tasks_per_column = 3

        column = 0
        for i, tasks_column in [(i, tasks[idx:idx+tasks_per_column]) for i, idx in enumerate(range(0, len(tasks), tasks_per_column))]:
            row = 2

            def purchase_row(unit_type, unit_price):
                nonlocal row
                nonlocal column

                existing_units = self.base.total_units_of_type(unit_type)
                scheduled_units = self.event.units.get(unit_type, 0)

                Label(self.frame, text="{}".format(db.unit_type_name(unit_type)), **STYLES["widget"]).grid(row=row, column=column, sticky=W)

                label = Label(self.frame, text="({})               ".format(existing_units), **STYLES["widget"])
                label.grid(column=column + 1, row=row)
                self.bought_amount_labels[unit_type] = label

                Label(self.frame, text="{}m".format(unit_price), **STYLES["widget"]).grid(column=column + 2, row=row, sticky=E)
                Button(self.frame, text="+", command=self.buy(unit_type), **STYLES["btn-primary"]).grid(column=column + 3, row=row, padx=(10,0))
                Button(self.frame, text="-", command=self.sell(unit_type), **STYLES["btn-warning"]).grid(column=column + 4, row=row, padx=(10,5))
                row += 1

            for task_type in tasks_column:
                Label(self.frame, text="{}".format(db.task_name(task_type)), **STYLES["strong"]).grid(row=row, column=column, columnspan=5, sticky=NSEW)
                row += 1

                units_column = list(set(units[task_type]))
                units_column.sort(key=lambda x: db.PRICES[x])
                for unit_type in units_column:
                    purchase_row(unit_type, db.PRICES[unit_type])

            column += 5

    def dismiss(self):
        if sum([x for x in self.event.units.values()]) == 0:
            self.game.units_delivery_remove(self.event)

        super(BaseMenu, self).dismiss()

    def _update_count_label(self, unit_type: UnitType):
        self.bought_amount_labels[unit_type]["text"] = "({}{})".format(
            self.cp.base.total_units_of_type(unit_type),
            unit_type in self.event.units and ", bought {}".format(self.event.units[unit_type]) or ""
        )

        self.budget_label["text"] = "Budget: {}m".format(self.game.budget)

    def buy(self, unit_type):
        def action():
            price = db.PRICES[unit_type]
            if self.game.budget >= price:
                self.event.deliver({unit_type: 1})
                self.game.budget -= price

            self._update_count_label(unit_type)

        return action

    def sell(self, unit_type):
        def action():
            if self.event.units.get(unit_type, 0) > 0:
                price = db.PRICES[unit_type]
                self.game.budget += price
                self.event.units[unit_type] = self.event.units[unit_type] - 1
                if self.event.units[unit_type] == 0:
                    del self.event.units[unit_type]
            elif self.base.total_units_of_type(unit_type) > 0:
                price = db.PRICES[unit_type]
                self.game.budget += price
                self.base.commit_losses({unit_type: 1})

            self._update_count_label(unit_type)

        return action