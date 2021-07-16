from collections import Iterator

from game.commander.tasks.primitive.strike import PlanStrike
from game.commander.theaterstate import TheaterState
from game.htn import CompoundTask, Method
from game.theater import TheaterGroundObject


class AttackBuildings(CompoundTask[TheaterState]):
    def each_valid_method(self, state: TheaterState) -> Iterator[Method[TheaterState]]:
        for building in state.strike_targets:
            assert isinstance(building, TheaterGroundObject)
            # Ammo depots are targeted based on the needs of the front line by
            # ReduceEnemyFrontLineCapacity. No reason to target them before that front
            # line is active.
            if not building.is_ammo_depot:
                yield [PlanStrike(building)]
