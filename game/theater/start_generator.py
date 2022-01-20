from __future__ import annotations

import logging
import pickle
import random
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Iterable, List, Set

from dcs.mapping import Point

from game import Game
from game.factions.faction import Faction
from game.scenery_group import SceneryGroup
from game.theater import PointWithHeading
from game.theater.theatergroundobject import (
    BuildingGroundObject,
    CarrierGroundObject,
    EwrGroundObject,
    FactoryGroundObject,
    LhaGroundObject,
    MissileSiteGroundObject,
    SamGroundObject,
    ShipGroundObject,
    SceneryGroundObject,
    VehicleGroupGroundObject,
    CoastalSiteGroundObject,
)
from game.utils import Heading
from game.version import VERSION
from gen.coastal.coastal_group_generator import generate_coastal_group
from gen.defenses.armor_group_generator import generate_armor_group
from gen.fleet.ship_group_generator import (
    generate_carrier_group,
    generate_lha_group,
    generate_ship_group,
)
from gen.missiles.missiles_group_generator import generate_missile_group
from gen.naming import namegen
from gen.sam.airdefensegroupgenerator import AirDefenseRange
from gen.sam.ewr_group_generator import generate_ewr_group
from gen.sam.sam_group_generator import generate_anti_air_group
from . import (
    ConflictTheater,
    ControlPoint,
    ControlPointType,
    Fob,
    OffMapSpawn,
)
from ..campaignloader.campaignairwingconfig import CampaignAirWingConfig
from ..profiling import logged_duration
from ..settings import Settings

GroundObjectTemplates = Dict[str, Dict[str, Any]]


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
        self.player = player.apply_mod_settings(mod_settings)
        self.enemy = enemy.apply_mod_settings(mod_settings)
        self.theater = theater
        self.air_wing_config = air_wing_config
        self.settings = settings
        self.generator_settings = generator_settings

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

    def generate(self) -> bool:
        self.control_point.connected_objectives = []
        if self.faction.navy_generators:
            # Even airbases can generate navies if they are close enough to the water.
            self.generate_navy()

        return True

    def generate_navy(self) -> None:
        skip_player_navy = self.generator_settings.no_player_navy
        if self.control_point.captured and skip_player_navy:
            return

        skip_enemy_navy = self.generator_settings.no_enemy_navy
        if not self.control_point.captured and skip_enemy_navy:
            return

        for position in self.control_point.preset_locations.ships:
            self.generate_ship_at(position)

    def generate_ship_at(self, position: PointWithHeading) -> None:
        group_id = self.game.next_group_id()

        g = ShipGroundObject(
            namegen.random_objective_name(), group_id, position, self.control_point
        )

        group = generate_ship_group(self.game, g, self.faction_name)
        g.groups = []
        if group is not None:
            g.groups.append(group)
            self.control_point.connected_objectives.append(g)


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

        # Create ground object group
        group_id = self.game.next_group_id()
        g = CarrierGroundObject(
            namegen.random_objective_name(), group_id, self.control_point
        )
        group = generate_carrier_group(self.faction_name, self.game, g)
        g.groups = []
        if group is not None:
            g.groups.append(group)
        self.control_point.connected_objectives.append(g)
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

        # Create ground object group
        group_id = self.game.next_group_id()
        g = LhaGroundObject(
            namegen.random_objective_name(), group_id, self.control_point
        )
        group = generate_lha_group(self.faction_name, self.game, g)
        g.groups = []
        if group is not None:
            g.groups.append(group)
        self.control_point.connected_objectives.append(g)
        self.control_point.name = random.choice(lha_names)
        return True


