import math
import pickle
import random
import typing
import logging

from gen.sam.sam_group_generator import generate_anti_air_group
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
    for _ in range(1000):
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

    amount = random.randrange(1, 11)
    for i in range(0, amount):
        available_categories = list(templates)
        if i >= amount - 1:
            tpl_category = "aa"
        else:
            if random.randint(0, 1) == 1:
                tpl_category = random.choice(available_categories)
            else:
                tpl_category = "aa"

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

            g.dcs_identifier = object["type"]
            g.heading = object["heading"]
            g.position = Point(point.x + object["offset"].x, point.y + object["offset"].y)

            if g.dcs_identifier == "AA":
                if cp.captured:
                    faction = game.player_name
                else:
                    faction = game.enemy_name
                generate_anti_air_group(game, cp, g, faction)

            cp.ground_objects.append(g)
    return group_id