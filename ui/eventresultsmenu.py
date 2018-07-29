from tkinter.ttk import *
from ui.window import *

from game.game import *
from userdata.debriefing import *


class EventResultsMenu(Menu):
    debriefing = None  # type: Debriefing
    player_losses = {}  # type: typing.Dict[UnitType, int]
    enemy_losses = {}  # type: typing.Dict[UnitType, int]

    def __init__(self, window: Window, parent, game: Game, event: Event):
        super(EventResultsMenu, self).__init__(window, parent, game)
        self.frame = window.right_pane
        self.event = event
        self.finished = False

        wait_for_debriefing(callback=self.process_debriefing)

    def display(self):
        self.window.clear_right_pane()

        if not self.finished:
            Label(self.frame, text="Play the mission and save debriefing to").grid(row=0, column=0)
            Label(self.frame, text=debriefing_directory_location()).grid(row=1, column=0)

            """
            For debugging purposes
            """

            row = 3
            Separator(self.frame, orient=HORIZONTAL).grid(row=row, sticky=EW); row += 1
            Label(self.frame, text="Cheat operation results: ").grid(row=row); row += 1
            Button(self.frame, text="full enemy losses", command=self.simulate_result(0, 1)).grid(row=row); row += 1
            Button(self.frame, text="full player losses", command=self.simulate_result(1, 0)).grid(row=row); row += 1
            Button(self.frame, text="some enemy losses", command=self.simulate_result(0, 0.8)).grid(row=row); row += 1
            Button(self.frame, text="some player losses", command=self.simulate_result(0.8, 0)).grid(row=row); row += 1
        else:
            row = 0
            if self.event.is_successfull(self.debriefing):
                Label(self.frame, text="Operation success").grid(row=row, columnspan=1); row += 1
            else:
                Label(self.frame, text="Operation failed").grid(row=row, columnspan=1); row += 1

            Separator(self.frame, orient='horizontal').grid(row=row, columnspan=1, sticky=NE); row += 1
            Label(self.frame, text="Player losses").grid(row=row, columnspan=1); row += 1
            for unit_type, count in self.player_losses.items():
                Label(self.frame, text=db.unit_type_name(unit_type)).grid(row=row)
                Label(self.frame, text="{}".format(count)).grid(column=1, row=row)
                row += 1

            Separator(self.frame, orient='horizontal').grid(row=row, columnspan=1, sticky=NE); row += 1
            Label(self.frame, text="Enemy losses").grid(columnspan=1, row=row); row += 1
            for unit_type, count in self.enemy_losses.items():
                if count == 0:
                    continue

                Label(self.frame, text=db.unit_type_name(unit_type)).grid(row=row)
                Label(self.frame, text="{}".format(count)).grid(column=1, row=row)
                row += 1

            Button(self.frame, text="Okay", command=self.dismiss).grid(columnspan=1, row=row); row += 1

    def process_debriefing(self, debriefing: Debriefing):
        self.debriefing = debriefing
        debriefing.calculate_units(mission=self.event.operation.mission,
                                   player_name=self.game.player,
                                   enemy_name=self.game.enemy)

        self.game.finish_event(event=self.event, debriefing=debriefing)
        self.game.pass_turn(ignored_cps=[self.event.to_cp, ])

        self.finished = True
        self.player_losses = debriefing.destroyed_units.get(self.game.player, {})
        self.enemy_losses = debriefing.destroyed_units.get(self.game.enemy, {})
        self.display()

    def simulate_result(self, player_factor: float, enemy_factor: float):
        def action():
            debriefing = Debriefing({})

            def count(country: Country) -> typing.Dict[UnitType, int]:
                result = {}
                for g in country.plane_group + country.vehicle_group + country.helicopter_group + country.ship_group:
                    group = g  # type: Group
                    for unit in group.units:
                        unit_type = None
                        if isinstance(unit, Vehicle):
                            unit_type = vehicle_map[unit.type]
                        elif isinstance(unit, Ship):
                            unit_type = ship_map[unit.type]
                        else:
                            unit_type = unit.unit_type

                        if unit_type in db.EXTRA_AA.values():
                            continue

                        result[unit_type] = result.get(unit_type, 0) + 1

                return result

            player = self.event.operation.mission.country(self.game.player)
            enemy = self.event.operation.mission.country(self.game.enemy)

            alive_player_units = count(player)
            alive_enemy_units = count(enemy)

            destroyed_player_units = db.unitdict_restrict_count(alive_player_units, math.ceil(sum(alive_player_units.values()) * player_factor))
            destroyed_enemy_units = db.unitdict_restrict_count(alive_enemy_units, math.ceil(sum(alive_enemy_units.values()) * enemy_factor))

            alive_player_units = {k: v - destroyed_player_units.get(k, 0) for k, v in alive_player_units.items()}
            alive_enemy_units = {k: v - destroyed_enemy_units.get(k, 0) for k, v in alive_enemy_units.items()}

            debriefing.alive_units = {
                enemy.name: alive_enemy_units,
                player.name: alive_player_units,
            }

            debriefing.destroyed_units = {
                player.name: destroyed_player_units,
                enemy.name: destroyed_enemy_units,
            }

            self.finished = True
            self.debriefing = debriefing
            self.player_losses = debriefing.destroyed_units.get(self.game.player, {})
            self.enemy_losses = debriefing.destroyed_units.get(self.game.enemy, {})

            self.game.finish_event(self.event, debriefing)
            self.display()
            self.game.pass_turn()

        return action
