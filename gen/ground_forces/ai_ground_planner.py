import random
from enum import Enum

from dcs.vehicles import *

from gen import Conflict
from gen.ground_forces.combat_stance import CombatStance
from theater import ControlPoint

TYPE_TANKS = [
    Armor.MBT_T_55,
    Armor.MBT_T_72B,
    Armor.MBT_T_80U,
    Armor.MBT_T_90,
    Armor.MBT_Leopard_2,
    Armor.MBT_Leopard_1A3,
    Armor.MBT_Leclerc,
    Armor.MBT_Challenger_II,
    Armor.MBT_M1A2_Abrams,
    Armor.MBT_M60A3_Patton,
    Armor.MBT_Merkava_Mk__4,
    Armor.MT_Pz_Kpfw_V_Panther_Ausf_G,
    Armor.MT_Pz_Kpfw_IV_Ausf_H,
    Armor.HT_Pz_Kpfw_VI_Tiger_I,
    Armor.HT_Pz_Kpfw_VI_Ausf__B__Tiger_II,
    Armor.MT_M4_Sherman,
    Armor.MT_M4A4_Sherman_Firefly,
    Armor.StuG_IV,
    Armor.ZTZ_96B
]

TYPE_ATGM = [
    Armor.ATGM_M1045_HMMWV_TOW,
    Armor.ATGM_M1134_Stryker,
    Armor.IFV_BMP_2,
]

TYPE_IFV = [
    Armor.IFV_BMP_3,
    Armor.IFV_BMP_2,
    Armor.IFV_BMP_1,
    Armor.IFV_Marder,
    Armor.IFV_MCV_80,
    Armor.IFV_LAV_25,
    Armor.IFV_Sd_Kfz_234_2_Puma,
    Armor.IFV_M2A2_Bradley,
    Armor.IFV_BMD_1,
    Armor.ZBD_04A,
    Armor.APC_Sd_Kfz_251,
    Armor.IFV_Sd_Kfz_234_2_Puma,
]

TYPE_APC = [
    Armor.APC_M1043_HMMWV_Armament,
    Armor.APC_M1126_Stryker_ICV,
    Armor.APC_M113,
    Armor.APC_BTR_80,
    Armor.APC_MTLB,
    Armor.APC_M2A1,
    Armor.APC_Cobra,
    Armor.APC_Sd_Kfz_251,
    Armor.APC_AAV_7,
    Armor.TPz_Fuchs,
    Armor.ARV_BRDM_2,
    Armor.ARV_BTR_RD,
    Armor.FDDM_Grad,
    Armor.M30_Cargo_Carrier,
    Armor.APC_M2A1,
]

TYPE_ARTILLERY = [
    Artillery.MLRS_9A52_Smerch,
    Artillery.SPH_2S1_Gvozdika,
    Artillery.SPH_2S3_Akatsia,
    Artillery.MLRS_BM_21_Grad,
    Artillery.MLRS_9K57_Uragan_BM_27,
    Artillery.SPH_M109_Paladin,
    Artillery.MLRS_M270,
    Artillery.SPH_2S9_Nona,
    Artillery.SpGH_Dana,
    Artillery.SPH_2S19_Msta,
    Artillery.M12_GMC,
    Artillery.MLRS_FDDM,
    Artillery.Sturmpanzer_IV_Brummbär
]

TYPE_LOGI = [
    Unarmed.Transport_M818,
    Unarmed.Transport_KAMAZ_43101,
    Unarmed.Transport_Ural_375,
    Unarmed.Transport_GAZ_66,
    Unarmed.Transport_GAZ_3307,
    Unarmed.Transport_GAZ_3308,
    Unarmed.Transport_Ural_4320_31_Armored,
    Unarmed.Transport_Ural_4320T,
    Unarmed.Blitz_3_6_6700A,
    Unarmed.Kübelwagen_82,
    Unarmed.Sd_Kfz_7,
    Unarmed.Sd_Kfz_2,
    Unarmed.Willys_MB,
    Unarmed.Land_Rover_109_S3,
    Unarmed.Land_Rover_101_FC,
]

TYPE_INFANTRY = [
    Infantry.Infantry_Soldier_Insurgents,
    Infantry.Soldier_AK,
    Infantry.Infantry_M1_Garand,
    Infantry.Infantry_Mauser_98,
    Infantry.Infantry_SMLE_No_4_Mk_1,
    Infantry.Georgian_soldier_with_M4,
    Infantry.Infantry_Soldier_Rus,
    Infantry.Paratrooper_AKS,
    Infantry.Paratrooper_RPG_16,
    Infantry.Soldier_M249,
    Infantry.Infantry_M4,
    Infantry.Soldier_RPG,
]

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
    CombatGroupRole.TANK:2800,
    CombatGroupRole.APC:7000,
    CombatGroupRole.IFV:3000,
    CombatGroupRole.ARTILLERY:14000,
    CombatGroupRole.SHORAD:12000,
    CombatGroupRole.LOGI:18000,
    CombatGroupRole.INFANTRY:2800,
    CombatGroupRole.ATGM:5500
}

GROUP_SIZES_BY_COMBAT_STANCE = {
    CombatStance.DEFENSIVE: [2, 4, 6],
    CombatStance.AGGRESIVE: [2, 4, 6],
    CombatStance.RETREAT: [2, 4, 6, 8],
    CombatStance.BREAKTHROUGH: [4, 6, 6, 8],
    CombatStance.ELIMINATION: [2, 4, 4, 4, 6],
    CombatStance.AMBUSH: [1, 1, 2, 2, 2, 2, 4]
}


class CombatGroup:

    def __init__(self, role:CombatGroupRole):
        self.units = []
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

    cp = None
    combat_groups_dict = {}
    connected_enemy_cp = []

    tank_groups = []
    apc_group = []
    ifv_group = []
    art_group = []
    shorad_groups = []
    logi_groups = []

    def __init__(self, cp:ControlPoint, game):
        self.cp = cp
        self.game = game
        self.connected_enemy_cp = [cp for cp in self.cp.connected_points if cp.captured != self.cp.captured]
        self.tank_groups = []
        self.apc_group = []
        self.ifv_group = []
        self.art_group = []
        self.atgm_group = []
        self.logi_groups = []
        self.shorad_groups = []

        self.units_per_cp = {}
        for cp in self.connected_enemy_cp:
            self.units_per_cp[cp.id] = []
        self.reserve = []


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
            else:
                print("Warning unit type not handled by ground generator")
                print(key)
                continue

            available = self.cp.base.armor[key]
            while available > 0:
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









