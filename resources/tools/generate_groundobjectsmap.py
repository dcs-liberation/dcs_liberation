import pickle
import typing

from dcs.mission import Mission
from dcs.mapping import Point
from dcs.unitgroup import VehicleGroup, StaticGroup
from dcs.unit import *
from dcs.statics import warehouse_map, fortification_map

from game import db
from gen.groundobjectsgen import TheaterGroundObject

m = Mission()
m.load_file("./cau_groundobjects.miz")


def parse_name(name: str) -> int:
    first_part = name.split()[0].split("|")
    return int(first_part[0]) if len(first_part) == 1 else int(first_part[1])


if __name__ == "__main__":
    theater_objects = []

    for group in m.country("Russia").static_group + m.country("Russia").vehicle_group:
        for unit in group.units:
            theater_object = TheaterGroundObject()
            theater_object.object_id = len(theater_objects) + 1

            try:
                theater_object.cp_id = parse_name(str(unit.name))
            except Exception as e:
                theater_object.cp_id = parse_name(str(group.name))

            theater_object.position = unit.position
            theater_object.heading = unit.heading

            if isinstance(unit, Vehicle):
                theater_object.dcs_identifier = "AA"
            else:
                theater_object.dcs_identifier = unit.type

            airport_distance = m.terrain.airport_by_id(theater_object.cp_id).position.distance_to_point(theater_object.position)
            if airport_distance > 150000:
                print("Object {} {} is placed {}m from airport {}!".format(theater_object.dcs_identifier,
                                                                           group.name,
                                                                           airport_distance,
                                                                           m.terrain.airport_by_id(theater_object.cp_id)))

            assert theater_object.dcs_identifier
            assert theater_object.cp_id
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
                elif object_b.group_id:
                    object_a.group_id = object_b.group_id
                else:
                    object_a.group_id = group_ids
                    object_b.group_id = group_ids
                    group_ids += 1

                assert object_a.cp_id == object_b.cp_id, "Object {} and {} are placed in group with different airports!".format(object_a.string_identifier, object_b.string_identifier)

    for a in theater_objects:
        if not a.group_id:
            a.group_id = group_ids
            group_ids += 1

    print("Total {} objects".format(len(theater_objects)))
    with open("../cau_groundobjects.p", "wb") as f:
        result = {}
        for theater_object in theater_objects:
            if theater_object.cp_id not in result:
                result[theater_object.cp_id] = []
            result[theater_object.cp_id].append(theater_object)

        pickle.dump(result, f)

