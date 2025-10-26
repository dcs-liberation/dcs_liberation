from datetime import datetime

from game.theater.controlpoint import Airfield
from game import Game
from .gameupdateevents import GameUpdateEvents


class ControlPointSimulation:
    def __init__(self, game: Game) -> None:
        self.game = game

    def on_game_tick(self, events: GameUpdateEvents, time: datetime) -> None:
        for control_point in self.game.theater.controlpoints:
            if not isinstance(control_point, Airfield):
                continue
            if not control_point.runway_is_operational():
                control_point.runway_status.update_repair_status(time)
                # If after repairing the runway is now operational, replan missions for both
                # blue and red and trigger a refresh of the React UI.
                if control_point.runway_is_operational():
                    self.game.blue.plan_missions(self.game.simulation_time)
                    self.game.red.plan_missions(self.game.simulation_time)
                    events.begin_new_turn()
