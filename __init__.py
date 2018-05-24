#!/usr/bin/env python3

import dcs
import os

import gen
import theater.caucasus

m = dcs.Mission()

theater = theater.caucasus.CaucasusTheater()
conflict = theater.controlpoints[0].conflict_attack(theater.controlpoints[1], m.country("USA"), m.country("Russia"))


"""
conflict = gen.Conflict(
        heading=100,
        attacker=m.country("USA"),
        defender=m.country("Russia"),
        point=m.terrain.krymsk().position,
        size=10000)
        """

armor_conflict = gen.ArmorConflictGenerator(m, conflict)
armor_conflict.generate(
        attackers={dcs.vehicles.Armor.MBT_M1A2_Abrams: 8},
        defenders={dcs.vehicles.Armor.MBT_T_80U: 10})

aircraft_conflict = gen.AircraftConflictGenerator(m, conflict)
aircraft_conflict.generate_cas({dcs.planes.A_10C: 4})
aircraft_conflict.generate_escort({dcs.planes.F_15C: 4})
aircraft_conflict.generate_interceptors({dcs.planes.Su_27: 6})

aa_conflict = gen.AAConflictGenerator(m, conflict)
aa_conflict.generate({dcs.vehicles.AirDefence.AAA_ZU_23_on_Ural_375: 3})

m.save("output.miz")
