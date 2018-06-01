import math

from tkinter import *
from ui.window import *

from userdata.debriefing_parser import *
from game.game import *
from game import event


class EventResultsMenu:
    def __init__(self, window: Window, parent, game: Game, event: Event):
        self.window = window
        self.frame = window.right_pane
        self.parent = parent

        self.game = game
        self.event = event

        self.update()

    def simulate_result(self, player_factor: float, enemy_factor: float, result: bool):
        def action():
            debriefing = Debriefing()

            def count_planes(groups: typing.List[FlyingGroup], mult: float) -> typing.Dict[UnitType, int]:
                result = {}
                for group in groups:
                    for unit in group.units:
                        result[unit.type] = result.get(unit.type, 0) + 1 * mult

                return {x: math.floor(y) for x, y in result.items()}

            player_planes = self.event.operation.mission.country(self.game.player).plane_group
            enemy_planes = self.event.operation.mission.country(self.game.enemy).plane_group

            player_losses = count_planes(player_planes, player_factor)
            enemy_losses = count_planes(enemy_planes, enemy_factor)

            debriefing.destroyed_units = {
                self.game.player: player_losses,
                self.game.enemy: enemy_losses,
            }

            self.game.finish_event(self.event, debriefing)
            self.game.pass_turn()
            self.parent.update()

        return action

    def update(self):
        self.window.clear_right_pane()

        Button(self.frame, text="no losses, succ", command=self.simulate_result(0, 1, True)).grid(row=0, column=0)
        Button(self.frame, text="no losses, fail", command=self.simulate_result(0, 1, False)).grid(row=0, column=1)

        Button(self.frame, text="half losses, succ", command=self.simulate_result(0.5, 0.5, True)).grid(row=1, column=0)
        Button(self.frame, text="half losses, fail", command=self.simulate_result(0.5, 0.5, False)).grid(row=1, column=1)

        Button(self.frame, text="full losses, succ", command=self.simulate_result(1, 0, True)).grid(row=2, column=0)
        Button(self.frame, text="full losses, fail", command=self.simulate_result(1, 0, False)).grid(row=2, column=1)
