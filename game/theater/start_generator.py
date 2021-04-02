from __future__ import annotations

import logging
import pickle
import random
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional, Set

from dcs.mapping import Point
from dcs.task import CAP, CAS, PinpointStrike
from dcs.vehicles import AirDefence

from game import Game, db
from game.factions.faction import Faction
from game.theater import Carrier, Lha, LocationType, PointWithHeading
from game.theater.theatergroundobject import (
    BuildingGroundObject,
    CarrierGroundObject,
    EwrGroundObject,
    LhaGroundObject,
    MissileSiteGroundObject,
    SamGroundObject,
    ShipGroundObject,
    VehicleGroupGroundObject,
    CoastalSiteGroundObject,
)
from game.version import VERSION
from gen import namegen
from gen.coastal.coastal_group_generator import generate_coastal_group
from gen.defenses.armor_group_generator import generate_armor_group
from gen.fleet.ship_group_generator import (
    generate_carrier_group,
    generate_lha_group,
    generate_ship_group,
)
from gen.locations.preset_location_finder import MizDataLocationFinder
from gen.missiles.missiles_group_generator import generate_missile_group
from gen.sam.airdefensegroupgenerator import AirDefenseRange
from gen.sam.sam_group_generator import (
    generate_anti_air_group,
    generate_ewr_group,
)
from . import (
    ConflictTheater,
    ControlPoint,
    ControlPointType,
    Fob,
    OffMapSpawn,
)
from ..settings import Settings

GroundObjectTemplates = Dict[str, Dict[str, Any]]

UNIT_VARIETY = 6
UNIT_AMOUNT_FACTOR = 16
UNIT_COUNT_IMPORTANCE_LOG = 1.3

COUNT_BY_TASK = {
    PinpointStrike: 12,
    CAP: 8,
    CAS: 4,
    AirDefence: 1,
}


@dataclass(frozen=True)
class GeneratorSettings:
    start_date: datetime
    player_budget: int
    enemy_budget: int
    midgame: bool
    inverted: bool
    no_carrier: bool
    no_lha: bool
    no_player_navy: bool
    no_enemy_navy: bool