class AirbaseGroundObjectGenerator(ControlPointGroundObjectGenerator):
    def __init__(
        self,
        game: Game,
        generator_settings: GeneratorSettings,
        control_point: ControlPoint,
        templates: GroundObjectTemplates,
    ) -> None:
        super().__init__(game, generator_settings, control_point)
        self.templates = templates

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

        if self.faction.missiles:
            self.generate_missile_sites()

        if self.faction.coastal_defenses:
            self.generate_coastal_sites()

    def generate_armor_groups(self) -> None:
        for position in self.control_point.preset_locations.armor_groups:
            self.generate_armor_at(position)

    def generate_armor_at(self, position: PointWithHeading) -> None:
        group_id = self.game.next_group_id()

        g = VehicleGroupGroundObject(
            namegen.random_objective_name(),
            group_id,
            position,
            self.control_point,
        )

        group = generate_armor_group(self.faction_name, self.game, g)
        if group is None:
            logging.error(
                "Could not generate armor group for %s at %s",
                g.name,
                self.control_point,
            )
            return
        g.groups = [group]
        self.control_point.connected_objectives.append(g)

    def generate_aa(self) -> None:
        presets = self.control_point.preset_locations
        for position in presets.long_range_sams:
            self.generate_aa_at(
                position,
                ranges=[
                    {AirDefenseRange.Long},
                    {AirDefenseRange.Medium},
                    {AirDefenseRange.Short},
                    {AirDefenseRange.AAA},
                ],
            )
        for position in presets.medium_range_sams:
            self.generate_aa_at(
                position,
                ranges=[
                    {AirDefenseRange.Medium},
                    {AirDefenseRange.Short},
                    {AirDefenseRange.AAA},
                ],
            )
        for position in presets.short_range_sams:
            self.generate_aa_at(
                position,
                ranges=[{AirDefenseRange.Short}, {AirDefenseRange.AAA}],
            )
        for position in presets.aaa:
            self.generate_aa_at(
                position,
                ranges=[{AirDefenseRange.AAA}],
            )

    def generate_ewrs(self) -> None:
        presets = self.control_point.preset_locations
        for position in presets.ewrs:
            self.generate_ewr_at(position)

    def generate_strike_target_at(self, category: str, position: Point) -> None:

        obj_name = namegen.random_objective_name()
        template = random.choice(list(self.templates[category].values()))

        object_id = 0
        group_id = self.game.next_group_id()

        # TODO: Create only one TGO per objective, each with multiple units.
        for unit in template:
            object_id += 1

            template_point = Point(unit["offset"].x, unit["offset"].y)
            g = BuildingGroundObject(
                obj_name,
                category,
                group_id,
                object_id,
                position + template_point,
                Heading.from_degrees(unit["heading"]),
                self.control_point,
                unit["type"],
            )

            self.control_point.connected_objectives.append(g)

    def generate_ammunition_depots(self) -> None:
        for position in self.control_point.preset_locations.ammunition_depots:
            self.generate_strike_target_at(category="ammo", position=position)

    def generate_factories(self) -> None:
        for position in self.control_point.preset_locations.factories:
            self.generate_factory_at(position)

    def generate_factory_at(self, point: PointWithHeading) -> None:
        obj_name = namegen.random_objective_name()
        group_id = self.game.next_group_id()

        g = FactoryGroundObject(
            obj_name,
            group_id,
            point,
            point.heading,
            self.control_point,
        )

        self.control_point.connected_objectives.append(g)

    def generate_aa_at(
        self, position: Point, ranges: Iterable[Set[AirDefenseRange]]
    ) -> None:
        group_id = self.game.next_group_id()

        g = SamGroundObject(
            namegen.random_objective_name(),
            group_id,
            position,
            self.control_point,
        )
        groups = generate_anti_air_group(self.game, g, self.faction, ranges)
        if not groups:
            logging.error(
                "Could not generate air defense group for %s at %s",
                g.name,
                self.control_point,
            )
            return
        g.groups = groups
        self.control_point.connected_objectives.append(g)

    def generate_ewr_at(self, position: PointWithHeading) -> None:
        group_id = self.game.next_group_id()

        g = EwrGroundObject(
            namegen.random_objective_name(),
            group_id,
            position,
            self.control_point,
        )
        group = generate_ewr_group(self.game, g, self.faction)
        if group is None:
            logging.error(
                "Could not generate ewr group for %s at %s",
                g.name,
                self.control_point,
            )
            return
        g.groups = [group]
        self.control_point.connected_objectives.append(g)

    def generate_scenery_sites(self) -> None:
        presets = self.control_point.preset_locations
        for scenery_group in presets.scenery:
            self.generate_tgo_for_scenery(scenery_group)

    def generate_tgo_for_scenery(self, scenery: SceneryGroup) -> None:

        obj_name = namegen.random_objective_name()
        category = scenery.category
        group_id = self.game.next_group_id()
        object_id = 0

        # Each nested trigger zone is a target/building/unit for an objective.
        for zone in scenery.zones:

            object_id += 1
            local_position = zone.position
            local_dcs_identifier = zone.name

            g = SceneryGroundObject(
                obj_name,
                category,
                group_id,
                object_id,
                local_position,
                self.control_point,
                local_dcs_identifier,
                zone,
            )

            self.control_point.connected_objectives.append(g)

        return

    def generate_missile_sites(self) -> None:
        for position in self.control_point.preset_locations.missile_sites:
            self.generate_missile_site_at(position)

    def generate_missile_site_at(self, position: PointWithHeading) -> None:
        group_id = self.game.next_group_id()

        g = MissileSiteGroundObject(
            namegen.random_objective_name(), group_id, position, self.control_point
        )
        group = generate_missile_group(self.game, g, self.faction_name)
        g.groups = []
        if group is not None:
            g.groups.append(group)
            self.control_point.connected_objectives.append(g)
        return

    def generate_coastal_sites(self) -> None:
        for position in self.control_point.preset_locations.coastal_defenses:
            self.generate_coastal_site_at(position)

    def generate_coastal_site_at(self, position: PointWithHeading) -> None:
        group_id = self.game.next_group_id()

        g = CoastalSiteGroundObject(
            namegen.random_objective_name(),
            group_id,
            position,
            self.control_point,
            position.heading,
        )
        group = generate_coastal_group(self.game, g, self.faction_name)
        g.groups = []
        if group is not None:
            g.groups.append(group)
            self.control_point.connected_objectives.append(g)
        return

    def generate_strike_targets(self) -> None:
        building_set = list(set(self.faction.building_set) - {"oil"})
        if not building_set:
            logging.error("Faction has no buildings defined")
            return
        for position in self.control_point.preset_locations.strike_locations:
            category = random.choice(building_set)
            self.generate_strike_target_at(category, position)

    def generate_offshore_strike_targets(self) -> None:
        if "oil" not in self.faction.building_set:
            logging.error("Faction does not support offshore strike targets")
            return
        for position in self.control_point.preset_locations.offshore_strike_locations:
            self.generate_strike_target_at("oil", position)


