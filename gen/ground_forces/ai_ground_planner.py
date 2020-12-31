import random
from enum import Enum
from typing import Dict, List

from dcs.unittype import VehicleType

from game.theater import ControlPoint
from gen.ground_forces.ai_ground_planner_db import *
from gen.ground_forces.combat_stance import CombatStance

MAX_COMBAT_GROUP_PER_CP = 10


class CombatGroupRole(Enum):
    TANK = 1
    APC = 2
    IFV = 3
    ARTILLERY = 4
    SHORAD = 5
    LOGI = 6
    INFANTRY = 7
    ATGM = 8


DISTANCE_FROM_FRONTLINE = {
    CombatGroupRole.TANK: (2200, 3200),
    CombatGroupRole.APC: (7500, 8500),
    CombatGroupRole.IFV: (2700, 3700),
    CombatGroupRole.ARTILLERY: (16000, 18000),
    CombatGroupRole.SHORAD: (12000, 13000),
    CombatGroupRole.LOGI: (18000, 20000),
    CombatGroupRole.INFANTRY: (2800, 3300),
    CombatGroupRole.ATGM: (5200, 6200),
}

GROUP_SIZES_BY_COMBAT_STANCE = {
    CombatStance.DEFENSIVE: [2, 4, 6],
    CombatStance.AGGRESSIVE: [2, 4, 6],
    CombatStance.RETREAT: [2, 4, 6, 8],
    CombatStance.BREAKTHROUGH: [4, 6, 6, 8],
    CombatStance.ELIMINATION: [2, 4, 4, 4, 6],
    CombatStance.AMBUSH: [1, 1, 2, 2, 2, 2, 4]
}


class CombatGroup:

    def __init__(self, role: CombatGroupRole):
        self.units: List[VehicleType] = []
        self.role = role
        self.assigned_enemy_cp = None
        self.start_position = None

    def __str__(self):
        s = ""
        s += "ROLE : " + str(self.role) + "\n"
        if len(self.units) > 0:
            s += "UNITS " + self.units[0].name + " * " + str(len(self.units))
        return s


class GroundPlanner:

    def __init__(self, cp:ControlPoint, game):
        self.cp = cp
        self.game = game
        self.connected_enemy_cp = [cp for cp in self.cp.connected_points if cp.captured != self.cp.captured]
        self.tank_groups: List[CombatGroup] = []
        self.apc_group: List[CombatGroup] = []
        self.ifv_group: List[CombatGroup] = []
        self.art_group: List[CombatGroup] = []
        self.atgm_group: List[CombatGroup] = []
        self.logi_groups: List[CombatGroup] = []
        self.shorad_groups: List[CombatGroup] = []

        self.units_per_cp: Dict[int, List[CombatGroup]] = {}
        for cp in self.connected_enemy_cp:
            self.units_per_cp[cp.id] = []
        self.reserve: List[CombatGroup] = []

    def plan_groundwar(self):

        if hasattr(self.cp, 'stance'):
            group_size_choice = GROUP_SIZES_BY_COMBAT_STANCE[self.cp.stance]
        else:
            self.cp.stance = CombatStance.DEFENSIVE
            group_size_choice = GROUP_SIZES_BY_COMBAT_STANCE[CombatStance.DEFENSIVE]

        # Create combat groups and assign them randomly to each enemy CP
        for key in self.cp.base.armor.keys():

            role = None
            collection = None
            if key in TYPE_TANKS:
                collection = self.tank_groups
                role = CombatGroupRole.TANK
            elif key in TYPE_APC:
                collection = self.apc_group
                role = CombatGroupRole.APC
            elif key in TYPE_ARTILLERY:
                collection = self.art_group
                role = CombatGroupRole.ARTILLERY
            elif key in TYPE_IFV:
                collection = self.ifv_group
                role = CombatGroupRole.IFV
            elif key in TYPE_LOGI:
                collection = self.logi_groups
                role = CombatGroupRole.LOGI
            elif key in TYPE_ATGM:
                collection = self.atgm_group
                role = CombatGroupRole.ATGM
            elif key in TYPE_SHORAD:
                collection = self.shorad_groups
                role = CombatGroupRole.SHORAD
            else:
                print("Warning unit type not handled by ground generator")
                print(key)
                continue

            available = self.cp.base.armor[key]
            while available > 0:

                if role == CombatGroupRole.SHORAD:
                    n = 1
                else:
                    n = random.choice(group_size_choice)
                    if n > available:
                        if available >= 2:
                            n = 2
                        else:
                            n = 1
                available -= n

                group = CombatGroup(role)
                if len(self.connected_enemy_cp) > 0:
                    enemy_cp = random.choice(self.connected_enemy_cp).id
                    self.units_per_cp[enemy_cp].append(group)
                    group.assigned_enemy_cp = enemy_cp
                else:
                    self.reserve.append(group)
                    group.assigned_enemy_cp = "__reserve__"

                for i in range(n):
                    group.units.append(key)
                collection.append(group)

        print("------------------")
        print("Ground Planner : ")
        print(self.cp.name)
        print("------------------")
        for key in self.units_per_cp.keys():
            print("For : #" + str(key))
            for group in self.units_per_cp[key]:
                print(str(group))









