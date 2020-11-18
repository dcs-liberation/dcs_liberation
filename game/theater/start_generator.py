from __future__ import annotations

import logging
import math
import pickle
import random
from typing import Any, Dict, List, Optional

from dcs.mapping import Point
from dcs.task import CAP, CAS, PinpointStrike
from dcs.vehicles import AirDefence

from game import Game, db
from game.factions.faction import Faction
from game.settings import Settings
from game.version import VERSION
from gen import namegen
from gen.defenses.armor_group_generator import generate_armor_group
from gen.fleet.ship_group_generator import (
    generate_carrier_group,
    generate_lha_group,
    generate_ship_group,
)
from gen.locations.preset_location_finder import PresetLocationFinder
from gen.locations.preset_locations import PresetLocation
from gen.missiles.missiles_group_generator import generate_missile_group
from gen.sam.sam_group_generator import (
    generate_anti_air_group,
    generate_ewr_group, generate_shorad_group,
)
from theater import (
    ConflictTheater,
    ControlPoint,
    ControlPointType,
    TheaterGroundObject,
)
from game.theater.conflicttheater import IMPORTANCE_HIGH, IMPORTANCE_LOW
from game.theater.theatergroundobject import (
    EwrGroundObject,
    SamGroundObject,
    BuildingGroundObject,
    CarrierGroundObject,
    LhaGroundObject,
    MissileSiteGroundObject,
    ShipGroundObject,
    VehicleGroupGroundObject,
)

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


