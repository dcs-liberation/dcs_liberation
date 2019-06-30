import os
import sys
import dcs

from game import db
from gen.aircraft import AircraftConflictGenerator

dcs.planes.FlyingType.payload_dirs = [os.path.join(os.path.dirname(os.path.realpath(__file__)), "..\\payloads")]

mis = dcs.Mission(dcs.terrain.PersianGulf())
pos = dcs.terrain.PersianGulf().khasab().position
airgen = AircraftConflictGenerator(mis, None, None)

for t, uts in db.UNIT_BY_TASK.items():
    if t != dcs.task.CAP and t != dcs.task.CAS:
        continue

    pos.y = dcs.terrain.PersianGulf().khasab().position.x
    for t in t == dcs.task.CAP and [dcs.task.CAP, dcs.task.Escort] or [t]:
        pos.x += 10000
        for ut in uts:
            pos.y += 5000
            ctr = mis.country([v["country"] for k, v in db.FACTIONS.items() if ut in v["units"]][0])

            g = mis.flight_group_inflight(
                country=ctr,
                name="{} - {}".format(t.name, ut),
                aircraft_type=ut,
                position=pos,
                altitude=10000
            )
            g.task = t.name
            airgen._setup_group(g, t, 0)

mis.save("loadout_test.miz")
