import math
import pickle
import random
import typing
import logging

from gen import namegen
from gen.defenses.armor_group_generator import generate_armor_group
from gen.fleet.ship_group_generator import generate_carrier_group, generate_lha_group
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
    for cp in theater.controlpoints:
        group_id = generate_cp_ground_points(cp, theater, game, group_id, tpls)

        # CP
        if cp.captured:
            faction = game.player_name
        else:
            faction = game.enemy_name

        if cp.cptype == ControlPointType.AIRCRAFT_CARRIER_GROUP:
            # Create ground object group
            group_id = group_id + 1
            g = TheaterGroundObject()
            g.group_id = group_id
            g.object_id = 0
            g.cp_id = cp.id
            g.airbase_group = True
            g.dcs_identifier = "CARRIER"
            g.obj_name = namegen.random_objective_name()
            g.heading = 0
            g.position = Point(cp.position.x, cp.position.y)
            group = generate_carrier_group(faction, game, g)
            g.groups = []
            if group is not None:
                g.groups.append(group)
            cp.ground_objects.append(g)
            # Set new name :
            if "carrier_names" in db.FACTIONS[faction]:
                cp.name = random.choice(db.FACTIONS[faction]["carrier_names"])
        elif cp.cptype == ControlPointType.LHA_GROUP:
            # Create ground object group
            group_id = group_id + 1
            g = TheaterGroundObject()
            g.group_id = group_id
            g.object_id = 0
            g.cp_id = cp.id
            g.airbase_group = True
            g.dcs_identifier = "LHA"
            g.obj_name = namegen.random_objective_name()
            g.heading = 0
            g.position = Point(cp.position.x, cp.position.y)
            group = generate_lha_group(faction, game, g)
            g.groups = []
            if group is not None:
                g.groups.append(group)
            cp.ground_objects.append(g)
            # Set new name :
            if "lhanames" in db.FACTIONS[faction]:
                cp.name = random.choice(db.FACTIONS[faction]["lhanames"])
        else:



            for i in range(random.randint(2,6)):
                point = find_location(True, cp.position, theater, 1000, 2800, [])

                if point is None:
                    print("Couldn't find point for {}".format(cp))
                    continue

                group_id = group_id + 1

                g = TheaterGroundObject()
                g.group_id = group_id
                g.object_id = 0
                g.cp_id = cp.id
                g.airbase_group = True
                g.dcs_identifier = "AA"
                g.obj_name = namegen.random_objective_name()
                g.heading = 0
                g.position = Point(point.x, point.y)

                generate_airbase_defense_group(i, g, faction, game, cp)
                cp.ground_objects.append(g)

            print("---------------------------")
            print("CP Generation : " + cp.name)
            for ground_object in cp.ground_objects:
                print(ground_object.groups)


def generate_airbase_defense_group(airbase_defense_group_id, ground_obj:TheaterGroundObject, faction, game, cp):

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


def find_location(on_ground, near, theater, min, max, others) -> typing.Optional[Point]:
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

    amount = random.randrange(3, 8)
    for i in range(0, amount):

        available_categories = list(templates)
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
            print("Couldn't find point for {}".format(cp))
            continue

        object_id = 0
        group_id = group_id + 1

        logging.info("generated {} for {}".format(tpl_category, cp))

        for object in tpl:
            object_id += 1

            g = TheaterGroundObject()
            g.group_id = group_id
            g.object_id = object_id
            g.cp_id = cp.id
            g.airbase_group = False
            g.obj_name = obj_name

            g.dcs_identifier = object["type"]
            g.heading = object["heading"]
            g.position = Point(point.x + object["offset"].x, point.y + object["offset"].y)

            #if g.dcs_identifier == "AA":
            #    if cp.captured:
            #        faction = game.player_name
            #    else:
            #        faction = game.enemy_name
            #    g.groups = []
            #    group = generate_anti_air_group(game, cp, g, faction)
            #    if group is not None:
            #        g.groups.append(group)

            cp.ground_objects.append(g)
    return group_id
