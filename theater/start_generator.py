from theater.base import *
from theater.conflicttheater import *

UNIT_VARIETY = 3
UNIT_AMOUNT_FACTOR = 16


def generate_initial(theater: ConflictTheater, enemy: str):
    for cp in theater.enemy_points():
        if cp.captured:
            continue

        for task in [CAP, FighterSweep, CAS, AirDefence]:
            assert cp.importance <= IMPORTANCE_HIGH, "invalid importance {}".format(cp.importance)
            assert cp.importance >= IMPORTANCE_LOW, "invalid importance {}".format(cp.importance)

            importance_factor = (cp.importance - IMPORTANCE_LOW) / (IMPORTANCE_HIGH - IMPORTANCE_LOW)
            variety = int(UNIT_VARIETY + UNIT_VARIETY * importance_factor / 2)
            unittypes = db.choose_units(task, importance_factor, variety, enemy)

            count = max(int(importance_factor * UNIT_AMOUNT_FACTOR), 1)
            count_per_type = max(int(float(count) / len(unittypes)), 1)
            for unit_type in unittypes:
                cp.base.commision_units({unit_type: count_per_type})
