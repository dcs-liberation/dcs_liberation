import typing

from dcs.mission import *
from dcs.terrain import *

from theater.nevada import *
from theater.persiangulf import *
from theater.caucasus import *
from theater.controlpoint import *

def find_ground_location(near, theater, max, min) -> typing.Optional[Point]:
    for _ in range(500):
        p = near.random_point_within(max, min)
        if theater.is_on_land(p):
            return p

    return None


mission = Mission(Nevada())
theater = NevadaTheater()

for cp in theater.enemy_points():
    for _ in range(0, random.randrange(3, 6)):
        p = find_ground_location(cp.position, theater, 120000, 5000)
        if not p:
            print("Didn't find ground location for {}".format(cp))
            continue

        mission.flight_group_inflight(
            mission.country("USA"),
            "",
            A_10C,
            p,
            10000
        )

mission.save("resources/tools/ground_objects_example.miz")
