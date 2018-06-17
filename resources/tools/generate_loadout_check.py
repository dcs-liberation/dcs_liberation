import dcs

from gen.aircraft import AircraftConflictGenerator
from game import db
mis = dcs.Mission(dcs.terrain.PersianGulf())
pos = dcs.terrain.PersianGulf().khasab().position
airgen = AircraftConflictGenerator(mis, None)

for t, uts in db.UNIT_BY_TASK.items():
    if t != dcs.task.CAP and t != dcs.task.CAS:
        continue

    pos.y = dcs.terrain.PersianGulf().khasab().position.x
    for t in t == dcs.task.CAP and [dcs.task.CAP, dcs.task.Escort] or [t]:
        pos.x += 10000
        for ut in uts:
            pos.y += 5000
            ctr = mis.country([k for k, v in db.UNIT_BY_COUNTRY.items() if ut in v][0])

            g = mis.flight_group_inflight(
                country=ctr,
                name="{} - {}".format(t.name, ut),
                aircraft_type=ut,
                position=pos,
                altitude=10000
            )
            g.task = t.name
            airgen._setup_group(g, t)

mis.save("loadout_test.miz")
