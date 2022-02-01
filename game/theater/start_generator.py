from __future__ import annotations

import logging
import random
from dataclasses import dataclass
from datetime import datetime
from typing import List

from game import Game
from game.factions.faction import Faction
from game.preset_group import PresetTrigger
from game.theater import PointWithHeading, PresetLocation
from game.theater.theatergroundobject import (
    BuildingGroundObject,
    SceneryGroundUnit,
    GroundGroup,
    IadsBuildingGroundObject,
)
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
from ..data.groups import GroupRole, GroupTask, ROLE_TASKINGS
from game.groundforces.ground_force_group import GroundForceGroup
from ..groundforces.ground_forces import GroundForces
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
    def ground_forces(self) -> GroundForces:
        return self.game.coalition_for(self.control_point.captured).ground_forces

    def generate(self) -> bool:
        self.control_point.connected_objectives = []
        self.generate_navy()
        return True

    def generate_ground_object_for_preset(
        self, preset_location: PresetLocation
    ) -> None:
        """Generate a ground_object for a given PresetLocation"""
        if preset_location.task is None:
            logging.error(
                f"PresetLocation {preset_location.original_name} has no task. Skipping"
            )
            return

        possible_unit_groups = list(
            self.ground_forces.groups_for_task(preset_location.task)
        )
        if preset_location.unit_group:
            possible_unit_groups = list(
                self.ground_forces.groups_by_name(preset_location.unit_group)
            )

        if not possible_unit_groups:
            logging.error(
                f"No groups found for PresetLocation {preset_location.original_name}"
            )
            return

        unit_group = random.choice(possible_unit_groups)
        self.generate_ground_object_from_group(
            unit_group, preset_location, preset_location.template
        )

    def generate_ground_object_from_group(
        self,
        unit_group: GroundForceGroup,
        location: PresetLocation,
        forced_template: str = "",
    ) -> None:
        """Generate a ground_object for a GroundForceGroup"""
        with logged_duration(
            f"GroundObject generation for {unit_group.name} ({unit_group.role.value})"
        ):
            ground_object = unit_group.generate(
                namegen.random_objective_name(),
                location,
                self.control_point,
                self.game,
                forced_template,
            )
            if ground_object:
                self.control_point.connected_objectives.append(ground_object)

    def generate_navy(self) -> None:
        skip_player_navy = self.generator_settings.no_player_navy
        if self.control_point.captured and skip_player_navy:
            return
        skip_enemy_navy = self.generator_settings.no_enemy_navy
        if not self.control_point.captured and skip_enemy_navy:
            return
        for position in self.control_point.preset_locations.ships:
            unit_group = self.ground_forces.random_group_for_role_and_task(
                GroupRole.Naval, GroupTask.Navy
            )
            if not unit_group:
                logging.error(f"{self.faction_name} has no UnitGroup for Navy")
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

        unit_group = self.ground_forces.random_group_for_role_and_task(
            GroupRole.Naval, GroupTask.AircraftCarrier
        )
        if not unit_group:
            logging.error(f"{self.faction_name} has no UnitGroup for AircraftCarrier")
            return False
        self.control_point.name = random.choice(carrier_names)
        self.generate_ground_object_from_group(
            unit_group,
            PresetLocation(
                self.control_point.name,
                PointWithHeading.from_point(
                    self.control_point.position, self.control_point.heading
                ),
            ),
        )
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

        unit_group = self.ground_forces.random_group_for_role_and_task(
            GroupRole.Naval, GroupTask.HelicopterCarrier
        )
        if not unit_group:
            logging.error(f"{self.faction_name} has no UnitGroup for HelicopterCarrier")
            return False
        self.control_point.name = random.choice(lha_names)
        self.generate_ground_object_from_group(
            unit_group,
            PresetLocation(
                self.control_point.name,
                PointWithHeading.from_point(
                    self.control_point.position, self.control_point.heading
                ),
            ),
        )
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
        self.generate_scenery_sites()
        self.generate_buildings()
        self.generate_missile_sites()
        self.generate_coastal_sites()

    def generate_armor_groups(self) -> None:
        for position in self.control_point.preset_locations.armor_groups:
            unit_group = self.ground_forces.random_group_for_role_and_tasks(
                GroupRole.GroundForce, ROLE_TASKINGS[GroupRole.GroundForce]
            )
            if not unit_group:
                logging.error(f"{self.faction_name} has no templates for Armor Groups")
                return
            self.generate_ground_object_from_group(unit_group, position)

    def generate_aa(self) -> None:
        presets = [
            self.control_point.preset_locations.ewrs,
            self.control_point.preset_locations.aaa,
            self.control_point.preset_locations.short_range_sams,
            self.control_point.preset_locations.medium_range_sams,
            self.control_point.preset_locations.long_range_sams,
        ]
        tasks = [
            GroupTask.EWR,
            GroupTask.AAA,
            GroupTask.SHORAD,
            GroupTask.MERAD,
            GroupTask.LORAD,
        ]

        # This will iterate over all presets for the different ranges and adds the
        # tasks for it. It adds also the previous tasks to ensure that if a faction
        # for example does not have long range SAMs it will generate medium range
        for i, preset in enumerate(presets):
            for location in preset:
                if location.unit_group or location.template:
                    # Specific group from preset trigger
                    self.generate_ground_object_for_preset(location)
                else:
                    # Random Group for Task
                    self.generate_random_aa_at(location, tasks[: i + 1])

    def generate_building_at(
        self,
        group_task: GroupTask,
        location: PresetLocation,
    ) -> None:
        # GroupTask is the type of the building to be generated
        unit_group = self.ground_forces.random_group_for_role_and_task(
            GroupRole.Building, group_task
        )
        if not unit_group:
            logging.error(
                f"{self.faction_name} has no access to Building ({group_task.value})"
            )
            return
        self.generate_ground_object_from_group(unit_group, location)

    def generate_random_aa_at(
        self, location: PresetLocation, tasks: list[GroupTask]
    ) -> None:
        for task in reversed(tasks):
            unit_group = self.ground_forces.random_group_for_role_and_task(
                GroupRole.AntiAir, task
            )
            if unit_group:
                # Only take next (smaller) aa_range when no template available for the
                # most requested range. Otherwise break the loop and continue
                self.generate_ground_object_from_group(unit_group, location)
                return

        logging.error(
            f"{self.faction_name} has no access to Anti Air ({', '.join([task.value for task in tasks])})"
        )

    def generate_scenery_sites(self) -> None:
        presets = self.control_point.preset_locations
        for scenery_group in presets.scenery:
            self.generate_tgo_for_scenery(scenery_group)

    def generate_tgo_for_scenery(self, scenery: PresetTrigger) -> None:
        # Special Handling for scenery Objects based on trigger zones
        g = BuildingGroundObject(
            namegen.random_objective_name(),
            scenery.task.value.lower(),
            scenery.location,
            self.control_point,
        )
        ground_group = GroundGroup(
            self.game.next_group_id(),
            scenery.zone.name,
            scenery.location,
            [],
            g,
        )
        ground_group.static_group = True
        g.groups.append(ground_group)
        # Each nested trigger zone is a target/building/unit for an objective.
        for zone in scenery.scenery_zones:
            scenery_unit = SceneryGroundUnit(
                zone.id,
                zone.name,
                "",
                PointWithHeading.from_point(zone.position, Heading.from_degrees(0)),
                g,
            )
            scenery_unit.zone = zone
            ground_group.units.append(scenery_unit)

        self.control_point.connected_objectives.append(g)

    def generate_missile_sites(self) -> None:
        for position in self.control_point.preset_locations.missile_sites:
            unit_group = self.ground_forces.random_group_for_role_and_task(
                GroupRole.Defenses, GroupTask.Missile
            )
            if not unit_group:
                logging.error(f"{self.faction_name} has no UnitGroup for Missile")
                return
            self.generate_ground_object_from_group(unit_group, position)

    def generate_coastal_sites(self) -> None:
        for position in self.control_point.preset_locations.coastal_defenses:
            unit_group = self.ground_forces.random_group_for_role_and_task(
                GroupRole.Defenses, GroupTask.Coastal
            )
            if not unit_group:
                logging.error(f"{self.faction_name} has no UnitGroup for Coastal")
                return
            self.generate_ground_object_from_group(unit_group, position)

    def generate_buildings(self) -> None:
        for preset_location in self.control_point.preset_locations.buildings:
            if preset_location.task is None:
                logging.error(
                    f"Building {preset_location.original_name} has no tasking"
                )
                continue
            self.generate_building_at(preset_location.task, preset_location)


class FobGroundObjectGenerator(AirbaseGroundObjectGenerator):
    def generate(self) -> bool:
        if super(FobGroundObjectGenerator, self).generate():
            self.generate_fob()
            return True
        return False

    def generate_fob(self) -> None:
        self.generate_building_at(
            GroupTask.FOB,
            PresetLocation(
                self.control_point.name,
                PointWithHeading.from_point(
                    self.control_point.position, self.control_point.heading
                ),
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
