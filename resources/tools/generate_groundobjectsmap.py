import pickle
import typing

from game import db
from gen.groundobjectsgen import TheaterGroundObject
from dcs.mission import Mission
from dcs.terrain import PersianGulf

m = Mission()
m.load_file("./cau_groundobjects.miz")

result = {}


def append_group(cp_id, category, group_id, object_id, position, heading):
    global result

    if cp_id not in result:
        result[cp_id] = []

    result[cp_id].append(TheaterGroundObject(category, cp_id, group_id, object_id, position, heading))


def parse_name(name: str) -> typing.Tuple:
    args = str(name).split("|")
    if len(args) == 3:
        args.append("1")

    return args[0], int(args[1]), int(args[2]), int(args[3])


for group in m.country("Russia").static_group + m.country("Russia").vehicle_group:
    try:
        category, cp_id, group_id, object_id = parse_name(str(group.name))
    except:
        print("Failed to parse {}".format(group.name))
        continue

    append_group(cp_id, category, group_id, object_id, [group.position.x, group.position.y], group.units[0].heading)

print("Total {} objects".format(sum([len(x) for x in result.values()])))
with open("../cau_groundobjects.p", "wb") as f:
    pickle.dump(result, f)

