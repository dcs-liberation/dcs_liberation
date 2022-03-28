import logging
from collections.abc import Iterator
from dataclasses import dataclass

from game.commander.tasks.compound.attackairinfrastructure import (
    AttackAirInfrastructure,
)
from game.commander.tasks.compound.attackbuildings import AttackBuildings
from game.commander.tasks.compound.attackgarrisons import AttackGarrisons
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

# FIXME: This is a hack for the dataclass to get around the fact that couldn't figure out how to import Game
class Game:
    pass


logger = logging.getLogger()


@dataclass(frozen=True)
class PlanNextAction(CompoundTask[TheaterState]):
    game: Game
    player: bool
    aircraft_cold_start: bool

    def each_valid_method(self, state: TheaterState) -> Iterator[Method[TheaterState]]:
        """The logic below suggests defense is priority, then checks whether or not there's an inbalance anywhere, like if lacking ground units, then create ground support missions, or if lacking air units, protect air space."""

        data = self.game.game_stats.data_per_turn[-1]

        air_ratio = data.allied_units.aircraft_count / data.enemy_units.aircraft_count
        ground_ratio = (
            data.allied_units.vehicles_count / data.enemy_units.vehicles_count
        )

        # if not player, inverse ratios for enemy
        if not self.player:
            air_ratio = 1 / air_ratio
        if not self.player:
            ground_ratio = 1 / ground_ratio

        logger.debug(f"player: {self.player}")
        logger.debug(f"air_ratio: {air_ratio}")
        logger.debug(f"ground_ratio: {ground_ratio}")

        # priority 1 - Theater Support
        yield [TheaterSupport()]
        logger.debug("1 - Theater Support")

        # priority 2 - Defend Bases
        defend_bases = False

        if ground_ratio < 0.8:  # outnumbered so prioritize defend base
            yield [DefendBases()]
            defend_bases = True
            logger.debug("2 - defend_bases")

        # priority 3 - Attack Opposer's Infrastructure and Protect Air Space
        protect_air_space = False
        attack_air_infrastructure = False

        if (
            air_ratio < 0.8
        ):  # outnumbered so prioritize air and try to surpress enemy air?
            yield [AttackAirInfrastructure(self.aircraft_cold_start)]  # maybe?
            yield [ProtectAirSpace()]
            protect_air_space = True
            attack_air_infrastructure = True
            logger.debug("3 - attack_air_infrastructure / protect_air_space")

        # priority 4 - Capture Opposer's Base(s)
        capture_base = False

        if ground_ratio > 1.4:  # advantage so prioritize capture base
            yield [CaptureBases()]
            capture_base = True
            logger.debug("4 - capture_base")

        # priority 5 - whatever we haven't done yet, but already checked for
        # still defend base, protect air, then capture base
        if not defend_bases:
            yield [DefendBases()]
            logger.debug("5.1 - defend_bases")

        if not protect_air_space:
            yield [ProtectAirSpace()]
            logger.debug("5.2 - protect_air_space")

        if not capture_base:
            yield [CaptureBases()]
            logger.debug("5.3 - capture_base")

        # priority 6 - the rest
        yield [InterdictReinforcements()]
        logger.debug("6.1 - interdict_reinforcements")
        yield [AttackGarrisons()]
        logger.debug("6.2 - attack_garrisons")

        if not attack_air_infrastructure:
            yield [AttackAirInfrastructure(self.aircraft_cold_start)]
            logger.debug("6.3 - attack_air_infrastructure")

        yield [AttackBuildings()]
        logger.debug("6.4 - attack_buildings")
        yield [DegradeIads()]
        logger.debug("6.5 - degrade_iads")
