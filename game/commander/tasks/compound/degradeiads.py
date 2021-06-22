from collections import Iterator

from game.commander.tasks.primitive.antiship import PlanAntiShip
from game.commander.tasks.primitive.dead import PlanDead
from game.commander.theaterstate import TheaterState
from game.htn import CompoundTask, Method
from game.theater.theatergroundobject import IadsGroundObject


class DegradeIads(CompoundTask[TheaterState]):
    def each_valid_method(self, state: TheaterState) -> Iterator[Method[TheaterState]]:
        for air_defense in state.threatening_air_defenses:
            if isinstance(air_defense, IadsGroundObject):
                yield [PlanDead(air_defense)]
            else:
                yield [PlanAntiShip(air_defense)]
