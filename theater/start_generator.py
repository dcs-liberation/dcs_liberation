import math
import pickle
import random
import typing
import logging

from game.data.building_data import DEFAULT_AVAILABLE_BUILDINGS
from game.settings import Settings
from gen import namegen, TheaterGroundObject
from gen.defenses.armor_group_generator import generate_armor_group
from gen.fleet.ship_group_generator import generate_carrier_group, generate_lha_group, generate_ship_group
from gen.missiles.missiles_group_generator import generate_missile_group
from gen.sam.sam_group_generator import generate_anti_air_group, generate_shorad_group
from theater import ControlPointType
from theater.base import *
from theater.conflicttheater import *

UNIT_VARIETY = 3
UNIT_AMOUNT_FACTOR = 16
UNIT_COUNT_IMPORTANCE_LOG = 1.3

COUNT_BY_TASK = {
    PinpointStrike: 12,
    CAP: 8,
    CAS: 4,
    AirDefence: 1,
}


def generate_inital_units(theater: ConflictTheater, enemy_country: str, sams: bool, multiplier: float):
    for cp in theater.enemy_points():
        if cp.captured:
            continue

        # Force reset cp on generation
        cp.base.aircraft = {}
        cp.base.armor = {}
        cp.base.aa = {}
        cp.base.commision_points = {}
        cp.base.strength = 1

        for task in [PinpointStrike, CAP, CAS, AirDefence]:
            assert cp.importance <= IMPORTANCE_HIGH, "invalid importance {}".format(cp.importance)
            assert cp.importance >= IMPORTANCE_LOW, "invalid importance {}".format(cp.importance)

            importance_factor = (cp.importance - IMPORTANCE_LOW) / (IMPORTANCE_HIGH - IMPORTANCE_LOW)
            variety = int(UNIT_VARIETY)
            unittypes = db.choose_units(task, importance_factor, variety, enemy_country)

            if not sams and task == AirDefence:
                unittypes = [x for x in db.find_unittype(AirDefence, enemy_country) if x not in db.SAM_BAN]

            count_log = math.log(cp.importance + 0.01, UNIT_COUNT_IMPORTANCE_LOG)
            count = max(COUNT_BY_TASK[task] * multiplier * (1+count_log), 1)

            if len(unittypes) > 0:
                count_per_type = max(int(float(count) / len(unittypes)), 1)
                for unit_type in unittypes:
                    logging.info("{} - {} {}".format(cp.name, db.unit_type_name(unit_type), count_per_type))
                    cp.base.commision_units({unit_type: count_per_type})


