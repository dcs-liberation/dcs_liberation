from collections import Iterator
from dataclasses import dataclass

from game.commander.tasks.compound.aewcsupport import PlanAewcSupport
from game.commander.tasks.compound.attackairinfrastructure import (
    AttackAirInfrastructure,
)
from game.commander.tasks.compound.attackbuildings import AttackBuildings
from game.commander.tasks.compound.attackgarrisons import AttackGarrisons
from game.commander.tasks.compound.degradeiads import DegradeIads
from game.commander.tasks.compound.destroyships import DestroyShips
from game.commander.tasks.compound.frontlinedefense import FrontLineDefense
from game.commander.tasks.compound.interdictreinforcements import (
    InterdictReinforcements,
)
from game.commander.tasks.compound.protectairspace import ProtectAirSpace
from game.commander.tasks.compound.refuelingsupport import PlanRefuelingSupport
from game.commander.theaterstate import TheaterState
from game.htn import CompoundTask, Method


@dataclass(frozen=True)
class PlanNextAction(CompoundTask[TheaterState]):
    aircraft_cold_start: bool

    def each_valid_method(self, state: TheaterState) -> Iterator[Method[TheaterState]]:
        yield [PlanAewcSupport()]
        yield [PlanRefuelingSupport()]
        yield [ProtectAirSpace()]
        yield [FrontLineDefense()]
        yield [DegradeIads()]
        yield [InterdictReinforcements()]
        yield [DestroyShips()]
        yield [AttackGarrisons()]
        yield [AttackAirInfrastructure(self.aircraft_cold_start)]
        yield [AttackBuildings()]
