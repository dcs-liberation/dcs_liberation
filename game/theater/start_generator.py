from __future__ import annotations

import logging
import random
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

import dcs.statics

from game import Game
from game.factions.faction import Faction
from game.scenery_group import SceneryGroup
from game.theater import PointWithHeading
from game.theater.theatergroundobject import (
    BuildingGroundObject,
)
from .theatergroup import SceneryUnit, TheaterGroup
from game.utils import Heading
from game.version import VERSION
from gen.naming import namegen
from . import (
    ConflictTheater,
    ControlPoint,
    ControlPointType,
    Fob,
    OffMapSpawn,
)
from ..campaignloader.campaignairwingconfig import CampaignAirWingConfig
from ..data.groups import GroupRole, GroupTask
from ..armedforces.forcegroup import ForceGroup
from ..armedforces.armedforces import ArmedForces
from ..profiling import logged_duration
from ..settings import Settings


@dataclass(frozen=True)
class GeneratorSettings:
    start_date: datetime
    player_budget: int
    enemy_budget: int
    inverted: bool
    no_carrier: bool
    no_lha: bool
    no_player_navy: bool
    no_enemy_navy: bool


@dataclass
class ModSettings:
    a4_skyhawk: bool = False
    f22_raptor: bool = False
    f104_starfighter: bool = False
    hercules: bool = False
    uh_60l: bool = False
    jas39_gripen: bool = False
    su57_felon: bool = False
    frenchpack: bool = False
    high_digit_sams: bool = False


class GameGenerator:
    def __init__(
        self,
        player: Faction,
        enemy: Faction,
        theater: ConflictTheater,
        air_wing_config: CampaignAirWingConfig,
        settings: Settings,
        generator_settings: GeneratorSettings,
        mod_settings: ModSettings,
    ) -> None:
        self.player = player
        self.enemy = enemy
        self.theater = theater
        self.air_wing_config = air_wing_config
        self.settings = settings
        self.generator_settings = generator_settings
        self.player.apply_mod_settings(mod_settings)
        self.enemy.apply_mod_settings(mod_settings)

    def generate(self) -> Game:
        with logged_duration("TGO population"):
            # Reset name generator
            namegen.reset()
            self.prepare_theater()
            game = Game(
                player_faction=self.player,
                enemy_faction=self.enemy,
                theater=self.theater,
                air_wing_config=self.air_wing_config,
                start_date=self.generator_settings.start_date,
                settings=self.settings,
                player_budget=self.generator_settings.player_budget,
                enemy_budget=self.generator_settings.enemy_budget,
            )

            GroundObjectGenerator(game, self.generator_settings).generate()
        game.settings.version = VERSION
        return game

    def should_remove_carrier(self, player: bool) -> bool:
        faction = self.player if player else self.enemy
        return self.generator_settings.no_carrier or not faction.carrier_names

    def should_remove_lha(self, player: bool) -> bool:
        faction = self.player if player else self.enemy
        return self.generator_settings.no_lha or not faction.helicopter_carrier_names

    def prepare_theater(self) -> None:
        to_remove: List[ControlPoint] = []

        # Remove carrier and lha, invert situation if needed
        for cp in self.theater.controlpoints:
            if self.generator_settings.inverted:
                cp.starts_blue = cp.captured_invert

            if cp.is_carrier and self.should_remove_carrier(cp.starts_blue):
                to_remove.append(cp)
            elif cp.is_lha and self.should_remove_lha(cp.starts_blue):
                to_remove.append(cp)

        # do remove
        for cp in to_remove:
            self.theater.controlpoints.remove(cp)


class ControlPointGroundObjectGenerator:
    def __init__(
        self,
        game: Game,
        generator_settings: GeneratorSettings,
        control_point: ControlPoint,
    ) -> None:
        self.game = game
        self.generator_settings = generator_settings
        self.control_point = control_point

    @property
    def faction_name(self) -> str:
        return self.faction.name

    @property
    def faction(self) -> Faction:
        return self.game.coalition_for(self.control_point.captured).faction

    @property
    def armed_forces(self) -> ArmedForces:
        return self.game.coalition_for(self.control_point.captured).armed_forces

    def generate(self) -> bool:
        self.control_point.connected_objectives = []
        self.generate_navy()
        return True

    def generate_ground_object_from_group(
        self, unit_group: ForceGroup, position: PointWithHeading
    ) -> None:
        ground_object = unit_group.generate(
            namegen.random_objective_name(),
            position,
            self.control_point,
            self.game,
        )
        self.control_point.connected_objectives.append(ground_object)

    def generate_navy(self) -> None:
        skip_player_navy = self.generator_settings.no_player_navy
        if self.control_point.captured and skip_player_navy:
            return
        skip_enemy_navy = self.generator_settings.no_enemy_navy
        if not self.control_point.captured and skip_enemy_navy:
            return
        for position in self.control_point.preset_locations.ships:
            unit_group = self.armed_forces.random_group_for_task(GroupTask.NAVY)
            if not unit_group:
                logging.warning(f"{self.faction_name} has no ForceGroup for Navy")
                return
            self.generate_ground_object_from_group(unit_group, position)