def generate_groundobjects(theater: ConflictTheater, game):
    with open("resources/groundobject_templates.p", "rb") as f:
        tpls = pickle.load(f)

    group_id = 0
    cp_to_remove = []
    for cp in theater.controlpoints:
        group_id = generate_cp_ground_points(cp, theater, game, group_id, tpls)

        # CP
        if cp.captured:
            faction_name = game.player_name
        else:
            faction_name = game.enemy_name

        if cp.cptype == ControlPointType.AIRCRAFT_CARRIER_GROUP:
            # Create ground object group
            group_id = game.next_group_id()
            g = TheaterGroundObject("CARRIER")
            g.group_id = group_id
            g.object_id = 0
            g.cp_id = cp.id
            g.airbase_group = True
            g.dcs_identifier = "CARRIER"
            g.sea_object = True
            g.obj_name = namegen.random_objective_name()
            g.heading = 0
            g.position = Point(cp.position.x, cp.position.y)
            group = generate_carrier_group(faction_name, game, g)
            g.groups = []
            if group is not None:
                g.groups.append(group)
            cp.ground_objects.append(g)
            # Set new name :
            if "carrier_names" in db.FACTIONS[faction_name]:
                cp.name = random.choice(db.FACTIONS[faction_name]["carrier_names"])
            else:
                cp_to_remove.append(cp)
        elif cp.cptype == ControlPointType.LHA_GROUP:
            # Create ground object group
            group_id = game.next_group_id()
            g = TheaterGroundObject("LHA")
            g.group_id = group_id
            g.object_id = 0
            g.cp_id = cp.id
            g.airbase_group = True
            g.dcs_identifier = "LHA"
            g.sea_object = True
            g.obj_name = namegen.random_objective_name()
            g.heading = 0
            g.position = Point(cp.position.x, cp.position.y)
            group = generate_lha_group(faction_name, game, g)
            g.groups = []
            if group is not None:
                g.groups.append(group)
            cp.ground_objects.append(g)
            # Set new name :
            if "lhanames" in db.FACTIONS[faction_name]:
                cp.name = random.choice(db.FACTIONS[faction_name]["lhanames"])
            else:
                cp_to_remove.append(cp)
        else:

            for i in range(random.randint(3,6)):

                logging.info("GENERATE BASE DEFENSE")
                point = find_location(True, cp.position, theater, 1000, 2800, [], True)
                logging.info(point)

                if point is None:
                    logging.info("Couldn't find point for {} base defense".format(cp))
                    continue

                group_id = game.next_group_id()

                g = TheaterGroundObject("aa")
                g.group_id = group_id
                g.object_id = 0
                g.cp_id = cp.id
                g.airbase_group = True
                g.dcs_identifier = "AA"
                g.sea_object = False
                g.obj_name = namegen.random_objective_name()
                g.heading = 0
                g.position = Point(point.x, point.y)

                generate_airbase_defense_group(i, g, faction_name, game, cp)
                cp.ground_objects.append(g)

            logging.info("---------------------------")
            logging.info("CP Generation : " + cp.name)
            for ground_object in cp.ground_objects:
                logging.info(ground_object.groups)

        # Generate navy groups
        if "boat" in db.FACTIONS[faction_name].keys():

            if cp.captured and game.settings.do_not_generate_player_navy:
                continue

            if not cp.captured and game.settings.do_not_generate_enemy_navy:
                continue

            boat_count = 1
            if "boat_count" in db.FACTIONS[faction_name].keys():
                boat_count = int(db.FACTIONS[faction_name]["boat_count"])

            for i in range(boat_count):

                point = find_location(False, cp.position, theater, 5000, 40000, [], False)

                if point is None:
                    logging.info("Couldn't find point for {} ships".format(cp))
                    continue

                group_id = game.next_group_id()

                g = TheaterGroundObject("aa")
                g.group_id = group_id
                g.object_id = 0
                g.cp_id = cp.id
                g.airbase_group = False
                g.dcs_identifier = "AA"
                g.sea_object = True
                g.obj_name = namegen.random_objective_name()
                g.heading = 0
                g.position = Point(point.x, point.y)

                group = generate_ship_group(game, g, faction_name)
                g.groups = []
                if group is not None:
                    g.groups.append(group)
                    cp.ground_objects.append(g)



        if "missiles" in db.FACTIONS[faction_name].keys():

            missiles_count = 1
            if "missiles_count" in db.FACTIONS[faction_name].keys():
                missiles_count = int(db.FACTIONS[faction_name]["missiles_count"])

            for i in range(missiles_count):

                point = find_location(True, cp.position, theater, 2500, 40000, [], False)

                if point is None:
                    logging.info("Couldn't find point for {} missiles".format(cp))
                    continue

                group_id = game.next_group_id()

                g = TheaterGroundObject("aa")
                g.group_id = group_id
                g.object_id = 0
                g.cp_id = cp.id
                g.airbase_group = False
                g.dcs_identifier = "AA"
                g.sea_object = False
                g.obj_name = namegen.random_objective_name()
                g.heading = 0
                g.position = Point(point.x, point.y)

                group = generate_missile_group(game, g, faction_name)
                g.groups = []
                if group is not None:
                    g.groups.append(group)
                    cp.ground_objects.append(g)

    for cp in cp_to_remove:
        theater.controlpoints.remove(cp)



def generate_airbase_defense_group(airbase_defense_group_id, ground_obj:TheaterGroundObject, faction, game, cp):

    logging.info("GENERATE AIR DEFENSE GROUP")
    logging.info(faction)
    logging.info(airbase_defense_group_id)

    if airbase_defense_group_id == 0:
        group = generate_armor_group(faction, game, ground_obj)
    elif airbase_defense_group_id == 1 and random.randint(0, 1) == 0:
        group = generate_anti_air_group(game, cp, ground_obj, faction)
    elif random.randint(0, 2) == 1:
        group = generate_shorad_group(game, cp, ground_obj, faction)
    else:
        group = generate_armor_group(faction, game, ground_obj)

    ground_obj.groups = []
    if group is not None:
        ground_obj.groups.append(group)