class FobGroundObjectGenerator(AirbaseGroundObjectGenerator):
    def generate(self) -> bool:
        self.generate_fob()
        self.generate_armor_groups()
        self.generate_factories()
        self.generate_ammunition_depots()
        self.generate_aa()
        self.generate_ewrs()
        self.generate_scenery_sites()
        self.generate_strike_targets()
        self.generate_offshore_strike_targets()

        if self.faction.missiles:
            self.generate_missile_sites()

        if self.faction.coastal_defenses:
            self.generate_coastal_sites()

        return True

    def generate_fob(self) -> None:
        category = "fob"
        obj_name = self.control_point.name
        template = random.choice(list(self.templates[category].values()))
        point = self.control_point.position
        # Pick from preset locations
        object_id = 0
        group_id = self.game.next_group_id()

        # TODO: Create only one TGO per objective, each with multiple units.
        for unit in template:
            object_id += 1

            template_point = Point(unit["offset"].x, unit["offset"].y)
            g = BuildingGroundObject(
                obj_name,
                category,
                group_id,
                object_id,
                point + template_point,
                Heading.from_degrees(unit["heading"]),
                self.control_point,
                unit["type"],
                is_fob_structure=True,
            )
            self.control_point.connected_objectives.append(g)


class GroundObjectGenerator:
    def __init__(self, game: Game, generator_settings: GeneratorSettings) -> None:
        self.game = game
        self.generator_settings = generator_settings
        with open("resources/groundobject_templates.p", "rb") as f:
            self.templates: GroundObjectTemplates = pickle.load(f)

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
                self.game, self.generator_settings, control_point, self.templates
            )
        else:
            generator = AirbaseGroundObjectGenerator(
                self.game, self.generator_settings, control_point, self.templates
            )
        return generator.generate()
