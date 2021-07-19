from collections import Iterator

from game.commander.tasks.primitive.bai import PlanBai
from game.commander.theaterstate import TheaterState
from game.htn import CompoundTask, Method


class AttackGarrisons(CompoundTask[TheaterState]):
    def each_valid_method(self, state: TheaterState) -> Iterator[Method[TheaterState]]:
        for garrisons in state.enemy_garrisons.values():
            for garrison in garrisons.in_priority_order:
                yield [PlanBai(garrison)]
