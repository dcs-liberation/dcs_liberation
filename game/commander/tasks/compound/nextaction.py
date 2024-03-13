from collections.abc import Iterator
from dataclasses import dataclass

from game.commander.tasks.compound.attackairinfrastructure import (
    AttackAirInfrastructure,
)
from game.commander.tasks.compound.attackbuildings import AttackBuildings
from game.commander.tasks.compound.attackbattlepositions import AttackBattlePositions
from game.commander.tasks.compound.capturebases import CaptureBases
from game.commander.tasks.compound.defendbases import DefendBases
from game.commander.tasks.compound.degradeiads import DegradeIads
from game.commander.tasks.compound.interdictreinforcements import (
    InterdictReinforcements,
)
from game.commander.tasks.compound.protectairspace import ProtectAirSpace
from game.commander.tasks.compound.theatersupport import TheaterSupport
from game.commander.theaterstate import TheaterState
from game.htn import CompoundTask, Method


@dataclass(frozen=True)
class PlanNextAction(CompoundTask[TheaterState]):
    aircraft_cold_start: bool

    def each_valid_method(self, state: TheaterState) -> Iterator[Method[TheaterState]]:
        yield [TheaterSupport()]
        yield [ProtectAirSpace()]
        yield [CaptureBases()]
        yield [DefendBases()]
        yield [InterdictReinforcements()]
        yield [AttackBattlePositions()]
        yield [AttackAirInfrastructure(self.aircraft_cold_start)]
        yield [AttackBuildings()]
        yield [DegradeIads()]
