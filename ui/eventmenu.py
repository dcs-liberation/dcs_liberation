from ui.eventresultsmenu import *

from game.game import *
from game import event, db


class EventMenu(Menu):
    aircraft_scramble_entries = None  # type: typing.Dict[PlaneType , Entry]
    aircraft_client_entries = None  # type: typing.Dict[PlaneType, Entry]
    armor_scramble_entries = None  # type: typing.Dict[VehicleType, Entry]
    awacs = None  # type: IntVar

    def __init__(self, window: Window, parent, game: Game, event: event.Event):
        super(EventMenu, self).__init__(window, parent, game)

        self.event = event
        self.aircraft_scramble_entries = {}
        self.armor_scramble_entries = {}
        self.aircraft_client_entries = {}

        if self.event.attacker_name == self.game.player:
            self.base = self.event.from_cp.base
        else:
            self.base = self.event.to_cp.base

        self.frame = self.window.right_pane
        self.awacs = IntVar()

    def display(self):
        self.window.clear_right_pane()
        row = 0

        def label(text, _row=None, _column=None, sticky=None):
            nonlocal row
            Label(self.frame, text=text).grid(row=_row and _row or row, column=_column and _column or 0, sticky=sticky)

            if _row is None:
                row += 1

        def scrable_row(unit_type, unit_count):
            nonlocal row
            Label(self.frame, text="{} ({})".format(db.unit_type_name(unit_type), unit_count)).grid(row=row, sticky=W)
            scramble_entry = Entry(self.frame, width=10)
            scramble_entry.grid(column=1, row=row)
            scramble_entry.insert(0, "0")
            self.aircraft_scramble_entries[unit_type] = scramble_entry

            client_entry = Entry(self.frame, width=10)
            client_entry.grid(column=2, row=row)
            client_entry.insert(0, "0")
            self.aircraft_client_entries[unit_type] = client_entry

            row += 1

        def scramble_armor_row(unit_type, unit_count):
            nonlocal row
            Label(self.frame, text="{} ({})".format(db.unit_type_name(unit_type), unit_count)).grid(row=row, sticky=W)
            scramble_entry = Entry(self.frame, width=10)
            scramble_entry.insert(0, "0")
            scramble_entry.grid(column=1, row=row)
            self.armor_scramble_entries[unit_type] = scramble_entry

            row += 1

        Button(self.frame, text="Commit", command=self.start).grid(column=1, row=row, sticky=E)
        Button(self.frame, text="Back", command=self.dismiss).grid(column=2, row=row, sticky=E)

        awacs_enabled = self.game.budget >= AWACS_BUDGET_COST and NORMAL or DISABLED
        Checkbutton(self.frame, text="AWACS ({}m)".format(AWACS_BUDGET_COST), var=self.awacs, state=awacs_enabled).grid(row=row, column=0, sticky=W)

        row += 1

        label("Aircraft")

        if self.base.aircraft:
            label("Amount", row, 1)
            label("Client slots", row, 2)
            row += 1

        for unit_type, count in self.base.aircraft.items():
            scrable_row(unit_type, count)

        if not self.base.total_planes:
            label("None", sticky=W)

        label("Armor")
        for unit_type, count in self.base.armor.items():
            scramble_armor_row(unit_type, count)

        if not self.base.total_armor:
            label("None", sticky=W)

    def start(self):
        if self.awacs.get() == 1:
            self.event.is_awacs_enabled = True
            self.game.awacs_expense_commit()
        else:
            self.event.is_awacs_enabled = False

        scrambled_aircraft = {}
        scrambled_sweep = {}
        scrambled_cas = {}
        for unit_type, field in self.aircraft_scramble_entries.items():
            value = field.get()
            if value and int(value) > 0:
                amount = min(int(value), self.base.aircraft[unit_type])
                task = db.unit_task(unit_type)

                scrambled_aircraft[unit_type] = amount
                if task == CAS:
                    scrambled_cas[unit_type] = amount
                elif task == FighterSweep:
                    scrambled_sweep[unit_type] = amount

        scrambled_clients = {}
        for unit_type, field in self.aircraft_client_entries.items():
            value = field.get()
            if value and int(value) > 0:
                amount = int(value)
                scrambled_clients[unit_type] = amount

        scrambled_armor = {}
        for unit_type, field in self.armor_scramble_entries.items():
            value = field.get()
            if value and int(value) > 0:
                scrambled_armor[unit_type] = int(value)

        if type(self.event) is CaptureEvent:
            e = self.event  # type: CaptureEvent
            if self.game.is_player_attack(self.event):
                e.player_attacking(cas=scrambled_cas,
                                   escort=scrambled_sweep,
                                   armor=scrambled_armor,
                                   clients=scrambled_clients)
            else:
                e.player_defending(interceptors=scrambled_aircraft,
                                   clients=scrambled_clients)
        elif type(self.event) is InterceptEvent:
            e = self.event  # type: InterceptEvent
            if self.game.is_player_attack(self.event):
                e.player_attacking(interceptors=scrambled_aircraft,
                                   clients=scrambled_clients)
            else:
                e.player_defending(escort=scrambled_aircraft,
                                   clients=scrambled_clients)
        elif type(self.event) is GroundInterceptEvent:
            e = self.event  # type: GroundInterceptEvent
            e.player_attacking(strikegroup=scrambled_aircraft, clients=scrambled_clients)

        self.game.initiate_event(self.event)
        EventResultsMenu(self.window, self.parent, self.game, self.event).display()