class NoOpGroundObjectGenerator(ControlPointGroundObjectGenerator):
    def generate(self) -> bool:
        return True


class CarrierGroundObjectGenerator(ControlPointGroundObjectGenerator):
    def generate(self) -> bool:
        if not super().generate():
            return False

        carrier_names = self.faction.carrier_names
        if not carrier_names:
            logging.info(
                f"Skipping generation of {self.control_point.name} because "
                f"{self.faction_name} has no carriers"
            )
            return False

        unit_group = self.armed_forces.random_group_for_task(GroupTask.AIRCRAFT_CARRIER)
        if not unit_group:
            logging.error(f"{self.faction_name} has no access to AircraftCarrier")
            return False
        self.generate_ground_object_from_group(
            unit_group,
            PointWithHeading.from_point(
                self.control_point.position, self.control_point.heading
            ),
        )
        self.control_point.name = random.choice(carrier_names)
        return True


class LhaGroundObjectGenerator(ControlPointGroundObjectGenerator):
    def generate(self) -> bool:
        if not super().generate():
            return False

        lha_names = self.faction.helicopter_carrier_names
        if not lha_names:
            logging.info(
                f"Skipping generation of {self.control_point.name} because "
                f"{self.faction_name} has no LHAs"
            )
            return False

        unit_group = self.armed_forces.random_group_for_task(
            GroupTask.HELICOPTER_CARRIER
        )
        if not unit_group:
            logging.error(f"{self.faction_name} has no access to HelicopterCarrier")
            return False
        self.generate_ground_object_from_group(
            unit_group,
            PointWithHeading.from_point(
                self.control_point.position, self.control_point.heading
            ),
        )
        self.control_point.name = random.choice(lha_names)
        return True


