from collections.abc import Iterator
from dataclasses import dataclass

from game.commander.tasks.compound.destroyenemygroundunits import (
    DestroyEnemyGroundUnits,
)
from game.commander.tasks.compound.reduceenemyfrontlinecapacity import (
    ReduceEnemyFrontLineCapacity,
)
from game.commander.tasks.primitive.breakthroughattack import BreakthroughAttack
from game.commander.theaterstate import TheaterState
from game.htn import CompoundTask, Method
from game.theater import ControlPoint, FrontLine


@dataclass(frozen=True)
class CaptureBase(CompoundTask[TheaterState]):
    front_line: FrontLine

    def each_valid_method(self, state: TheaterState) -> Iterator[Method[TheaterState]]:
        yield [BreakthroughAttack(self.front_line, state.context.coalition.player)]
        yield [DestroyEnemyGroundUnits(self.front_line)]
        if self.worth_destroying_ammo_depots(state):
            yield [ReduceEnemyFrontLineCapacity(self.enemy_cp(state))]

    def enemy_cp(self, state: TheaterState) -> ControlPoint:
        return self.front_line.control_point_hostile_to(state.context.coalition.player)

    def units_deployable(self, state: TheaterState, player: bool) -> int:
        cp = self.front_line.control_point_friendly_to(player)
        ammo_depots = list(state.ammo_dumps_at(cp))
        return cp.deployable_front_line_units_with(len(ammo_depots))

    def unit_cap(self, state: TheaterState, player: bool) -> int:
        cp = self.front_line.control_point_friendly_to(player)
        ammo_depots = list(state.ammo_dumps_at(cp))
        return cp.front_line_capacity_with(len(ammo_depots))

    def enemy_has_ammo_dumps(self, state: TheaterState) -> bool:
        return bool(state.ammo_dumps_at(self.enemy_cp(state)))

    def worth_destroying_ammo_depots(self, state: TheaterState) -> bool:
        if not self.enemy_has_ammo_dumps(state):
            return False

        friendly_cap = self.unit_cap(state, state.context.coalition.player)
        enemy_deployable = self.units_deployable(state, state.context.coalition.player)

        # If the enemy can currently deploy 50% more units than we possibly could, it's
        # worth killing an ammo depot.
        return enemy_deployable / friendly_cap > 1.5
