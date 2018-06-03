from tkinter import *
from ui.window import *
from ui.eventresultsmenu import *

from game.game import *
from game import event


class EventMenu(Menu):
    aircraft_scramble_entries = None  # type: typing.Dict[PlaneType, Entry]
    armor_scramble_entries = None  # type: typing.Dict[Armor, Entry]

    def __init__(self, window: Window, parent, game: Game, event: event.Event):
        super(EventMenu, self).__init__(window, parent, game)

        self.event = event
        self.aircraft_scramble_entries = {}
        self.armor_scramble_entries = {}

        self.frame = self.window.right_pane

    def display(self):
        self.window.clear_right_pane()
        row = 0

        def label(text):
            nonlocal row
            Label(self.frame, text=text).grid(column=0, row=0)

            row += 1

        def scrable_row(unit_type, unit_count):
            nonlocal row
            Label(self.frame, text="{} ({})".format(unit_type.id and unit_type.id or unit_type.name, unit_count)).grid(column=0, row=row)
            e = Entry(self.frame)
            e.grid(column=1, row=row)

            self.aircraft_scramble_entries[unit_type] = e
            row += 1

        base = None  # type: Base
        if self.event.attacker.name == self.game.player:
            base = self.event.from_cp.base
        else:
            base = self.event.to_cp.base

        label("Aircraft")
        for unit_type, count in base.aircraft.items():
            scrable_row(unit_type, count)

        Button(self.frame, text="Commit", command=self.start).grid(column=0, row=row)
        Button(self.frame, text="Back", command=self.dismiss).grid(column=0, row=row)

    def start(self):
        scrambled_aircraft = {}
        scrambled_sweep = {}
        scrambled_cas = {}
        for unit_type, field in self.aircraft_scramble_entries.items():
            value = field.get()
            if value and int(value) > 0:
                amount = int(value)
                task = db.unit_task(unit_type)

                scrambled_aircraft[unit_type] = amount
                if task == CAS:
                    scrambled_cas[unit_type] = amount
                elif task == FighterSweep:
                    scrambled_sweep[unit_type] = amount

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
                                   armor=scrambled_armor)
            else:
                e.player_defending(interceptors=scrambled_aircraft)
        elif type(self.event) is InterceptEvent:
            e = self.event  # type: InterceptEvent
            if self.game.is_player_attack(self.event):
                e.player_attacking(interceptors=scrambled_aircraft)
            else:
                e.player_defending(escort=scrambled_aircraft)
        elif type(self.event) is GroundInterceptEvent:
            e = self.event  # type: GroundInterceptEvent
            e.player_attacking(e.to_cp.position.random_point_within(30000), strikegroup=scrambled_aircraft)

        self.game.initiate_event(self.event)
        EventResultsMenu(self.window, self.parent, self.game, self.event).display()

