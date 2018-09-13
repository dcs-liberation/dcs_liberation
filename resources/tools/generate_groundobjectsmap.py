import pickle
import typing

from dcs.mission import Mission
from dcs.mapping import Point
from dcs.terrain import *
from dcs.unitgroup import VehicleGroup, StaticGroup
from dcs.unit import *
from dcs.statics import warehouse_map, fortification_map

from game import db
from gen.groundobjectsgen import TheaterGroundObject
from theater.caucasus import CaucasusTheater
from theater.persiangulf import PersianGulfTheater
from theater.nevada import NevadaTheater

m = Mission()
m.load_file("resources/tools/cau_groundobjects.miz")

if isinstance(m.terrain, Caucasus):
    theater = CaucasusTheater(load_ground_objects=False)
elif isinstance(m.terrain, PersianGulf):
    theater = PersianGulfTheater(load_ground_objects=False)
elif isinstance(m.terrain, Nevada):
    theater = NevadaTheater(load_ground_objects=False)
else:
    assert False


def closest_cp(location: Point) -> (int, float):
    global theater
    min_distance, min_cp = None, None

    for cp in theater.controlpoints:
        if not min_distance or location.distance_to_point(cp.position) < min_distance:
            min_distance = location.distance_to_point(cp.position)
            min_cp = cp.id

    assert min_cp is not None
    return min_cp


if __name__ == "__main__":
    theater_objects = []

    for group in m.country("Russia").static_group + m.country("Russia").vehicle_group:
        for unit in group.units:
            theater_object = TheaterGroundObject()
            theater_object.object_id = len(theater_objects) + 1

            theater_object.position = unit.position
            theater_object.heading = unit.heading

            if isinstance(unit, Vehicle):
                theater_object.dcs_identifier = "AA"
            else:
                theater_object.dcs_identifier = unit.type

            assert theater_object.dcs_identifier
            assert theater_object.object_id

            theater_objects.append(theater_object)

    group_ids = 1
    for object_a in theater_objects:
        for object_b in theater_objects:
            if object_a.position.distance_to_point(object_b.position) < 2000:
                if object_a.group_id and object_b.group_id:
                    continue
                elif object_a.group_id:
                    object_b.group_id = object_a.group_id
                    object_b.cp_id = object_a.cp_id
                elif object_b.group_id:
                    object_a.group_id = object_b.group_id
                    object_a.cp_id = object_b.cp_id
                else:
                    object_a.group_id = group_ids
                    object_b.group_id = group_ids
                    object_a.cp_id = closest_cp(object_a.position)
                    object_b.cp_id = object_a.cp_id
                    group_ids += 1

                assert object_a.cp_id == object_b.cp_id, "Object {} and {} are placed in group with different airports!".format(object_a.string_identifier, object_b.string_identifier)

    for a in theater_objects:
        if not a.group_id:
            a.group_id = group_ids
            a.cp_id = closest_cp(a.position)
            group_ids += 1

    with open("resources/cau_groundobjects.p", "wb") as f:
        result = {}
        for theater_object in theater_objects:
            assert theater_object.cp_id
            assert theater_object.group_id
            assert theater_object.object_id

            if theater_object.cp_id not in result:
                result[theater_object.cp_id] = []
            result[theater_object.cp_id].append(theater_object)

        print("Total {} objects".format(len(theater_objects)))
        for cp_id, objects in result.items():
            print("{}: total {} objects".format(m.terrain.airport_by_id(cp_id), len(objects)))

        pickle.dump(result, f)