class GameGenerator:
    def __init__(self, player: str, enemy: str, theater: ConflictTheater,
                 settings: Settings, start_date, starting_budget: int,
                 multiplier: float, midgame: bool) -> None:
        self.player = player
        self.enemy = enemy
        self.theater = theater
        self.settings = settings
        self.start_date = start_date
        self.starting_budget = starting_budget
        self.multiplier = multiplier
        self.midgame = midgame

    def generate(self) -> Game:
        # Reset name generator
        namegen.reset()
        self.prepare_theater()
        self.populate_red_airbases()
        game = Game(player_name=self.player,
                    enemy_name=self.enemy,
                    theater=self.theater,
                    start_date=self.start_date,
                    settings=self.settings)

        GroundObjectGenerator(game).generate()
        game.budget = self.starting_budget
        game.settings.multiplier = self.multiplier
        game.settings.sams = True
        game.settings.version = VERSION
        return game

    def prepare_theater(self) -> None:
        to_remove = []
        # Auto-capture half the bases if midgame.
        if self.midgame:
            control_points = self.theater.controlpoints
            for control_point in control_points[:len(control_points) // 2]:
                control_point.captured = True

        # Remove carrier and lha, invert situation if needed
        for cp in self.theater.controlpoints:
            no_carrier = self.settings.do_not_generate_carrier
            no_lha = self.settings.do_not_generate_lha
            if cp.cptype is ControlPointType.AIRCRAFT_CARRIER_GROUP and \
                    no_carrier:
                to_remove.append(cp)
            elif cp.cptype is ControlPointType.LHA_GROUP and no_lha:
                to_remove.append(cp)

            if self.settings.inverted:
                cp.captured = cp.captured_invert

        # do remove
        for cp in to_remove:
            self.theater.controlpoints.remove(cp)

        # TODO: Fix this. This captures all bases for blue.
        # reapply midgame inverted if needed
        if self.midgame and self.settings.inverted:
            for i, cp in enumerate(reversed(self.theater.controlpoints)):
                if i > len(self.theater.controlpoints):
                    break
                else:
                    cp.captured = True

    def populate_red_airbases(self) -> None:
        for control_point in self.theater.enemy_points():
            if control_point.captured:
                continue
            self.populate_red_airbase(control_point)

    def populate_red_airbase(self, control_point: ControlPoint) -> None:
        # Force reset cp on generation
        control_point.base.aircraft = {}
        control_point.base.armor = {}
        control_point.base.aa = {}
        control_point.base.commision_points = {}
        control_point.base.strength = 1

        for task in [PinpointStrike, CAP, CAS, AirDefence]:
            if IMPORTANCE_HIGH <= control_point.importance <= IMPORTANCE_LOW:
                raise ValueError(
                    f"CP importance must be between {IMPORTANCE_LOW} and "
                    f"{IMPORTANCE_HIGH}, is {control_point.importance}")

            importance_factor = ((control_point.importance - IMPORTANCE_LOW) /
                                 (IMPORTANCE_HIGH - IMPORTANCE_LOW))
            # noinspection PyTypeChecker
            unit_types = db.choose_units(task, importance_factor, UNIT_VARIETY,
                                         self.enemy)
            if not unit_types:
                continue

            count_log = math.log(control_point.importance + 0.01,
                                 UNIT_COUNT_IMPORTANCE_LOG)
            count = max(
                COUNT_BY_TASK[task] * self.multiplier * (1 + count_log), 1
            )

            count_per_type = max(int(float(count) / len(unit_types)), 1)
            for unit_type in unit_types:
                control_point.base.commision_units({unit_type: count_per_type})


class ControlPointGroundObjectGenerator:
    def __init__(self, game: Game, control_point: ControlPoint) -> None:
        self.game = game
        self.control_point = control_point
        self.preset_locations = PresetLocationFinder.compute_possible_locations(game.theater.terrain.name, control_point.full_name)

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
        skip_player_navy = self.game.settings.do_not_generate_player_navy
        if self.control_point.captured and skip_player_navy:
            return

        skip_enemy_navy = self.game.settings.do_not_generate_enemy_navy
        if not self.control_point.captured and skip_enemy_navy:
            return

        for _ in range(self.faction.navy_group_count):
            self.generate_ship()

    def generate_ship(self) -> None:
        point = find_location(False, self.control_point.position,
                              self.game.theater, 5000, 40000, [], False)
        if point is None:
            logging.error(
                f"Could not find point for {self.control_point}'s navy")
            return

        group_id = self.game.next_group_id()

        g = ShipGroundObject(namegen.random_objective_name(), group_id, point,
                             self.control_point)

        group = generate_ship_group(self.game, g, self.faction_name)
        g.groups = []
        if group is not None:
            g.groups.append(group)
            self.control_point.connected_objectives.append(g)

    def pick_preset_location(self, offshore=False) -> Optional[PresetLocation]:
        """
        Return a preset location if any is setup and still available for this point
        @:param offshore Whether this should be an offshore location
        @:return The preset location if found; None if it couldn't be found
        """
        if offshore:
            if len(self.preset_locations.offshore_locations) > 0:
                location = random.choice(self.preset_locations.offshore_locations)
                self.preset_locations.offshore_locations.remove(location)
                logging.info("Picked a preset offshore location")
                return location
        else:
            if len(self.preset_locations.ashore_locations) > 0:
                location = random.choice(self.preset_locations.ashore_locations)
                self.preset_locations.ashore_locations.remove(location)
                logging.info("Picked a preset ashore location")
                return location
        logging.info("No preset location found")
        return None


class CarrierGroundObjectGenerator(ControlPointGroundObjectGenerator):
    def generate(self) -> bool:
        if not super().generate():
            return False

        carrier_names = self.faction.carrier_names
        if not carrier_names:
            logging.info(
                f"Skipping generation of {self.control_point.name} because "
                f"{self.faction_name} has no carriers")
            return False

        # Create ground object group
        group_id = self.game.next_group_id()
        g = CarrierGroundObject(namegen.random_objective_name(), group_id,
                                self.control_point)
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
                f"{self.faction_name} has no LHAs")
            return False

        # Create ground object group
        group_id = self.game.next_group_id()
        g = LhaGroundObject(namegen.random_objective_name(), group_id,
                            self.control_point)
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
        position = self._find_location()
        if position is None:
            logging.error("Could not find position for "
                          f"{self.control_point} EWR")
            return

        group_id = self.game.next_group_id()

        g = EwrGroundObject(namegen.random_objective_name(), group_id,
                            position, self.control_point)

        group = generate_ewr_group(self.game, g, self.faction_name)
        if group is None:
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
        position = self._find_location()
        if position is None:
            logging.error("Could not find position for "
                          f"{self.control_point} garrison")
            return

        group_id = self.game.next_group_id()

        g = VehicleGroupGroundObject(namegen.random_objective_name(), group_id,
                                     position, self.control_point,
                                     for_airbase=True)

        group = generate_armor_group(self.faction_name, self.game, g)
        if group is not None:
            g.groups.append(group)
        self.control_point.base_defenses.append(g)

    def generate_sam(self) -> None:
        position = self._find_location()
        if position is None:
            logging.error("Could not find position for "
                          f"{self.control_point} SAM")
            return

        group_id = self.game.next_group_id()

        g = SamGroundObject(namegen.random_objective_name(), group_id,
                            position, self.control_point, for_airbase=True)

        group = generate_anti_air_group(self.game, g, self.faction_name)
        if group is not None:
            g.groups.append(group)
        self.control_point.base_defenses.append(g)

    def generate_shorad(self) -> None:
        position = self._find_location()
        if position is None:
            logging.error("Could not find position for "
                          f"{self.control_point} SHORAD")
            return

        group_id = self.game.next_group_id()

        g = SamGroundObject(namegen.random_objective_name(), group_id,
                            position, self.control_point, for_airbase=True)

        group = generate_shorad_group(self.game, g, self.faction_name)
        if group is not None:
            g.groups.append(group)
        self.control_point.base_defenses.append(g)

    def _find_location(self) -> Optional[Point]:
        position = find_location(True, self.control_point.position,
                                 self.game.theater, 400, 3200, [], True)

        # Retry once, searching a bit further (On some big airbase, 3200 is too short (Ex : Incirlik))
        # But searching farther on every base would be problematic, as some base defense units
        # would end up very far away from small airfields.
        # (I know it's not good for performance, but this is only done on campaign generation)
        # TODO : Make the whole process less stupid with preset possible positions for each airbase
        if position is None:
            position = find_location(True, self.control_point.position,
                                     self.game.theater, 3200, 4800, [], True)
        return position


