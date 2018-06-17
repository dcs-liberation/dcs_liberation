import math

from theater.base import *
from theater.conflicttheater import *

UNIT_VARIETY = 3
UNIT_AMOUNT_FACTOR = 16

COUNT_BY_TASK = {
    PinpointStrike: 24,
    CAP: 16,
    CAS: 8,
    AirDefence: 0.5,
}


def generate_initial(theater: ConflictTheater, enemy: str, sams: bool):
    for cp in theater.enemy_points():
        if cp.captured:
            continue

        for task in [PinpointStrike, CAP, CAS, AirDefence]:
            assert cp.importance <= IMPORTANCE_HIGH, "invalid importance {}".format(cp.importance)
            assert cp.importance >= IMPORTANCE_LOW, "invalid importance {}".format(cp.importance)

            importance_factor = (cp.importance - IMPORTANCE_LOW) / (IMPORTANCE_HIGH - IMPORTANCE_LOW)
            variety = int(UNIT_VARIETY)
            unittypes = db.choose_units(task, importance_factor, variety, enemy)

            if not sams:
                unittypes = [x for x in unittypes if x not in db.SAM_BAN]

            count = max(COUNT_BY_TASK[task] * importance_factor, 1)
            count_per_type = max(int(float(count) / len(unittypes)), 1)
            for unit_type in unittypes:
                print("{} - {} {}".format(cp.name, db.unit_type_name(unit_type), count_per_type))
                cp.base.commision_units({unit_type: count_per_type})