class GameGenerator:
    def __init__(
        self,
        player: str,
        enemy: str,
        theater: ConflictTheater,
        settings: Settings,
        generator_settings: GeneratorSettings,
    ) -> None:
        self.player = player
        self.enemy = enemy
        self.theater = theater
        self.settings = settings
        self.generator_settings = generator_settings

    def generate(self) -> Game:
        # Reset name generator
        namegen.reset()
        self.prepare_theater()
        game = Game(
            player_name=self.player,
            enemy_name=self.enemy,
            theater=self.theater,
            start_date=self.generator_settings.start_date,
            settings=self.settings,
            player_budget=self.generator_settings.player_budget,
            enemy_budget=self.generator_settings.enemy_budget,
        )

        GroundObjectGenerator(game, self.generator_settings).generate()
        game.settings.version = VERSION
        return game

    def prepare_theater(self) -> None:
        to_remove: List[ControlPoint] = []
        # Auto-capture half the bases if midgame.
        if self.generator_settings.midgame:
            control_points = self.theater.controlpoints
            for control_point in control_points[: len(control_points) // 2]:
                control_point.captured = True

        # Remove carrier and lha, invert situation if needed
        for cp in self.theater.controlpoints:
            if isinstance(cp, Carrier) and self.generator_settings.no_carrier:
                to_remove.append(cp)
            elif isinstance(cp, Lha) and self.generator_settings.no_lha:
                to_remove.append(cp)

            if self.generator_settings.inverted:
                cp.captured = cp.captured_invert

        # do remove
        for cp in to_remove:
            self.theater.controlpoints.remove(cp)

        # TODO: Fix this. This captures all bases for blue.
        # reapply midgame inverted if needed
        if self.generator_settings.midgame and self.generator_settings.inverted:
            for i, cp in enumerate(reversed(self.theater.controlpoints)):
                if i > len(self.theater.controlpoints):
                    break
                else:
                    cp.captured = True


class LocationFinder:
    def __init__(self, game: Game, control_point: ControlPoint) -> None:
        self.game = game
        self.control_point = control_point
        self.miz_data = MizDataLocationFinder.compute_possible_locations(
            game.theater.terrain.name, control_point.full_name
        )

    def location_for(self, location_type: LocationType) -> Optional[PointWithHeading]:
        position = self.control_point.preset_locations.random_for(location_type)
        if position is not None:
            return position

        logging.warning(
            f"No campaign location for %s Mat %s",
            location_type.value,
            self.control_point,
        )
        position = self.random_from_miz_data(
            location_type == LocationType.OffshoreStrikeTarget
        )
        if position is not None:
            return position

        logging.debug(
            f"No mizdata location for %s at %s", location_type.value, self.control_point
        )
        position = self.random_position(location_type)
        if position is not None:
            return position

        logging.error(
            f"Could not find position for %s at %s",
            location_type.value,
            self.control_point,
        )
        return None

    def random_from_miz_data(self, offshore: bool) -> Optional[PointWithHeading]:
        if offshore:
            locations = self.miz_data.offshore_locations
        else:
            locations = self.miz_data.ashore_locations
        if self.miz_data.offshore_locations:
            preset = random.choice(locations)
            locations.remove(preset)
            return PointWithHeading.from_point(preset.position, preset.heading)
        return None

    def random_position(
        self, location_type: LocationType
    ) -> Optional[PointWithHeading]:
        # TODO: Flesh out preset locations so we never hit this case.

        if location_type == LocationType.Coastal:
            # No coastal locations generated randomly
            return None

        logging.warning(
            "Falling back to random location for %s at %s",
            location_type.value,
            self.control_point,
        )

        is_base_defense = location_type in {
            LocationType.BaseAirDefense,
            LocationType.Garrison,
            LocationType.Shorad,
        }

        on_land = location_type not in {
            LocationType.OffshoreStrikeTarget,
            LocationType.Ship,
        }

        avoid_others = location_type not in {
            LocationType.Garrison,
            LocationType.MissileSite,
            LocationType.Sam,
            LocationType.Ship,
            LocationType.Shorad,
        }

        if is_base_defense:
            min_range = 400
            max_range = 3200
        elif location_type == LocationType.Ship:
            min_range = 5000
            max_range = 40000
        elif location_type == LocationType.MissileSite:
            min_range = 2500
            max_range = 40000
        else:
            min_range = 10000
            max_range = 40000

        position = self._find_random_position(
            min_range, max_range, on_land, is_base_defense, avoid_others
        )

        # Retry once, searching a bit further (On some big airbases, 3200 is too
        # short (Ex : Incirlik)), but searching farther on every base would be
        # problematic, as some base defense units would end up very far away
        # from small airfields.
        if position is None and is_base_defense:
            position = self._find_random_position(
                3200, 4800, on_land, is_base_defense, avoid_others
            )
        return position

    def _find_random_position(
        self,
        min_range: int,
        max_range: int,
        on_ground: bool,
        is_base_defense: bool,
        avoid_others: bool,
    ) -> Optional[PointWithHeading]:
        """
        Find a valid ground object location
        :param on_ground: Whether it should be on ground or on sea (True = on
        ground)
        :param min_range: Minimal range from point
        :param max_range: Max range from point
        :param is_base_defense: True if the location is for base defense.
        :return:
        """
        near = self.control_point.position
        others = self.control_point.ground_objects

        def is_valid(point: Optional[PointWithHeading]) -> bool:
            if point is None:
                return False

            if on_ground and not self.game.theater.is_on_land(point):
                return False
            elif not on_ground and not self.game.theater.is_in_sea(point):
                return False

            if avoid_others:
                for other in others:
                    if other.position.distance_to_point(point) < 10000:
                        return False

            if is_base_defense:
                # If it's a base defense we don't care how close it is to other
                # points.
                return True

            # Else verify that it's not too close to another control point.
            for control_point in self.game.theater.controlpoints:
                if control_point != self.control_point:
                    if control_point.position.distance_to_point(point) < 30000:
                        return False
                    for ground_obj in control_point.ground_objects:
                        if ground_obj.position.distance_to_point(point) < 10000:
                            return False
            return True

        for _ in range(300):
            # Check if on land or sea
            p = PointWithHeading.from_point(
                near.random_point_within(max_range, min_range), random.randint(0, 360)
            )
            if is_valid(p):
                return p
        return None


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
        self.location_finder = LocationFinder(game, control_point)

    @property
    def faction_name(self) -> str:
        if self.control_point.captured:
            return self.game.player_name
        else:
            return self.game.enemy_name

    @property
    def faction(self) -> Faction:
        return db.FACTIONS[self.faction_name]

    def generate(self) -> bool:
        self.control_point.connected_objectives = []
        if self.faction.navy_generators:
            # Even airbases can generate navies if they are close enough to the
            # water. This is not controlled by the control point definition, but
            # rather by whether or not the generator can find a valid position
            # for the ship.
            self.generate_navy()

        return True

    def generate_navy(self) -> None:
        skip_player_navy = self.generator_settings.no_player_navy
        if self.control_point.captured and skip_player_navy:
            return

        skip_enemy_navy = self.generator_settings.no_enemy_navy
        if not self.control_point.captured and skip_enemy_navy:
            return

        for _ in range(self.faction.navy_group_count):
            self.generate_ship()

    def generate_ship(self) -> None:
        point = self.location_finder.location_for(LocationType.OffshoreStrikeTarget)
        if point is None:
            return

        group_id = self.game.next_group_id()

        g = ShipGroundObject(
            namegen.random_objective_name(), group_id, point, self.control_point
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


class BaseDefenseGenerator:
    def __init__(self, game: Game, control_point: ControlPoint) -> None:
        self.game = game
        self.control_point = control_point
        self.location_finder = LocationFinder(game, control_point)

    @property
    def faction_name(self) -> str:
        if self.control_point.captured:
            return self.game.player_name
        else:
            return self.game.enemy_name

    @property
    def faction(self) -> Faction:
        return db.FACTIONS[self.faction_name]

    def generate(self) -> None:
        self.generate_ewr()
        self.generate_garrison()
        self.generate_base_defenses()

    def generate_ewr(self) -> None:
        position = self.location_finder.location_for(LocationType.Ewr)
        if position is None:
            return

        group_id = self.game.next_group_id()

        g = EwrGroundObject(
            namegen.random_objective_name(), group_id, position, self.control_point
        )

        group = generate_ewr_group(self.game, g, self.faction)
        if group is None:
            logging.error(f"Could not generate EWR at {self.control_point}")
            return

        g.groups = [group]
        self.control_point.base_defenses.append(g)

    def generate_base_defenses(self) -> None:
        # First group has a 1/2 chance of being a SAM, 1/6 chance of SHORAD,
        # and a 1/6 chance of a garrison.
        #
        # Further groups have a 1/3 chance of being SHORAD and 2/3 chance of
        # being a garrison.
        for i in range(random.randint(2, 5)):
            if i == 0 and random.randint(0, 1) == 0:
                self.generate_sam()
            elif random.randint(0, 2) == 1:
                self.generate_shorad()
            else:
                self.generate_garrison()

    def generate_garrison(self) -> None:
        position = self.location_finder.location_for(LocationType.Garrison)
        if position is None:
            return

        group_id = self.game.next_group_id()

        g = VehicleGroupGroundObject(
            namegen.random_objective_name(),
            group_id,
            position,
            self.control_point,
            for_airbase=True,
        )

        group = generate_armor_group(self.faction_name, self.game, g)
        if group is None:
            logging.error(f"Could not generate garrison at {self.control_point}")
            return
        g.groups.append(group)
        self.control_point.base_defenses.append(g)

    def generate_sam(self) -> None:
        position = self.location_finder.location_for(LocationType.BaseAirDefense)
        if position is None:
            return

        group_id = self.game.next_group_id()

        g = SamGroundObject(
            namegen.random_objective_name(),
            group_id,
            position,
            self.control_point,
            for_airbase=True,
        )

        groups = generate_anti_air_group(self.game, g, self.faction)
        if not groups:
            logging.error(f"Could not generate SAM at {self.control_point}")
            return
        g.groups = groups
        self.control_point.base_defenses.append(g)

    def generate_shorad(self) -> None:
        position = self.location_finder.location_for(LocationType.BaseAirDefense)
        if position is None:
            return

        group_id = self.game.next_group_id()

        g = SamGroundObject(
            namegen.random_objective_name(),
            group_id,
            position,
            self.control_point,
            for_airbase=True,
        )

        groups = generate_anti_air_group(
            self.game, g, self.faction, ranges=[{AirDefenseRange.Short}]
        )
        if not groups:
            logging.error(f"Could not generate SHORAD group at {self.control_point}")
            return
        g.groups = groups
        self.control_point.base_defenses.append(g)


class FobDefenseGenerator(BaseDefenseGenerator):
    def generate(self) -> None:
        self.generate_garrison()
        self.generate_fob_defenses()

    def generate_fob_defenses(self):
        # First group has a 1/2 chance of being a SHORAD,
        # and a 1/2 chance of a garrison.
        #
        # Further groups have a 1/3 chance of being SHORAD and 2/3 chance of
        # being a garrison.
        for i in range(random.randint(2, 5)):
            if i == 0 and random.randint(0, 1) == 0:
                self.generate_shorad()
            elif i == 0 and random.randint(0, 1) == 0:
                self.generate_garrison()
            elif random.randint(0, 2) == 1:
                self.generate_shorad()
            else:
                self.generate_garrison()


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

        BaseDefenseGenerator(self.game, self.control_point).generate()
        self.generate_ground_points()

        if self.faction.missiles:
            self.generate_missile_sites()

        if self.faction.coastal_defenses:
            self.generate_coastal_sites()

        return True

    def generate_ground_points(self) -> None:
        """Generate ground objects and AA sites for the control point."""
        skip_sams = self.generate_required_aa()

        if self.control_point.is_global:
            return

        # Always generate at least one AA point.
        self.generate_aa_site()

        # And between 2 and 7 other objectives.
        amount = random.randrange(2, 7)
        for i in range(amount):
            # 1 in 4 additional objectives are AA.
            if random.randint(0, 3) == 0:
                if skip_sams > 0:
                    skip_sams -= 1
                else:
                    self.generate_aa_site()
            else:
                self.generate_ground_point()

    def generate_required_aa(self) -> int:
        """Generates the AA sites that are required by the campaign.

        Returns:
            The number of AA sites that were generated.
        """
        presets = self.control_point.preset_locations
        for position in presets.required_long_range_sams:
            self.generate_aa_at(
                position,
                ranges=[
                    {AirDefenseRange.Long},
                    {AirDefenseRange.Medium},
                    {AirDefenseRange.Short},
                ],
            )
        for position in presets.required_medium_range_sams:
            self.generate_aa_at(
                position,
                ranges=[
                    {AirDefenseRange.Medium},
                    {AirDefenseRange.Short},
                ],
            )
        return len(presets.required_long_range_sams) + len(
            presets.required_medium_range_sams
        )

    def generate_ground_point(self) -> None:
        try:
            category = random.choice(self.faction.building_set)
        except IndexError:
            logging.exception("Faction has no buildings defined")
            return

        obj_name = namegen.random_objective_name()
        template = random.choice(list(self.templates[category].values()))

        if category == "oil":
            location_type = LocationType.OffshoreStrikeTarget
        else:
            location_type = LocationType.StrikeTarget

        # Pick from preset locations
        point = self.location_finder.location_for(location_type)
        if point is None:
            return

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
                unit["heading"],
                self.control_point,
                unit["type"],
            )

            self.control_point.connected_objectives.append(g)

    def generate_aa_site(self) -> None:
        position = self.location_finder.location_for(LocationType.Sam)
        if position is None:
            return
        self.generate_aa_at(
            position,
            ranges=[
                # Prefer to use proper SAMs, but fall back to SHORADs if needed.
                {AirDefenseRange.Long, AirDefenseRange.Medium},
                {AirDefenseRange.Short},
            ],
        )

    def generate_aa_at(
        self, position: Point, ranges: Iterable[Set[AirDefenseRange]]
    ) -> None:
        group_id = self.game.next_group_id()

        g = SamGroundObject(
            namegen.random_objective_name(),
            group_id,
            position,
            self.control_point,
            for_airbase=False,
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

    def generate_missile_sites(self) -> None:
        for i in range(self.faction.missiles_group_count):
            self.generate_missile_site()

    def generate_missile_site(self) -> None:
        position = self.location_finder.location_for(LocationType.MissileSite)
        if position is None:
            return

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
        for i in range(self.faction.coastal_group_count):
            self.generate_coastal_site()

    def generate_coastal_site(self) -> None:
        position = self.location_finder.location_for(LocationType.Coastal)
        if position is None:
            return

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


class FobGroundObjectGenerator(AirbaseGroundObjectGenerator):
    def generate(self) -> bool:
        self.generate_fob()
        FobDefenseGenerator(self.game, self.control_point).generate()
        self.generate_required_aa()
        return True

    def generate_fob(self) -> None:
        try:
            category = self.faction.building_set[self.faction.building_set.index("fob")]
        except IndexError:
            logging.exception("Faction has no fob buildings defined")
            return

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
                unit["heading"],
                self.control_point,
                unit["type"],
                airbase_group=True,
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
