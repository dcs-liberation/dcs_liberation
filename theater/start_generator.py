import math
import pickle
import random
import typing

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


def generate_inital_units(theater: ConflictTheater, enemy: str, sams: bool, multiplier: float):
    for cp in theater.enemy_points():
        if cp.captured:
            continue

        for task in [PinpointStrike, CAP, CAS, AirDefence]:
            assert cp.importance <= IMPORTANCE_HIGH, "invalid importance {}".format(cp.importance)
            assert cp.importance >= IMPORTANCE_LOW, "invalid importance {}".format(cp.importance)

            importance_factor = (cp.importance - IMPORTANCE_LOW) / (IMPORTANCE_HIGH - IMPORTANCE_LOW)
            variety = int(UNIT_VARIETY)
            unittypes = db.choose_units(task, importance_factor, variety, enemy)

            if not sams and task == AirDefence:
                unittypes = [x for x in db.find_unittype(AirDefence, enemy) if x not in db.SAM_BAN]

            count_log = math.log(cp.importance + 0.01, UNIT_COUNT_IMPORTANCE_LOG)
            count = max(COUNT_BY_TASK[task] * multiplier * (1+count_log), 1)
            count_per_type = max(int(float(count) / len(unittypes)), 1)
            for unit_type in unittypes:
                logging.info("{} - {} {}".format(cp.name, db.unit_type_name(unit_type), count_per_type))
                cp.base.commision_units({unit_type: count_per_type})


def generate_groundobjects(theater: ConflictTheater):
    with open("resources/groundobject_templates.p", "rb") as f:
        tpls = pickle.load(f)

    def find_location(on_ground, near, theater, min, max) -> typing.Optional[Point]:
        point = None
        for _ in range(1000):
            p = near.random_point_within(max, min)
            if on_ground and theater.is_on_land(p):
                point = p
            elif not on_ground and theater.is_in_sea(p):
                point = p

            if point:
                for angle in range(0, 360, 45):
                    p = point.point_from_heading(angle, 1000)
                    if on_ground and not theater.is_on_land(p):
                        point = None
                        break
                    elif not on_ground and not theater.is_in_sea(p):
                        point = None
                        break

            if point:
                return point

        return None

    group_id = 0
    for cp in theater.enemy_points():
        for _ in range(0, random.randrange(3, 6)):
            available_categories = list(tpls) + ["aa", "aa", "aa"]
            tpl_category = random.choice(available_categories)

            tpl = random.choice(list(tpls[tpl_category].values()))

            point = find_location(tpl_category != "oil", cp.position, theater, 15000, 80000)

            if point is None:
                print("Couldn't find point for {}".format(cp))
                continue

            dist = point.distance_to_point(cp.position)
            for another_cp in theater.enemy_points():
                if another_cp.position.distance_to_point(point) < dist:
                    cp = another_cp

            group_id += 1
            object_id = 0

            for object in tpl:
                object_id += 1

                g = TheaterGroundObject()
                g.group_id = group_id
                g.object_id = object_id
                g.cp_id = cp.id

                g.dcs_identifier = object["type"]
                g.heading = object["heading"]
                g.position = Point(point.x + object["offset"].x, point.y + object["offset"].y)

                cp.ground_objects.append(g)