def find_location(on_ground, near, theater, min, max, others, is_base_defense=False) -> typing.Optional[Point]:
    """
    Find a valid ground object location
    :param on_ground: Whether it should be on ground or on sea (True = on ground)
    :param near: Point
    :param theater: Theater object
    :param min: Minimal range from point
    :param max: Max range from point
    :param others: Other already existing ground objects
    :return:
    """
    point = None
    for _ in range(300):

        # Check if on land or sea
        p = near.random_point_within(max, min)
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
            for other in theater.controlpoints:
                if is_base_defense: break
                if other.position != near:
                    if point is None:
                        break
                    if other.position.distance_to_point(point) < 30000:
                        point = None
                        break
                    for ground_obj in other.ground_objects:
                        if ground_obj.position.distance_to_point(point) < 10000:
                            point = None
                            break

        if point:
            return point
    return None


def generate_cp_ground_points(cp: ControlPoint, theater, game, group_id, templates):
    """
    Generate inital ground objects and AA site for given control point
    :param cp: Control point to initialize
    :param theater: Theater
    :param game: Game object
    :param group_id: Group id
    :param templates: Ground object templates
    :return: True if something was generated
    """
    # Reset cp ground objects
    cp.ground_objects = []

    if cp.is_global:
        return False

    if cp.captured:
        faction = game.player_name
    else:
        faction = game.enemy_name
    faction_data = db.FACTIONS[faction]

    available_categories = DEFAULT_AVAILABLE_BUILDINGS
    if "objects" in faction_data.keys():
        available_categories = faction_data["objects"]

    if len(available_categories) == 0:
        return False

    amount = random.randrange(3, 8)
    for i in range(0, amount):

        obj_name = namegen.random_objective_name()

        if i >= amount - 1:
            tpl_category = "aa"
        else:
            if random.randint(0, 3) == 0:
                tpl_category = "aa"
            else:
                tpl_category = random.choice(available_categories)

        tpl = random.choice(list(templates[tpl_category].values()))
        point = find_location(tpl_category != "oil", cp.position, theater, 10000, 40000, cp.ground_objects)

        if point is None:
            logging.info("Couldn't find point for {}".format(cp))
            continue

        object_id = 0
        group_id = game.next_group_id()

        logging.info("generated {} for {}".format(tpl_category, cp))

        for object in tpl:
            object_id += 1

            g = TheaterGroundObject(tpl_category)
            g.group_id = group_id
            g.object_id = object_id
            g.cp_id = cp.id
            g.airbase_group = False
            g.obj_name = obj_name

            g.dcs_identifier = object["type"]
            g.heading = object["heading"]
            g.sea_object = False
            g.position = Point(point.x + object["offset"].x, point.y + object["offset"].y)

            if g.dcs_identifier == "AA":
                g.groups = []
                group = generate_anti_air_group(game, cp, g, faction)
                if group is not None:
                    g.groups.append(group)

            cp.ground_objects.append(g)
    return group_id


def prepare_theater(theater: ConflictTheater, settings:Settings, midgame):

    to_remove = []

    # autocapture half the base if midgame
    if midgame:
        for i in range(0, int(len(theater.controlpoints) / 2)):
            theater.controlpoints[i].captured = True

    # Remove carrier and lha, invert situation if needed
    for cp in theater.controlpoints:
        if cp.cptype is ControlPointType.AIRCRAFT_CARRIER_GROUP and settings.do_not_generate_carrier:
            to_remove.append(cp)
        elif cp.cptype is ControlPointType.LHA_GROUP and settings.do_not_generate_lha:
            to_remove.append(cp)

        if settings.inverted:
            cp.captured = cp.captured_invert

    # do remove
    for cp in to_remove:
        theater.controlpoints.remove(cp)

    # reapply midgame inverted if needed
    if midgame and settings.inverted:
        for i, cp in enumerate(reversed(theater.controlpoints)):
            if i > len(theater.controlpoints):
                break
            else:
                cp.captured = True


