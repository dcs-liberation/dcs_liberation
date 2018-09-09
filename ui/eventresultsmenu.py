from tkinter.ttk import *
from ui.window import *

from game.game import *
from userdata.debriefing import *
from .styles import STYLES


class EventResultsMenu(Menu):
    debriefing = None  # type: Debriefing
    player_losses = {}  # type: typing.Dict[UnitType, int]
    enemy_losses = {}  # type: typing.Dict[UnitType, int]

    def __init__(self, window: Window, parent, game: Game, event: Event):
        super(EventResultsMenu, self).__init__(window, parent, game)
        self.frame = window.right_pane
        self.frame.grid_rowconfigure(0, weight=0)
        self.event = event
        self.finished = False

        wait_for_debriefing(callback=self.process_debriefing)

    def display(self):
        self.window.clear_right_pane()

        row = 0

        def header(text, style="strong"):
            nonlocal row
            head = Frame(self.frame, **STYLES["header"])
            head.grid(row=row, column=0, sticky=N + EW, columnspan=2, pady=(0, 10))
            Label(head, text=text, **STYLES[style]).grid()
            row += 1

        def label(text, style="widget"):
            nonlocal row
            Label(self.frame, text=text, **STYLES[style]).grid(row=row, column=0, sticky=NW, columnspan=2)
            row += 1

        if not self.finished:

            header("You are clear for takeoff!")

            label("In DCS, open and play the mission:")
            label("liberation_nextturn", "italic")
            label("or")
            label("liberation_nextturn_quick", "italic")
            header("Then save the debriefing to the folder:")
            label(debriefing_directory_location(), "italic")
            header("Waiting for results...")

            pg = Progressbar(self.frame, orient="horizontal", length=200, mode="determinate")
            pg.grid(row=row, column=0, columnspan=2, sticky=EW, pady=5, padx=5)
            pg.start(10)
            row += 1

            Label(self.frame, text="Cheat operation results: ", **STYLES["strong"]).grid(column=0, row=row,
                                                                                         columnspan=2, sticky=NSEW,
                                                                                         pady=5)

            row += 1
            Button(self.frame, text="full enemy losses", command=self.simulate_result(0, 1),
                   **STYLES["btn-warning"]).grid(column=0, row=row, padx=5, pady=5)
            Button(self.frame, text="full player losses", command=self.simulate_result(1, 0),
                   **STYLES["btn-warning"]).grid(column=1, row=row, padx=5, pady=5)
            row += 1
            Button(self.frame, text="some enemy losses", command=self.simulate_result(0, 0.8),
                   **STYLES["btn-warning"]).grid(column=0, row=row, padx=5, pady=5)
            Button(self.frame, text="some player losses", command=self.simulate_result(0.8, 0),
                   **STYLES["btn-warning"]).grid(column=1, row=row, padx=5, pady=5)
            row += 1

        else:
            row = 0
            if self.event.is_successfull(self.debriefing):
                header("Operation success", "title-green")
            else:
                header("Operation failed", "title-red")

            header("Player losses")

            for unit_type, count in self.player_losses.items():
                Label(self.frame, text=db.unit_type_name(unit_type), **STYLES["widget"]).grid(row=row)
                Label(self.frame, text="{}".format(count), **STYLES["widget"]).grid(column=1, row=row)
                row += 1

            header("Enemy losses")

            if self.debriefing.destroyed_objects:
                Label(self.frame, text="Ground assets", **STYLES["widget"]).grid(row=row)
                Label(self.frame, text="{}".format(len(self.debriefing.destroyed_objects)), **STYLES["widget"]).grid(column=1, row=row)
                row += 1

            for unit_type, count in self.enemy_losses.items():
                if count == 0:
                    continue

                Label(self.frame, text=db.unit_type_name(unit_type), **STYLES["widget"]).grid(row=row)
                Label(self.frame, text="{}".format(count), **STYLES["widget"]).grid(column=1, row=row)
                row += 1

            Button(self.frame, text="Okay", command=self.dismiss, **STYLES["btn-primary"]).grid(columnspan=1, row=row);
            row += 1

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
            debriefing = Debriefing({}, [])

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

            destroyed_player_units = db.unitdict_restrict_count(alive_player_units, math.ceil(
                sum(alive_player_units.values()) * player_factor))
            destroyed_enemy_units = db.unitdict_restrict_count(alive_enemy_units, math.ceil(
                sum(alive_enemy_units.values()) * enemy_factor))

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