class AirbaseGroundObjectGenerator(ControlPointGroundObjectGenerator):
    def __init__(self, game: Game, control_point: ControlPoint,
                 templates: GroundObjectTemplates) -> None:
        super().__init__(game, control_point)
        self.templates = templates

    def generate(self) -> bool:
        if not super().generate():
            return False

        BaseDefenseGenerator(self.game, self.control_point).generate()
        self.generate_ground_points()

        if self.faction.missiles:
            self.generate_missile_sites()

        return True

    def generate_ground_points(self) -> None:
        """Generate ground objects and AA sites for the control point."""
        if self.control_point.is_global:
            return

        # Always generate at least one AA point.
        self.generate_aa_site()

        # And between 2 and 7 other objectives.
        amount = random.randrange(2, 7)
        for i in range(amount):
            # 1 in 4 additional objectives are AA.
            if random.randint(0, 3) == 0:
                self.generate_aa_site()
            else:
                self.generate_ground_point()

    def generate_ground_point(self) -> None:
        try:
            category = random.choice(self.faction.building_set)
        except IndexError:
            logging.exception("Faction has no buildings defined")
            return

        obj_name = namegen.random_objective_name()
        template = random.choice(list(self.templates[category].values()))

        offshore = category == "oil"

        # Pick from preset locations
        location = self.pick_preset_location(offshore)

        # Else try the old algorithm
        if location is None:
            point = find_location(not offshore,
                                  self.control_point.position,
                                  self.game.theater, 10000, 40000,
                                  self.control_point.ground_objects)
        else:
            point = location.position

        if point is None:
            logging.error(
                f"Could not find point for {obj_name} at {self.control_point}")
            return

        object_id = 0
        group_id = self.game.next_group_id()

        # TODO: Create only one TGO per objective, each with multiple units.
        for unit in template:
            object_id += 1

            template_point = Point(unit["offset"].x, unit["offset"].y)
            g = BuildingGroundObject(
                obj_name, category, group_id, object_id, point + template_point,
                unit["heading"], self.control_point, unit["type"])

            self.control_point.connected_objectives.append(g)

    def generate_aa_site(self) -> None:
        obj_name = namegen.random_objective_name()

        # Pick from preset locations
        location = self.pick_preset_location(False)

        # If no preset location, then try the old algorithm
        if location is None:
            position = find_location(True, self.control_point.position,
                                 self.game.theater, 10000, 40000,
                                 self.control_point.ground_objects)
        else:
            position = location.position

        if position is None:
            logging.error(
                f"Could not find point for {obj_name} at {self.control_point}")
            return

        group_id = self.game.next_group_id()

        g = SamGroundObject(namegen.random_objective_name(), group_id,
                            position, self.control_point, for_airbase=False)
        group = generate_anti_air_group(self.game, g, self.faction_name)
        if group is not None:
            g.groups = [group]
        self.control_point.connected_objectives.append(g)

    def generate_missile_sites(self) -> None:
        for i in range(self.faction.missiles_group_count):
            self.generate_missile_site()

    def generate_missile_site(self) -> None:

        # Pick from preset locations
        location = self.pick_preset_location(False)

        # If no preset location, then try the old algorithm
        if location is None:
            position = find_location(True, self.control_point.position,
                                     self.game.theater, 2500, 40000,
                                     [], False)
        else:
            position = location.position


        if position is None:
            logging.info(
                f"Could not find point for {self.control_point} missile site")
            return

        group_id = self.game.next_group_id()

        g = MissileSiteGroundObject(namegen.random_objective_name(), group_id,
                                    position, self.control_point)
        group = generate_missile_group(self.game, g, self.faction_name)
        g.groups = []
        if group is not None:
            g.groups.append(group)
            self.control_point.connected_objectives.append(g)
        return


