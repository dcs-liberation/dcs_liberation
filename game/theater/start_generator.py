from __future__ import annotations

import logging
import random
from dataclasses import dataclass
from datetime import datetime
from typing import List

from game import Game
from game.factions.faction import Faction
from game.scenery_group import SceneryGroup
from game.theater import PointWithHeading
from game.theater.theatergroundobject import (
    AirDefenseRange,
    BuildingGroundObject,
    SceneryGroundUnit,
    GroundGroup,
)
from game.utils import Heading
from game.version import VERSION
from gen.templates import GroundObjectTemplates, TemplateCategory, GroundObjectTemplate
from gen.naming import namegen
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
        self.player = player.apply_mod_settings(mod_settings)
        self.enemy = enemy.apply_mod_settings(mod_settings)
        self.theater = theater
        self.air_wing_config = air_wing_config
        self.settings = settings
        self.generator_settings = generator_settings

        with logged_duration(f"Initializing templates"):
            self.load_templates()

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

    def load_templates(self) -> None:
        templates = GroundObjectTemplates.from_json(
            "resources/templates/templates.json"
        )
        self.player.load_templates(templates)
        self.enemy.load_templates(templates)


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

    def generate_random_from_templates(
        self, templates: list[GroundObjectTemplate], position: PointWithHeading
    ) -> None:
        try:
            template = random.choice(templates)
            with logged_duration(
                f"Ground Object generation from template {template.name}"
            ):
                ground_object = template.generate(
                    namegen.random_objective_name(),
                    position,
                    self.control_point,
                    self.game,
                )
            self.control_point.connected_objectives.append(ground_object)
        except NotImplementedError:
            logging.error("Template Generator not implemented yet")
        except IndexError:
            logging.error(f"No templates to generate object")

    def generate_navy(self) -> None:
        skip_player_navy = self.generator_settings.no_player_navy
        if self.control_point.captured and skip_player_navy:
            return

        skip_enemy_navy = self.generator_settings.no_enemy_navy
        if not self.control_point.captured and skip_enemy_navy:
            return

        templates = list(
            self.faction.templates.for_category(TemplateCategory.Naval, "ship")
        )

        for position in self.control_point.preset_locations.ships:
            self.generate_random_from_templates(templates, position)


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

        templates = list(
            self.faction.templates.for_category(TemplateCategory.Naval, "carrier")
        )

        self.generate_random_from_templates(
            templates,
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

        templates = list(
            self.faction.templates.for_category(TemplateCategory.Naval, "lha")
        )

        self.generate_random_from_templates(
            templates,
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

        if self.faction.missiles:
            self.generate_missile_sites()

        if self.faction.coastal_defenses:
            self.generate_coastal_sites()

    def generate_armor_groups(self) -> None:
        templates = list(self.faction.templates.for_category(TemplateCategory.Armor))
        if not templates:
            logging.error(f"{self.faction_name} has no access to Armor templates")
            return

        for position in self.control_point.preset_locations.armor_groups:
            self.generate_random_from_templates(templates, position)

    def generate_aa(self) -> None:
        presets = self.control_point.preset_locations
        for position in presets.long_range_sams:
            self.generate_aa_at(
                position,
                [
                    AirDefenseRange.Long,
                    AirDefenseRange.Medium,
                    AirDefenseRange.Short,
                    AirDefenseRange.AAA,
                ],
            )
        for position in presets.medium_range_sams:
            self.generate_aa_at(
                position,
                [
                    AirDefenseRange.Medium,
                    AirDefenseRange.Short,
                    AirDefenseRange.AAA,
                ],
            )
        for position in presets.short_range_sams:
            self.generate_aa_at(
                position,
                [AirDefenseRange.Short, AirDefenseRange.AAA],
            )
        for position in presets.aaa:
            self.generate_aa_at(
                position,
                [AirDefenseRange.AAA],
            )

    def generate_ewrs(self) -> None:
        templates = list(
            self.faction.templates.for_category(TemplateCategory.AirDefence, "EWR")
        )
        if not templates:
            logging.error(f"{self.faction_name} has no access to EWR templates")
            return

        for position in self.control_point.preset_locations.ewrs:
            self.generate_random_from_templates(templates, position)

    def generate_building_at(
        self,
        template_category: TemplateCategory,
        building_category: str,
        position: PointWithHeading,
    ) -> None:
        templates = list(
            self.faction.templates.for_category(template_category, building_category)
        )
        if templates:
            self.generate_random_from_templates(templates, position)
        else:
            logging.error(
                f"{self.faction_name} has no access to Building type {building_category}"
            )

    def generate_ammunition_depots(self) -> None:
        for position in self.control_point.preset_locations.ammunition_depots:
            self.generate_building_at(TemplateCategory.Building, "ammo", position)

    def generate_factories(self) -> None:
        for position in self.control_point.preset_locations.factories:
            self.generate_building_at(TemplateCategory.Building, "factory", position)

    def generate_aa_at(
        self, position: PointWithHeading, ranges: list[AirDefenseRange]
    ) -> None:

        templates = []
        for aa_range in ranges:
            for template in self.faction.templates.for_category(
                TemplateCategory.AirDefence, aa_range.name
            ):
                templates.append(template)
            if len(templates) > 0:
                # Only take next (smaller) aa_range when no template available for the
                # most requested range. Otherwise break the loop and continue
                break

        if templates:
            self.generate_random_from_templates(templates, position)
        else:
            logging.error(
                f"{self.faction_name} has no access to SAM Templates ({', '.join([range.name for range in ranges])})"
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
        ground_group = GroundGroup(
            self.game.next_group_id(),
            scenery.zone_def.name,
            PointWithHeading.from_point(scenery.position, Heading.from_degrees(0)),
            [],
            g,
        )
        ground_group.static_group = True
        g.groups.append(ground_group)
        # Each nested trigger zone is a target/building/unit for an objective.
        for zone in scenery.zones:
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
        templates = list(self.faction.templates.for_category(TemplateCategory.Missile))
        if not templates:
            logging.error(f"{self.faction_name} has no access to Missile templates")
            return
        for position in self.control_point.preset_locations.missile_sites:
            self.generate_random_from_templates(templates, position)

    def generate_coastal_sites(self) -> None:
        templates = list(self.faction.templates.for_category(TemplateCategory.Coastal))
        if not templates:
            logging.error(f"{self.faction_name} has no access to Coastal templates")
            return
        for position in self.control_point.preset_locations.coastal_defenses:
            self.generate_random_from_templates(templates, position)

    def generate_strike_targets(self) -> None:
        building_set = list(set(self.faction.building_set) - {"oil"})
        if not building_set:
            logging.error(f"{self.faction_name} has no buildings defined")
            return
        for position in self.control_point.preset_locations.strike_locations:
            category = random.choice(building_set)
            self.generate_building_at(TemplateCategory.Building, category, position)

    def generate_offshore_strike_targets(self) -> None:
        if "oil" not in self.faction.building_set:
            logging.error(
                f"{self.faction_name} does not support offshore strike targets"
            )
            return
        for position in self.control_point.preset_locations.offshore_strike_locations:
            self.generate_building_at(TemplateCategory.Building, "oil", position)


class FobGroundObjectGenerator(AirbaseGroundObjectGenerator):
    def generate(self) -> bool:
        if super(FobGroundObjectGenerator, self).generate():
            self.generate_fob()
            return True
        return False

    def generate_fob(self) -> None:
        self.generate_building_at(
            TemplateCategory.Building,
            "fob",
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