class AirbaseGroundObjectGenerator(ControlPointGroundObjectGenerator):
    def __init__(
        self,
        game: Game,
        generator_settings: GeneratorSettings,
        control_point: ControlPoint,
    ) -> None:
        super().__init__(game, generator_settings, control_point)

    def generate(self) -> bool:
        if not super().generate():
            return False

        self.generate_ground_points()
        return True

    def generate_ground_points(self) -> None:
        """Generate ground objects and AA sites for the control point."""
        self.generate_armor_groups()
        self.generate_aa()
        self.generate_ewrs()
        self.generate_scenery_sites()
        self.generate_strike_targets()
        self.generate_offshore_strike_targets()
        self.generate_factories()
        self.generate_ammunition_depots()
        self.generate_missile_sites()
        self.generate_coastal_sites()

    def generate_armor_groups(self) -> None:
        for position in self.control_point.preset_locations.armor_groups:
            unit_group = self.armed_forces.random_group_for_task(GroupTask.BASE_DEFENSE)
            if not unit_group:
                logging.error(f"{self.faction_name} has no ForceGroup for Armor")
                return
            self.generate_ground_object_from_group(unit_group, position)

    def generate_aa(self) -> None:
        presets = self.control_point.preset_locations
        aa_tasking = [GroupTask.AAA]
        for position in presets.aaa:
            self.generate_aa_at(position, aa_tasking)
        aa_tasking.insert(0, GroupTask.SHORAD)
        for position in presets.short_range_sams:
            self.generate_aa_at(position, aa_tasking)
        aa_tasking.insert(0, GroupTask.MERAD)
        for position in presets.medium_range_sams:
            self.generate_aa_at(position, aa_tasking)
        aa_tasking.insert(0, GroupTask.LORAD)
        for position in presets.long_range_sams:
            self.generate_aa_at(position, aa_tasking)

    def generate_ewrs(self) -> None:
        for position in self.control_point.preset_locations.ewrs:
            unit_group = self.armed_forces.random_group_for_task(
                GroupTask.EARLY_WARNING_RADAR
            )
            if not unit_group:
                logging.error(f"{self.faction_name} has no ForceGroup for EWR")
                return
            self.generate_ground_object_from_group(unit_group, position)

    def generate_building_at(
        self,
        group_task: GroupTask,
        position: PointWithHeading,
    ) -> None:
        # GroupTask is the type of the building to be generated
        unit_group = self.armed_forces.random_group_for_task(group_task)
        if not unit_group:
            raise RuntimeError(
                f"{self.faction_name} has no access to Building {group_task.description}"
            )
        self.generate_ground_object_from_group(unit_group, position)

    def generate_ammunition_depots(self) -> None:
        for position in self.control_point.preset_locations.ammunition_depots:
            self.generate_building_at(GroupTask.AMMO, position)

    def generate_factories(self) -> None:
        for position in self.control_point.preset_locations.factories:
            self.generate_building_at(GroupTask.FACTORY, position)

    def generate_aa_at(
        self, position: PointWithHeading, tasks: list[GroupTask]
    ) -> None:
        for task in tasks:
            unit_group = self.armed_forces.random_group_for_task(task)
            if unit_group:
                # Only take next (smaller) aa_range when no template available for the
                # most requested range. Otherwise break the loop and continue
                self.generate_ground_object_from_group(unit_group, position)
                return

        logging.error(
            f"{self.faction_name} has no access to SAM {', '.join([task.description for task in tasks])}"
        )

    def generate_scenery_sites(self) -> None:
        presets = self.control_point.preset_locations
        for scenery_group in presets.scenery:
            self.generate_tgo_for_scenery(scenery_group)

    def generate_tgo_for_scenery(self, scenery: SceneryGroup) -> None:
        # Special Handling for scenery Objects based on trigger zones
        g = BuildingGroundObject(
            namegen.random_objective_name(),
            scenery.category,
            scenery.position,
            Heading.from_degrees(0),
            self.control_point,
        )
        ground_group = TheaterGroup(
            self.game.next_group_id(),
            scenery.zone_def.name,
            PointWithHeading.from_point(scenery.position, Heading.from_degrees(0)),
            [],
            g,
        )
        g.groups.append(ground_group)
        # Each nested trigger zone is a target/building/unit for an objective.
        for zone in scenery.zones:
            scenery_unit = SceneryUnit(
                zone.id,
                zone.name,
                dcs.statics.Fortification.White_Flag,
                PointWithHeading.from_point(zone.position, Heading.from_degrees(0)),
                g,
            )
            scenery_unit.zone = zone
            ground_group.units.append(scenery_unit)

        self.control_point.connected_objectives.append(g)

    def generate_missile_sites(self) -> None:
        for position in self.control_point.preset_locations.missile_sites:
            unit_group = self.armed_forces.random_group_for_task(GroupTask.MISSILE)
            if not unit_group:
                logging.warning(f"{self.faction_name} has no ForceGroup for Missile")
                return
            self.generate_ground_object_from_group(unit_group, position)

    def generate_coastal_sites(self) -> None:
        for position in self.control_point.preset_locations.coastal_defenses:
            unit_group = self.armed_forces.random_group_for_task(GroupTask.COASTAL)
            if not unit_group:
                logging.warning(f"{self.faction_name} has no ForceGroup for Coastal")
                return
            self.generate_ground_object_from_group(unit_group, position)

    def generate_strike_targets(self) -> None:
        for position in self.control_point.preset_locations.strike_locations:
            self.generate_building_at(GroupTask.STRIKE_TARGET, position)

    def generate_offshore_strike_targets(self) -> None:
        for position in self.control_point.preset_locations.offshore_strike_locations:
            self.generate_building_at(GroupTask.OIL, position)


class FobGroundObjectGenerator(AirbaseGroundObjectGenerator):
    def generate(self) -> bool:
        if super(FobGroundObjectGenerator, self).generate():
            self.generate_fob()
            return True
        return False

    def generate_fob(self) -> None:
        self.generate_building_at(
            GroupTask.FOB,
            PointWithHeading.from_point(
                self.control_point.position, self.control_point.heading
            ),
        )


class GroundObjectGenerator:
    def __init__(self, game: Game, generator_settings: GeneratorSettings) -> None:
        self.game = game
        self.generator_settings = generator_settings

    def generate(self) -> None:
        # Copied so we can remove items from the original list without breaking
        # the iterator.
        control_points = list(self.game.theater.controlpoints)
        for control_point in control_points:
            if not self.generate_for_control_point(control_point):
                self.game.theater.controlpoints.remove(control_point)

    def generate_for_control_point(self, control_point: ControlPoint) -> bool:
        generator: ControlPointGroundObjectGenerator
        if control_point.cptype == ControlPointType.AIRCRAFT_CARRIER_GROUP:
            generator = CarrierGroundObjectGenerator(
                self.game, self.generator_settings, control_point
            )
        elif control_point.cptype == ControlPointType.LHA_GROUP:
            generator = LhaGroundObjectGenerator(
                self.game, self.generator_settings, control_point
            )
        elif isinstance(control_point, OffMapSpawn):
            generator = NoOpGroundObjectGenerator(
                self.game, self.generator_settings, control_point
            )
        elif isinstance(control_point, Fob):
            generator = FobGroundObjectGenerator(
                self.game, self.generator_settings, control_point
            )
        else:
            generator = AirbaseGroundObjectGenerator(
                self.game, self.generator_settings, control_point
            )
        return generator.generate()