class GroundObjectGenerator:
    def __init__(self, game: Game) -> None:
        self.game = game
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
            generator = CarrierGroundObjectGenerator(self.game, control_point)
        elif control_point.cptype == ControlPointType.LHA_GROUP:
            generator = LhaGroundObjectGenerator(self.game, control_point)
        else:
            generator = AirbaseGroundObjectGenerator(self.game, control_point,
                                                     self.templates)
        return generator.generate()


# TODO: https://stackoverflow.com/a/19482012/632035
# A lot of the time spent on mission generation is spent in this function since
# just randomly guess up to 1800 times and often fail. This is particularly
# problematic while trying to find placement for navies in Nevada.
def find_location(on_ground: bool, near: Point, theater: ConflictTheater,
                  min_range: int, max_range: int,
                  others: List[TheaterGroundObject],
                  is_base_defense: bool = False) -> Optional[Point]:
    """
    Find a valid ground object location
    :param on_ground: Whether it should be on ground or on sea (True = on
    ground)
    :param near: Point
    :param theater: Theater object
    :param min_range: Minimal range from point
    :param max_range: Max range from point
    :param others: Other already existing ground objects
    :param is_base_defense: True if the location is for base defense.
    :return:
    """
    point = None
    for _ in range(300):

        # Check if on land or sea
        p = near.random_point_within(max_range, min_range)
        if on_ground and theater.is_on_land(p):
            point = p
        elif not on_ground and theater.is_in_sea(p):
            point = p

        if point:
            for angle in range(0, 360, 45):
                p = point.point_from_heading(angle, 2500)
                if on_ground and not theater.is_on_land(p):
                    point = None
                    break
                elif not on_ground and not theater.is_in_sea(p):
                    point = None
                    break
        if point:
            for other in others:
                if other.position.distance_to_point(point) < 10000:
                    point = None
                    break

        if point:
            for control_point in theater.controlpoints:
                if is_base_defense:
                    break
                if control_point.position != near:
                    if point is None:
                        break
                    if control_point.position.distance_to_point(point) < 30000:
                        point = None
                        break
                    for ground_obj in control_point.ground_objects:
                        if ground_obj.position.distance_to_point(point) < 10000:
                            point = None
                            break

        if point:
            return point
    return None
