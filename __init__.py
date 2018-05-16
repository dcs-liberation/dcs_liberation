#!/usr/bin/env python3

import dcs
import os

import gen

m = dcs.Mission()

conflict = gen.Conflict(
        heading=100,
        attacker=m.country("USA"),
        defender=m.country("Russia"),
        point=m.terrain.krymsk().position,
        size=10000)

armor_conflict = gen.ArmorConflictGenerator(m, conflict)
armor_conflict.generate(
        attackers={dcs.vehicles.Armor.MBT_M1A2_Abrams: 8},
        defenders={dcs.vehicles.Armor.MBT_T_80U: 6})

aircraft_conflict = gen.AircraftConflictGenerator(m, conflict)
aircraft_conflict.generate_cas({dcs.planes.A_10C: 2})
aircraft_conflict.generate_escort({dcs.planes.F_15C: 2})
aircraft_conflict.generate_interceptors({dcs.planes.Su_27: 2})
