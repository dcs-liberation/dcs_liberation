from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Tuple, Type, Union
import json
from pathlib import Path

from dcs.countries import country_dict
from dcs.helicopters import (
    AH_1W,
    AH_64A,
    AH_64D,
    HelicopterType,
    Ka_50,
    Mi_24V,
    Mi_28N,
    Mi_8MT,
    OH_58D,
    SA342L,
    SA342M,
    SA342Minigun,
    SA342Mistral,
    SH_60B,
    UH_1H,
    UH_60A,
    helicopter_map,
)
from dcs.mapping import Point
# mypy can't resolve these if they're wildcard imports for some reason.
from dcs.planes import (
    AJS37,
    AV8BNA,
    A_10A,
    A_10C,
    A_10C_2,
    A_20G,
    A_50,
    An_26B,
    An_30M,
    B_17G,
    B_1B,
    B_52H,
    Bf_109K_4,
    C_101CC,
    C_130,
    E_3A,
    E_2C,
    FA_18C_hornet,
    FW_190A8,
    FW_190D9,
    F_117A,
    F_14A_135_GR,
    F_14B,
    F_111F,
    F_15C,
    F_15E,
    F_16A,
    F_16C_50,
    F_4E,
    F_5E_3,
    F_86F_Sabre,
    F_A_18C,
    IL_76MD,
    IL_78M,
    JF_17,
    J_11A,
    Ju_88A4,
    KC130,
    KC_135,
    KC135MPRS,
    KJ_2000,
    L_39C,
    L_39ZA,
    MQ_9_Reaper,
    M_2000C,
    MiG_15bis,
    MiG_19P,
    MiG_21Bis,
    MiG_23MLD,
    MiG_25PD,
    MiG_27K,
    MiG_29A,
    MiG_29G,
    MiG_29S,
    MiG_31,
    Mirage_2000_5,
    P_47D_30,
    P_47D_30bl1,
    P_47D_40,
    P_51D,
    P_51D_30_NA,
    PlaneType,
    RQ_1A_Predator,
    S_3B,
    S_3B_Tanker,
    SpitfireLFMkIX,
    SpitfireLFMkIXCW,
    Su_17M4,
    Su_24M,
    Su_24MR,
    Su_25,
    Su_25T,
    Su_25TM,
    Su_27,
    Su_30,
    Su_33,
    Su_34,
    Tornado_GR4,
    Tornado_IDS,
    Tu_160,
    Tu_22M3,
    Tu_95MS,
    WingLoong_I,
    Yak_40,
    plane_map,
    I_16
)
from dcs.ships import (
    Armed_speedboat,
    Bulk_cargo_ship_Yakushev,
    CVN_71_Theodore_Roosevelt,
    CVN_72_Abraham_Lincoln,
    CVN_73_George_Washington,
    CVN_74_John_C__Stennis,
    CVN_75_Harry_S__Truman,
    CV_1143_5_Admiral_Kuznetsov,
    CV_1143_5_Admiral_Kuznetsov_2017,
    Dry_cargo_ship_Ivanov,
    LHA_1_Tarawa,
    Tanker_Elnya_160,
    ship_map,
)
from dcs.task import (
    AWACS,
    AntishipStrike,
    CAP,
    CAS,
    CargoTransportation,
    Embarking,
    Escort,
    FighterSweep,
    GroundAttack,
    Intercept,
    MainTask,
    Nothing,
    PinpointStrike,
    Reconnaissance,
    Refueling,
    SEAD,
    Task,
    Transport,
    RunwayAttack,
)
from dcs.terrain.terrain import Airport
from dcs.unit import Ship, Unit, Vehicle
from dcs.unitgroup import ShipGroup, StaticGroup
from dcs.unittype import FlyingType, ShipType, UnitType, VehicleType
from dcs.vehicles import (
    AirDefence,
    Armor,
    Artillery,
    Carriage,
    Infantry,
    Unarmed,
    vehicle_map,
)

import pydcs_extensions.frenchpack.frenchpack as frenchpack
import pydcs_extensions.highdigitsams.highdigitsams as highdigitsams
# PATCH pydcs data with MODS
from game.factions.faction_loader import FactionLoader
from pydcs_extensions.a4ec.a4ec import A_4E_C
from pydcs_extensions.f22a.f22a import F_22A
from pydcs_extensions.hercules.hercules import Hercules
from pydcs_extensions.mb339.mb339 import MB_339PAN
from pydcs_extensions.rafale.rafale import Rafale_A_S, Rafale_M, Rafale_B
from pydcs_extensions.su57.su57 import Su_57

UNITINFOTEXT_PATH = Path("./resources/units/unit_info_text.json")

plane_map["A-4E-C"] = A_4E_C
plane_map["MB-339PAN"] = MB_339PAN
plane_map["Rafale_M"] = Rafale_M
plane_map["Rafale_A_S"] = Rafale_A_S
plane_map["Rafale_B"] = Rafale_B
plane_map["Su-57"] = Su_57
plane_map["Hercules"] = Hercules

vehicle_map["FieldHL"] = frenchpack._FIELD_HIDE
vehicle_map["HARRIERH"] = frenchpack._FIELD_HIDE_SMALL
vehicle_map["SMOKESAM"] = frenchpack.SMOKE_SAM_IR
vehicle_map["SmokeD1"] = frenchpack.SmokeD1
vehicle_map["SmokeD3"] = frenchpack.SmokeD3
vehicle_map["AMX10RCR"] = frenchpack.AMX_10RCR
vehicle_map["SEPAR"] = frenchpack.AMX_10RCR_SEPAR
vehicle_map["ERC"] = frenchpack.ERC_90
vehicle_map["M120"] = frenchpack.MO_120_RT
vehicle_map["AA20"] = frenchpack._53T2
vehicle_map["TRM2000"] = frenchpack.TRM_2000
vehicle_map["TRM2000_Citerne"] = frenchpack.TRM_2000_Fuel
vehicle_map["TRM2000_AA20"] = frenchpack.TRM_2000_53T2
vehicle_map["TRMMISTRAL"] = frenchpack.TRM_2000_PAMELA
vehicle_map["VABH"] = frenchpack.VAB_MEDICAL
vehicle_map["VAB_RADIO"] = frenchpack.VAB
vehicle_map["VAB_50"] = frenchpack.VAB__50
vehicle_map["VIB_VBR"] = frenchpack.VAB_T20_13
vehicle_map["VAB_HOT"] = frenchpack.VAB_MEPHISTO
vehicle_map["VAB_MORTIER"] = frenchpack.VAB_MORTIER
vehicle_map["VBL50"] = frenchpack.VBL__50
vehicle_map["VBLANF1"] = frenchpack.VBL_AANF1
vehicle_map["VBL-radio"] = frenchpack.VBL
vehicle_map["VBAE"] = frenchpack.VBAE_CRAB
vehicle_map["VBAE_MMP"] = frenchpack.VBAE_CRAB_MMP
vehicle_map["AMX-30B2"] = frenchpack.AMX_30B2
vehicle_map["Tracma"] = frenchpack.Tracma_TD_1500
vehicle_map["JTACFP"] = frenchpack.Infantry_Soldier_JTAC
vehicle_map["SHERIDAN"] = frenchpack.Char_M551_Sheridan
vehicle_map["Leclerc_XXI"] = frenchpack.Leclerc_Serie_XXI
vehicle_map["Toyota_bleu"] = frenchpack.DIM__TOYOTA_BLUE
vehicle_map["Toyota_vert"] = frenchpack.DIM__TOYOTA_GREEN
vehicle_map["Toyota_desert"] = frenchpack.DIM__TOYOTA_DESERT
vehicle_map["Kamikaze"] = frenchpack.DIM__KAMIKAZE

vehicle_map[highdigitsams.AAA_SON_9_Fire_Can.id] = highdigitsams.AAA_SON_9_Fire_Can
vehicle_map[highdigitsams.AAA_100mm_KS_19.id] = highdigitsams.AAA_100mm_KS_19
vehicle_map[highdigitsams.SAM_SA_10B_S_300PS_54K6_CP.id] = highdigitsams.SAM_SA_10B_S_300PS_54K6_CP
vehicle_map[highdigitsams.SAM_SA_10B_S_300PS_5P85SE_LN.id] = highdigitsams.SAM_SA_10B_S_300PS_5P85SE_LN
vehicle_map[highdigitsams.SAM_SA_10B_S_300PS_5P85SU_LN.id] = highdigitsams.SAM_SA_10B_S_300PS_5P85SU_LN
vehicle_map[highdigitsams.SAM_SA_10__5V55RUD__S_300PS_LN_5P85CE.id] = highdigitsams.SAM_SA_10__5V55RUD__S_300PS_LN_5P85CE
vehicle_map[highdigitsams.SAM_SA_10__5V55RUD__S_300PS_LN_5P85DE.id] = highdigitsams.SAM_SA_10__5V55RUD__S_300PS_LN_5P85DE
vehicle_map[highdigitsams.SAM_SA_10B_S_300PS_30N6_TR.id] = highdigitsams.SAM_SA_10B_S_300PS_30N6_TR
vehicle_map[highdigitsams.SAM_SA_10B_S_300PS_40B6M_TR.id] = highdigitsams.SAM_SA_10B_S_300PS_40B6M_TR
vehicle_map[highdigitsams.SAM_SA_10B_S_300PS_40B6MD_SR.id] = highdigitsams.SAM_SA_10B_S_300PS_40B6MD_SR
vehicle_map[highdigitsams.SAM_SA_10B_S_300PS_64H6E_SR.id] = highdigitsams.SAM_SA_10B_S_300PS_64H6E_SR
vehicle_map[highdigitsams.SAM_SA_20_S_300PMU1_CP_54K6.id] = highdigitsams.SAM_SA_20_S_300PMU1_CP_54K6
vehicle_map[highdigitsams.SAM_SA_20_S_300PMU1_TR_30N6E.id] = highdigitsams.SAM_SA_20_S_300PMU1_TR_30N6E
vehicle_map[highdigitsams.SAM_SA_20_S_300PMU1_TR_30N6E_truck.id] = highdigitsams.SAM_SA_20_S_300PMU1_TR_30N6E_truck
vehicle_map[highdigitsams.SAM_SA_20_S_300PMU1_SR_5N66E.id] = highdigitsams.SAM_SA_20_S_300PMU1_SR_5N66E
vehicle_map[highdigitsams.SAM_SA_20_S_300PMU1_SR_64N6E.id] = highdigitsams.SAM_SA_20_S_300PMU1_SR_64N6E
vehicle_map[highdigitsams.SAM_SA_20_S_300PMU1_LN_5P85CE.id] = highdigitsams.SAM_SA_20_S_300PMU1_LN_5P85CE
vehicle_map[highdigitsams.SAM_SA_20_S_300PMU1_LN_5P85DE.id] = highdigitsams.SAM_SA_20_S_300PMU1_LN_5P85DE
vehicle_map[highdigitsams.SAM_SA_20B_S_300PMU2_CP_54K6E2.id] = highdigitsams.SAM_SA_20B_S_300PMU2_CP_54K6E2
vehicle_map[highdigitsams.SAM_SA_20B_S_300PMU2_TR_92H6E_truck.id] = highdigitsams.SAM_SA_20B_S_300PMU2_TR_92H6E_truck
vehicle_map[highdigitsams.SAM_SA_20B_S_300PMU2_SR_64N6E2.id] = highdigitsams.SAM_SA_20B_S_300PMU2_SR_64N6E2
vehicle_map[highdigitsams.SAM_SA_20B_S_300PMU2_LN_5P85SE2.id] = highdigitsams.SAM_SA_20B_S_300PMU2_LN_5P85SE2
vehicle_map[highdigitsams.SAM_SA_12_S_300V_9S457_CP.id] = highdigitsams.SAM_SA_12_S_300V_9S457_CP
vehicle_map[highdigitsams.SAM_SA_12_S_300V_9A82_LN.id] = highdigitsams.SAM_SA_12_S_300V_9A82_LN
vehicle_map[highdigitsams.SAM_SA_12_S_300V_9A83_LN.id] = highdigitsams.SAM_SA_12_S_300V_9A83_LN
vehicle_map[highdigitsams.SAM_SA_12_S_300V_9S15_SR.id] = highdigitsams.SAM_SA_12_S_300V_9S15_SR
vehicle_map[highdigitsams.SAM_SA_12_S_300V_9S19_SR.id] = highdigitsams.SAM_SA_12_S_300V_9S19_SR
vehicle_map[highdigitsams.SAM_SA_12_S_300V_9S32_TR.id] = highdigitsams.SAM_SA_12_S_300V_9S32_TR
vehicle_map[highdigitsams.SAM_SA_23_S_300VM_9S457ME_CP.id] = highdigitsams.SAM_SA_23_S_300VM_9S457ME_CP
vehicle_map[highdigitsams.SAM_SA_23_S_300VM_9S15M2_SR.id] = highdigitsams.SAM_SA_23_S_300VM_9S15M2_SR
vehicle_map[highdigitsams.SAM_SA_23_S_300VM_9S19M2_SR.id] = highdigitsams.SAM_SA_23_S_300VM_9S19M2_SR
vehicle_map[highdigitsams.SAM_SA_23_S_300VM_9S32ME_TR.id] = highdigitsams.SAM_SA_23_S_300VM_9S32ME_TR
vehicle_map[highdigitsams.SAM_SA_23_S_300VM_9A83ME_LN.id] = highdigitsams.SAM_SA_23_S_300VM_9A83ME_LN
vehicle_map[highdigitsams.SAM_SA_23_S_300VM_9A82ME_LN.id] = highdigitsams.SAM_SA_23_S_300VM_9A82ME_LN
vehicle_map[highdigitsams.SAM_SA_17_Buk_M1_2_LN_9A310M1_2.id] = highdigitsams.SAM_SA_17_Buk_M1_2_LN_9A310M1_2
vehicle_map[highdigitsams.SAM_SA_2__V759__LN_SM_90.id] = highdigitsams.SAM_SA_2__V759__LN_SM_90
vehicle_map[highdigitsams.SAM_HQ_2_LN_SM_90.id] = highdigitsams.SAM_HQ_2_LN_SM_90
vehicle_map[highdigitsams.SAM_SA_3__V_601P__LN_5P73.id] = highdigitsams.SAM_SA_3__V_601P__LN_5P73
vehicle_map[highdigitsams.SAM_SA_24_Igla_S_manpad.id] = highdigitsams.SAM_SA_24_Igla_S_manpad
vehicle_map[highdigitsams.SAM_SA_14_Strela_3_manpad.id] = highdigitsams.SAM_SA_14_Strela_3_manpad
vehicle_map[highdigitsams.Polyana_D4M1_C2_node.id] = highdigitsams.Polyana_D4M1_C2_node
vehicle_map[highdigitsams._34Ya6E_Gazetchik_E_decoy.id] = highdigitsams._34Ya6E_Gazetchik_E_decoy

"""
---------- BEGINNING OF CONFIGURATION SECTION
"""

"""
All aircraft names in this file should correspond with naming provided in following files:

* https://github.com/pydcs/dcs/blob/master/dcs/planes.py - for planes
* https://github.com/pydcs/dcs/blob/master/dcs/helicopters.py - for helicopters
* https://github.com/pydcs/dcs/blob/master/dcs/vehicles.py - for vehicles (this include all of the ground vehicles)

You can find names at the bottom of the file in following format:

x_map = {
    "Name of the unit in game": Identifier,
}

from this example `Identifier` should be used (which may or may not include category of the unit and dot + underscore characters).
For example, player accessible Hornet is called `FA_18C_hornet`, and MANPAD Igla is called `AirDefence.SAM_SA_18_Igla_S_MANPADS`
"""

# This should probably be much higher, but the AI doesn't rollover their budget
# and isn't smart enough to save to repair a critical runway anyway, so it has
# to be cheap enough to repair with a single turn's income.
RUNWAY_REPAIR_COST = 100

"""
Prices for the aircraft. 
This defines both price for the player (although only aircraft listed in CAP/CAS/Transport/Armor/AirDefense roles will be purchasable) 
and prioritization for the enemy (i.e. less important bases will receive units with lower price)
"""
PRICES = {
    # fighter
    MiG_23MLD: 13,
    Su_27: 18,
    Su_33: 22,
    MiG_29A: 18,
    MiG_29S: 20,
    MiG_29G: 18,
    MiG_25PD: 20,
    MiG_31: 30,
    J_11A: 26,
    JF_17: 20,
    Su_30: 24,
    Su_57: 40,

    SpitfireLFMkIX: 14,
    SpitfireLFMkIXCW: 14,
    I_16: 10,
    Bf_109K_4: 14,
    FW_190D9: 16,
    FW_190A8: 14,
    A_20G: 22,
    Ju_88A4: 24,

    F_5E_3: 8,
    MiG_15bis: 4,
    MiG_19P: 6,
    F_86F_Sabre: 4,
    MiG_21Bis: 8,
    F_4E: 10,
    AJS37: 12,
    C_101CC: 6,
    A_4E_C: 8,
    MB_339PAN: 6,

    AV8BNA: 14,
    M_2000C: 16,
    Mirage_2000_5: 20,
    FA_18C_hornet: 22,
    F_15C: 22,
    F_15E: 24,
    F_16C_50: 20,
    F_16A: 14,
    F_14A_135_GR: 20,
    F_14B: 24,
    F_22A: 40,
    Tornado_IDS: 20,
    Tornado_GR4: 20,

    # bomber
    Su_17M4: 10,
    Su_25: 15,
    Su_25T: 18,
    L_39ZA: 10,
    Su_34: 24,
    Su_24M: 20,
    Su_24MR: 24,
    MiG_27K: 20,

    A_10A: 16,
    A_10C: 22,
    A_10C_2: 24,
    S_3B: 10,

    # heli
    Ka_50: 13,
    SA342M: 8,
    SA342L: 5,
    SA342Minigun: 4,
    SA342Mistral: 8,
    UH_1H: 4,
    Mi_8MT: 5,
    Mi_24V: 18,
    Mi_28N: 24,
    AH_1W: 20,
    AH_64A: 24,
    AH_64D: 30,
    OH_58D: 6,
    SH_60B: 6,

    # Bombers
    B_52H: 35,
    B_1B: 50,
    F_117A: 100,
    Tu_160: 50,
    Tu_22M3: 40,
    Tu_95MS: 35,
    F_111F: 21,

    # special
    IL_76MD: 30,
    An_26B: 25,
    An_30M: 25,
    Yak_40: 25,
    S_3B_Tanker: 20,
    IL_78M: 25,
    KC_135: 25,
    KC130: 25,
    KC135MPRS: 25,

    A_50: 50,
    KJ_2000: 50,
    E_3A: 50,
    E_2C: 50,
    C_130: 25,
    Hercules: 25,

    # WW2
    P_51D_30_NA: 18,
    P_51D: 16,
    P_47D_30: 17,
    P_47D_30bl1: 16,
    P_47D_40: 18,
    B_17G: 30,

    # Drones
    MQ_9_Reaper: 12,
    RQ_1A_Predator: 6,
    WingLoong_I: 6,

    # Modded
    Rafale_M: 26,
    Rafale_A_S: 26,
    Rafale_B: 26,

    # armor
    Armor.APC_MTLB: 4,
    Armor.FDDM_Grad: 4,
    Armor.ARV_BRDM_2: 6,
    Armor.ARV_BTR_RD: 6,
    Armor.APC_BTR_80: 8,
    Armor.APC_BTR_82A: 10,
    Armor.MBT_T_55: 18,
    Armor.MBT_T_72B: 20,
    Armor.MBT_T_72B3: 25,
    Armor.MBT_T_80U: 25,
    Armor.MBT_T_90: 30,
    Armor.IFV_BMD_1: 8,
    Armor.IFV_BMP_1: 14,
    Armor.IFV_BMP_2: 16,
    Armor.IFV_BMP_3: 18,
    Armor.ZBD_04A: 12,
    Armor.ZTZ_96B: 30,

    Armor.APC_Cobra: 4,
    Armor.APC_M113: 6,
    Armor.APC_M1043_HMMWV_Armament: 2,
    Armor.ATGM_M1045_HMMWV_TOW: 8,
    Armor.IFV_M2A2_Bradley: 12,
    Armor.APC_M1126_Stryker_ICV: 10,
    Armor.SPG_M1128_Stryker_MGS: 14,
    Armor.ATGM_M1134_Stryker: 12,
    Armor.MBT_M60A3_Patton: 16,
    Armor.MBT_M1A2_Abrams: 25,
    Armor.MBT_Leclerc: 25,
    Armor.MBT_Leopard_1A3: 20,
    Armor.MBT_Leopard_2: 25,
    Armor.MBT_Merkava_Mk__4: 25,
    Armor.TPz_Fuchs: 5,
    Armor.MBT_Challenger_II: 25,
    Armor.IFV_Marder: 10,
    Armor.IFV_MCV_80: 10,
    Armor.IFV_LAV_25: 7,

    Artillery.MLRS_M270: 55,
    Artillery.SPH_M109_Paladin: 25,

    Artillery.SPH_2S9_Nona: 12,
    Artillery.SPH_2S1_Gvozdika: 18,
    Artillery.SPH_2S3_Akatsia: 24,
    Artillery.SPH_2S19_Msta: 30,
    Artillery.MLRS_BM_21_Grad: 15,
    Artillery.MLRS_9K57_Uragan_BM_27: 50,
    Artillery.MLRS_9A52_Smerch: 40,
    Artillery._2B11_mortar: 4,
    Artillery.SpGH_Dana: 26,

    Unarmed.Transport_UAZ_469: 3,
    Unarmed.Transport_Ural_375: 3,
    Infantry.Infantry_M4: 1,
    Infantry.Soldier_AK: 1,

    Unarmed.Transport_M818: 3,

    # WW2
    Armor.MT_Pz_Kpfw_V_Panther_Ausf_G: 24,
    Armor.MT_Pz_Kpfw_IV_Ausf_H: 16,
    Armor.HT_Pz_Kpfw_VI_Tiger_I: 24,
    Armor.HT_Pz_Kpfw_VI_Ausf__B_Tiger_II: 26,
    Armor.TD_Jagdpanther_G1: 18,
    Armor.TD_Jagdpanzer_IV: 11,
    Armor.Sd_Kfz_184_Elefant: 18,
    Armor.APC_Sd_Kfz_251: 4,
    Armor.AC_Sd_Kfz_234_2_Puma: 8,
    Armor.MT_M4_Sherman: 12,
    Armor.MT_M4A4_Sherman_Firefly: 16,
    Armor.CT_Cromwell_IV: 12,
    Armor.M30_Cargo_Carrier: 2,
    Armor.APC_M2A1: 4,
    Armor.CT_Centaur_IV: 10,
    Armor.HIT_Churchill_VII: 16,
    Armor.LAC_M8_Greyhound: 8,
    Armor.TD_M10_GMC: 14,
    Armor.StuG_III_Ausf__G: 12,
    Armor.StuG_IV: 14,
    Artillery.M12_GMC: 10,
    Artillery.Sturmpanzer_IV_Brummbär: 10,
    Armor.Daimler_Armoured_Car: 8,
    Armor.LT_Mk_VII_Tetrarch: 8,
    Armor.M4_Tractor: 2,

    # ship
    CV_1143_5_Admiral_Kuznetsov: 100,
    CVN_74_John_C__Stennis: 100,
    LHA_1_Tarawa: 50,

    Bulk_cargo_ship_Yakushev: 10,
    Armed_speedboat: 10,
    Dry_cargo_ship_Ivanov: 10,
    Tanker_Elnya_160: 10,

    # Air Defence units
    AirDefence.SAM_SA_19_Tunguska_2S6: 30,
    AirDefence.SAM_SA_6_Kub_LN_2P25: 20,
    AirDefence.SAM_SA_3_S_125_LN_5P73: 6,

    AirDefence.SAM_SA_11_Buk_LN_9A310M1: 30,
    AirDefence.SAM_SA_11_Buk_CC_9S470M1: 25,
    AirDefence.SAM_SA_11_Buk_SR_9S18M1: 28,
    AirDefence.SAM_SA_8_Osa_9A33: 28,
    AirDefence.SAM_SA_15_Tor_9A331: 40,
    AirDefence.SAM_SA_13_Strela_10M3_9A35M3: 16,
    AirDefence.SAM_SA_9_Strela_1_9P31: 12,
    AirDefence.SAM_SA_8_Osa_LD_9T217: 22,
    AirDefence.SAM_Patriot_AMG_AN_MRC_137: 35,
    AirDefence.SAM_Patriot_ECS_AN_MSQ_104: 30,
    AirDefence.SPAAA_Gepard: 24,
    AirDefence.SAM_Hawk_PCP: 14,
    AirDefence.AAA_Vulcan_M163: 10,
    AirDefence.SAM_Hawk_LN_M192: 8,
    AirDefence.SAM_Chaparral_M48: 16,
    AirDefence.SAM_Linebacker_M6: 18,
    AirDefence.SAM_Patriot_LN_M901: 15,
    AirDefence.SAM_Avenger_M1097: 20,
    AirDefence.SAM_Patriot_EPP_III: 15,
    AirDefence.SAM_Patriot_ICC: 18,
    AirDefence.SAM_Roland_ADS: 12,
    AirDefence.Stinger_MANPADS: 6,
    AirDefence.SAM_Stinger_comm_dsr: 4,
    AirDefence.SAM_Stinger_comm: 4,
    AirDefence.SPAAA_ZSU_23_4_Shilka: 10,
    AirDefence.AAA_ZSU_57_2: 12,
    AirDefence.AAA_ZU_23_Closed: 6,
    AirDefence.AAA_ZU_23_Emplacement: 6,
    AirDefence.AAA_ZU_23_on_Ural_375: 7,
    AirDefence.AAA_ZU_23_Insurgent_Closed: 6,
    AirDefence.AAA_ZU_23_Insurgent_on_Ural_375: 7,
    AirDefence.AAA_ZU_23_Insurgent: 6,
    AirDefence.SAM_SA_18_Igla_MANPADS: 10,
    AirDefence.SAM_SA_18_Igla_comm: 8,
    AirDefence.SAM_SA_18_Igla_S_MANPADS: 12,
    AirDefence.SAM_SA_18_Igla_S_comm: 8,
    AirDefence.EWR_1L13: 30,
    AirDefence.SAM_SA_6_Kub_STR_9S91: 22,

    AirDefence.EWR_55G6: 30,
    AirDefence.CP_9S80M1_Sborka: 10,
    AirDefence.SAM_Hawk_TR_AN_MPQ_46: 14,
    AirDefence.SAM_Hawk_SR_AN_MPQ_50: 18,
    AirDefence.SAM_Patriot_STR_AN_MPQ_53: 22,
    AirDefence.SAM_Hawk_CWAR_AN_MPQ_55: 20,
    AirDefence.SAM_SR_P_19: 14,
    AirDefence.SAM_Roland_EWR: 16,
    AirDefence.SAM_SA_3_S_125_TR_SNR: 14,
    AirDefence.SAM_SA_2_LN_SM_90: 8,
    AirDefence.SAM_SA_2_TR_SNR_75_Fan_Song: 12,
    AirDefence.Rapier_FSA_Launcher: 6,
    AirDefence.Rapier_FSA_Optical_Tracker: 6,
    AirDefence.Rapier_FSA_Blindfire_Tracker: 8,
    AirDefence.HQ_7_Self_Propelled_LN: 20,
    AirDefence.HQ_7_Self_Propelled_STR: 24,
    AirDefence.AAA_8_8cm_Flak_18: 6,
    AirDefence.AAA_Flak_38: 6,
    AirDefence.AAA_8_8cm_Flak_36: 8,
    AirDefence.AAA_8_8cm_Flak_37: 9,
    AirDefence.AAA_Flak_Vierling_38: 5,
    AirDefence.AAA_Kdo_G_40: 8,
    AirDefence.Flak_Searchlight_37: 4,
    AirDefence.Maschinensatz_33: 10,
    AirDefence.AAA_8_8cm_Flak_41: 10,
    AirDefence.EWR_FuMG_401_Freya_LZ: 25,
    AirDefence.AAA_Bofors_40mm: 8,
    AirDefence.AAA_M1_37mm: 7,
    AirDefence.AAA_M45_Quadmount: 4,
    AirDefence.AA_gun_QF_3_7: 10,

    # FRENCH PACK MOD
    frenchpack.AMX_10RCR: 10,
    frenchpack.AMX_10RCR_SEPAR: 12,
    frenchpack.ERC_90: 12,
    frenchpack.MO_120_RT: 10,
    frenchpack._53T2: 4,
    frenchpack.TRM_2000: 4,
    frenchpack.TRM_2000_Fuel: 4,
    frenchpack.TRM_2000_53T2: 8,
    frenchpack.TRM_2000_PAMELA: 14,
    frenchpack.VAB_MEDICAL: 8,
    frenchpack.VAB: 6,
    frenchpack.VAB__50: 4,
    frenchpack.VAB_T20_13: 6,
    frenchpack.VAB_MEPHISTO: 8,
    frenchpack.VAB_MORTIER: 10,
    frenchpack.VBL__50: 4,
    frenchpack.VBL_AANF1: 2,
    frenchpack.VBL: 1,
    frenchpack.VBAE_CRAB: 8,
    frenchpack.VBAE_CRAB_MMP: 12,
    frenchpack.AMX_30B2: 18,
    frenchpack.Tracma_TD_1500: 2,
    frenchpack.Infantry_Soldier_JTAC: 1,
    frenchpack.Leclerc_Serie_XXI: 35,
    frenchpack.DIM__TOYOTA_BLUE: 2,
    frenchpack.DIM__TOYOTA_GREEN: 2,
    frenchpack.DIM__TOYOTA_DESERT: 2,
    frenchpack.DIM__KAMIKAZE: 6,

    # SA-10
    AirDefence.SAM_SA_10_S_300PS_CP_54K6: 18,
    AirDefence.SAM_SA_10_S_300PS_TR_30N6: 24,
    AirDefence.SAM_SA_10_S_300PS_SR_5N66M: 30,
    AirDefence.SAM_SA_10_S_300PS_SR_64H6E: 30,
    AirDefence.SAM_SA_10_S_300PS_LN_5P85C: 22,
    AirDefence.SAM_SA_10_S_300PS_LN_5P85D: 22,

    # High digit sams mod
    highdigitsams.AAA_SON_9_Fire_Can: 8,
    highdigitsams.AAA_100mm_KS_19: 10,

    highdigitsams.SAM_SA_10B_S_300PS_54K6_CP: 20,
    highdigitsams.SAM_SA_10B_S_300PS_5P85SE_LN: 24,
    highdigitsams.SAM_SA_10B_S_300PS_5P85SU_LN: 24,
    highdigitsams.SAM_SA_10__5V55RUD__S_300PS_LN_5P85CE: 24,
    highdigitsams.SAM_SA_10__5V55RUD__S_300PS_LN_5P85DE: 24,
    highdigitsams.SAM_SA_10B_S_300PS_30N6_TR: 26,
    highdigitsams.SAM_SA_10B_S_300PS_40B6M_TR: 26,
    highdigitsams.SAM_SA_10B_S_300PS_40B6MD_SR: 32,
    highdigitsams.SAM_SA_10B_S_300PS_64H6E_SR: 32,

    highdigitsams.SAM_SA_12_S_300V_9S457_CP: 22,
    highdigitsams.SAM_SA_12_S_300V_9A82_LN: 26,
    highdigitsams.SAM_SA_12_S_300V_9A83_LN: 26,
    highdigitsams.SAM_SA_12_S_300V_9S15_SR: 34,
    highdigitsams.SAM_SA_12_S_300V_9S19_SR: 34,
    highdigitsams.SAM_SA_12_S_300V_9S32_TR: 28,

    highdigitsams.SAM_SA_20_S_300PMU1_CP_54K6: 26,
    highdigitsams.SAM_SA_20_S_300PMU1_TR_30N6E: 30,
    highdigitsams.SAM_SA_20_S_300PMU1_TR_30N6E_truck: 32,
    highdigitsams.SAM_SA_20_S_300PMU1_SR_5N66E: 38,
    highdigitsams.SAM_SA_20_S_300PMU1_SR_64N6E: 38,
    highdigitsams.SAM_SA_20_S_300PMU1_LN_5P85CE: 28,
    highdigitsams.SAM_SA_20_S_300PMU1_LN_5P85DE: 28,

    highdigitsams.SAM_SA_20B_S_300PMU2_CP_54K6E2: 27,
    highdigitsams.SAM_SA_20B_S_300PMU2_TR_92H6E_truck: 33,
    highdigitsams.SAM_SA_20B_S_300PMU2_SR_64N6E2: 40,
    highdigitsams.SAM_SA_20B_S_300PMU2_LN_5P85SE2: 30,

    highdigitsams.SAM_SA_23_S_300VM_9S457ME_CP: 30,
    highdigitsams.SAM_SA_23_S_300VM_9S15M2_SR: 45,
    highdigitsams.SAM_SA_23_S_300VM_9S19M2_SR: 45,
    highdigitsams.SAM_SA_23_S_300VM_9S32ME_TR: 35,
    highdigitsams.SAM_SA_23_S_300VM_9A83ME_LN: 32,
    highdigitsams.SAM_SA_23_S_300VM_9A82ME_LN: 32,

    highdigitsams.SAM_SA_17_Buk_M1_2_LN_9A310M1_2: 40,

}

"""
Units separated by tasks. This will include units for both countries. Be advised that unit could only belong to single task!

Following tasks are present:
* CAP - figther aircraft for CAP/Escort/Intercept
* CAS - CAS aircraft
* Transport - transport aircraft (used as targets in intercept operations)
* AWACS - awacs
* AntishipStrike - units that will engage shipping
* PinpointStrike - armor that will engage in ground war
* AirDefense - AA units
* Reconnaissance - units that will be used as targets in destroy insurgents operations
* Nothing - troops that will be used for helicopter transport operations
* Embarking - helicopters that will be used for helicopter transport operations
* Carriage - aircraft carriers
* CargoTransportation - ships that will be used as targets for ship intercept operations
"""
UNIT_BY_TASK = {
    CAP: [
        F_5E_3,
        Su_27,
        Su_33,
        Su_57,
        MiG_19P,
        MiG_21Bis,
        MiG_23MLD,
        MiG_25PD,
        MiG_29A,
        MiG_29S,
        MiG_31,
        FA_18C_hornet,
        F_15C,
        F_22A,
        F_14A_135_GR,
        F_14B,
        F_16A,
        F_16C_50,
        M_2000C,
        Mirage_2000_5,
        P_51D_30_NA,
        P_51D,
        MiG_29G,
        Su_30,
        J_11A,
        JF_17,
        F_4E,
        C_101CC,
        I_16,
        Bf_109K_4,
        FW_190D9,
        FW_190A8,
        SpitfireLFMkIXCW,
        SpitfireLFMkIX,
        A_4E_C,
        Rafale_M,
        SA342Mistral
    ],
    CAS: [
        AH_1W,
        AH_64A,
        AH_64D,
        AJS37,
        AV8BNA,
        A_10A,
        A_10C,
        A_10C_2,
        A_20G,
        B_17G,
        F_111F,
        B_1B,
        B_52H,
        F_117A,
        F_15E,
        F_86F_Sabre,
        Ju_88A4,
        Ka_50,
        L_39ZA,
        MB_339PAN,
        MQ_9_Reaper,
        MiG_15bis,
        MiG_27K,
        Mi_24V,
        Mi_28N,
        Mi_8MT,
        OH_58D,
        P_47D_30,
        P_47D_30bl1,
        P_47D_40,
        RQ_1A_Predator,
        Rafale_A_S,
        Rafale_B,
        S_3B,
        SA342L,
        SA342M,
        SA342Minigun,
        Su_17M4,
        Su_24M,
        Su_24MR,
        Su_25,
        Su_25T,
        Su_34,
        Tornado_GR4,
        Tornado_IDS,
        Tu_160,
        Tu_22M3,
        Tu_95MS,
        UH_1H,        
        SH_60B,
        WingLoong_I,
        Hercules
    ],
    Transport: [
        IL_76MD,
        An_26B,
        An_30M,
        Yak_40,
        C_130
    ],
    Refueling: [
        IL_78M,
        KC_135,
        KC130,
        S_3B_Tanker,
        KC135MPRS,
    ],
    AWACS: [
        E_3A,
        E_2C,
        A_50,
        KJ_2000
    ],
    PinpointStrike: [
        Armor.APC_MTLB,
        Armor.APC_MTLB,
        Armor.APC_MTLB,
        Armor.APC_MTLB,
        Armor.APC_MTLB,
        Armor.FDDM_Grad,
        Armor.FDDM_Grad,
        Armor.FDDM_Grad,
        Armor.FDDM_Grad,
        Armor.FDDM_Grad,
        Armor.ARV_BRDM_2,
        Armor.ARV_BRDM_2,
        Armor.ARV_BRDM_2,
        Armor.ARV_BTR_RD,
        Armor.ARV_BTR_RD,
        Armor.ARV_BTR_RD,
        Armor.ARV_BTR_RD,
        Armor.APC_BTR_80,
        Armor.APC_BTR_80,
        Armor.APC_BTR_80,
        Armor.APC_BTR_80,
        Armor.APC_BTR_80,
        Armor.APC_BTR_82A,
        Armor.APC_BTR_82A,
        Armor.IFV_BMP_1,
        Armor.IFV_BMP_1,
        Armor.IFV_BMP_1,
        Armor.IFV_BMP_2,
        Armor.IFV_BMP_2,
        Armor.IFV_BMP_3,
        Armor.IFV_BMP_3,
        Armor.IFV_BMD_1,
        Armor.ZBD_04A,
        Armor.ZBD_04A,
        Armor.ZBD_04A,
        Armor.MBT_T_55,
        Armor.MBT_T_55,
        Armor.MBT_T_55,
        Armor.MBT_T_72B,
        Armor.MBT_T_72B,
        Armor.MBT_T_72B3,
        Armor.MBT_T_72B3,
        Armor.MBT_T_80U,
        Armor.MBT_T_80U,
        Armor.MBT_T_90,
        Armor.ZTZ_96B,

        Armor.APC_Cobra,
        Armor.APC_Cobra,
        Armor.APC_Cobra,
        Armor.APC_Cobra,
        Armor.APC_M113,
        Armor.APC_M113,
        Armor.APC_M113,
        Armor.APC_M113,
        Armor.TPz_Fuchs,
        Armor.TPz_Fuchs,
        Armor.TPz_Fuchs,
        Armor.TPz_Fuchs,
        Armor.ATGM_M1045_HMMWV_TOW,
        Armor.ATGM_M1045_HMMWV_TOW,
        Armor.APC_M1043_HMMWV_Armament,
        Armor.APC_M1043_HMMWV_Armament,
        Armor.IFV_M2A2_Bradley,
        Armor.IFV_M2A2_Bradley,
        Armor.ATGM_M1134_Stryker,
        Armor.ATGM_M1134_Stryker,
        Armor.APC_M1126_Stryker_ICV,
        Armor.APC_M1126_Stryker_ICV,
        Armor.APC_M1126_Stryker_ICV,
        Armor.SPG_M1128_Stryker_MGS,
        Armor.IFV_MCV_80,
        Armor.IFV_MCV_80,
        Armor.IFV_MCV_80,
        Armor.IFV_LAV_25,
        Armor.IFV_LAV_25,
        Armor.IFV_Marder,
        Armor.IFV_Marder,
        Armor.IFV_Marder,
        Armor.IFV_Marder,
        Armor.MBT_M60A3_Patton,
        Armor.MBT_M60A3_Patton,
        Armor.MBT_M60A3_Patton,
        Armor.MBT_Leopard_1A3,
        Armor.MBT_Leopard_1A3,
        Armor.MBT_M1A2_Abrams,
        Armor.MBT_Leclerc,
        Armor.MBT_Leopard_2,
        Armor.MBT_Challenger_II,
        Armor.MBT_Merkava_Mk__4,

        Armor.MT_Pz_Kpfw_V_Panther_Ausf_G,
        Armor.MT_Pz_Kpfw_IV_Ausf_H,
        Armor.HT_Pz_Kpfw_VI_Tiger_I,
        Armor.HT_Pz_Kpfw_VI_Ausf__B_Tiger_II,
        Armor.APC_Sd_Kfz_251,
        Armor.APC_Sd_Kfz_251,
        Armor.APC_Sd_Kfz_251,
        Armor.APC_Sd_Kfz_251,
        Armor.AC_Sd_Kfz_234_2_Puma,
        Armor.AC_Sd_Kfz_234_2_Puma,
        Armor.MT_M4_Sherman,
        Armor.MT_M4A4_Sherman_Firefly,
        Armor.CT_Cromwell_IV,
        Armor.M30_Cargo_Carrier,
        Armor.M30_Cargo_Carrier,
        Armor.APC_M2A1,
        Armor.APC_M2A1,
        Armor.APC_M2A1,
        Armor.APC_M2A1,
        Armor.MT_Pz_Kpfw_V_Panther_Ausf_G,
        Armor.MT_Pz_Kpfw_IV_Ausf_H,
        Armor.HT_Pz_Kpfw_VI_Tiger_I,
        Armor.HT_Pz_Kpfw_VI_Ausf__B_Tiger_II,
        Armor.TD_Jagdpanther_G1,
        Armor.TD_Jagdpanzer_IV,
        Armor.Sd_Kfz_184_Elefant,
        Armor.APC_Sd_Kfz_251,
        Armor.AC_Sd_Kfz_234_2_Puma,
        Armor.MT_M4_Sherman,
        Armor.MT_M4A4_Sherman_Firefly,
        Armor.CT_Cromwell_IV,
        Armor.M30_Cargo_Carrier,
        Armor.M30_Cargo_Carrier,
        Armor.M30_Cargo_Carrier,
        Armor.APC_M2A1,
        Armor.APC_M2A1,
        Armor.CT_Centaur_IV,
        Armor.CT_Centaur_IV,
        Armor.HIT_Churchill_VII,
        Armor.LAC_M8_Greyhound,
        Armor.LAC_M8_Greyhound,
        Armor.TD_M10_GMC,
        Armor.TD_M10_GMC,
        Armor.StuG_III_Ausf__G,
        Armor.StuG_IV,
        Artillery.M12_GMC,
        Artillery.Sturmpanzer_IV_Brummbär,
        Armor.Daimler_Armoured_Car,
        Armor.LT_Mk_VII_Tetrarch,

        Artillery.MLRS_M270,
        Artillery.SPH_M109_Paladin,
        Artillery.SPH_2S9_Nona,
        Artillery.SPH_2S1_Gvozdika,
        Artillery.SPH_2S3_Akatsia,
        Artillery.SPH_2S19_Msta,
        Artillery.MLRS_BM_21_Grad,
        Artillery.MLRS_BM_21_Grad,
        Artillery.MLRS_9K57_Uragan_BM_27,
        Artillery.MLRS_9A52_Smerch,
        Artillery.SpGH_Dana,
        Artillery.M12_GMC,
        Artillery.Sturmpanzer_IV_Brummbär,

        AirDefence.AAA_ZU_23_on_Ural_375,
        AirDefence.AAA_ZU_23_Insurgent_on_Ural_375,
        AirDefence.AAA_ZSU_57_2,
        AirDefence.SPAAA_ZSU_23_4_Shilka,
        AirDefence.SAM_SA_8_Osa_9A33,
        AirDefence.SAM_SA_9_Strela_1_9P31,
        AirDefence.SAM_SA_13_Strela_10M3_9A35M3,
        AirDefence.SAM_SA_15_Tor_9A331,
        AirDefence.SAM_SA_19_Tunguska_2S6,
        AirDefence.SPAAA_Gepard,
        AirDefence.AAA_Vulcan_M163,
        AirDefence.SAM_Linebacker_M6,
        AirDefence.SAM_Chaparral_M48,
        AirDefence.SAM_Avenger_M1097,
        AirDefence.SAM_Roland_ADS,
        AirDefence.HQ_7_Self_Propelled_LN,
        AirDefence.AAA_8_8cm_Flak_18,
        AirDefence.AAA_8_8cm_Flak_36,
        AirDefence.AAA_8_8cm_Flak_37,
        AirDefence.AAA_8_8cm_Flak_41,
        AirDefence.AAA_Bofors_40mm,
        AirDefence.AAA_M1_37mm,
        AirDefence.AA_gun_QF_3_7,

        frenchpack.DIM__TOYOTA_BLUE,
        frenchpack.DIM__TOYOTA_DESERT,
        frenchpack.DIM__TOYOTA_GREEN,
        frenchpack.DIM__KAMIKAZE,

        frenchpack.AMX_10RCR,
        frenchpack.AMX_10RCR_SEPAR,
        frenchpack.ERC_90,
        frenchpack.TRM_2000_PAMELA,
        frenchpack.VAB__50,
        frenchpack.VAB_MEPHISTO,
        frenchpack.VAB_T20_13,
        frenchpack.VBL__50,
        frenchpack.VBL_AANF1,
        frenchpack.VBAE_CRAB,
        frenchpack.VBAE_CRAB_MMP,
        frenchpack.AMX_30B2,
        frenchpack.Leclerc_Serie_XXI,
        frenchpack.DIM__TOYOTA_BLUE,
        frenchpack.DIM__TOYOTA_GREEN,
        frenchpack.DIM__TOYOTA_DESERT,
        frenchpack.DIM__KAMIKAZE,

    ],
    AirDefence: [
    ],
    Reconnaissance: [Unarmed.Transport_M818, Unarmed.Transport_Ural_375, Unarmed.Transport_UAZ_469],
    Nothing: [Infantry.Infantry_M4, Infantry.Soldier_AK, ],
    Embarking: [],
    Carriage: [CVN_74_John_C__Stennis, LHA_1_Tarawa, CV_1143_5_Admiral_Kuznetsov, ],
    CargoTransportation: [Dry_cargo_ship_Ivanov, Bulk_cargo_ship_Yakushev, Tanker_Elnya_160, Armed_speedboat, ]
}

"""
Units from AirDefense category of UNIT_BY_TASK that will be removed from use if "No SAM" option is checked at the start of the game
"""
SAM_BAN = [
    AirDefence.SAM_Linebacker_M6,

    AirDefence.SAM_SA_9_Strela_1_9P31,
    AirDefence.SAM_SA_8_Osa_9A33,
    AirDefence.SAM_SA_19_Tunguska_2S6,
    AirDefence.SAM_SA_6_Kub_LN_2P25,
    AirDefence.SAM_SA_8_Osa_9A33,
    AirDefence.SAM_SA_3_S_125_LN_5P73,
    AirDefence.SAM_Hawk_PCP,
    AirDefence.SAM_SA_2_LN_SM_90,
    AirDefence.SAM_SA_11_Buk_LN_9A310M1,
]

"""
Used to convert SAM site parts to the corresponding site
"""
SAM_CONVERT = {
    AirDefence.SAM_SR_P_19: AirDefence.SAM_SA_3_S_125_LN_5P73,
    AirDefence.SAM_SA_3_S_125_TR_SNR: AirDefence.SAM_SA_3_S_125_LN_5P73,
    AirDefence.SAM_SA_3_S_125_LN_5P73: AirDefence.SAM_SA_3_S_125_LN_5P73,
    AirDefence.SAM_SA_6_Kub_LN_2P25: AirDefence.SAM_SA_6_Kub_LN_2P25,
    AirDefence.SAM_SA_6_Kub_STR_9S91: AirDefence.SAM_SA_6_Kub_LN_2P25,
    AirDefence.SAM_SA_10_S_300PS_LN_5P85C: AirDefence.SAM_SA_10_S_300PS_LN_5P85C,
    AirDefence.SAM_SA_10_S_300PS_SR_5N66M: AirDefence.SAM_SA_10_S_300PS_LN_5P85C,
    AirDefence.SAM_SA_10_S_300PS_TR_30N6: AirDefence.SAM_SA_10_S_300PS_LN_5P85C,
    AirDefence.SAM_SA_10_S_300PS_CP_54K6: AirDefence.SAM_SA_10_S_300PS_LN_5P85C,
    AirDefence.SAM_SA_10_S_300PS_SR_64H6E: AirDefence.SAM_SA_10_S_300PS_CP_54K6,
    AirDefence.SAM_Hawk_TR_AN_MPQ_46: AirDefence.SAM_Hawk_PCP,
    AirDefence.SAM_Hawk_SR_AN_MPQ_50: AirDefence.SAM_Hawk_PCP,
    AirDefence.SAM_Hawk_LN_M192: AirDefence.SAM_Hawk_PCP,
    'except': {
        # this radar is shared between the two S300's. if we attempt to find a SAM site at a base and can't find one
        #  model, we can safely assume the other was deployed
        # well, perhaps not safely, but we'll make the assumption anyway :p
        AirDefence.SAM_SA_10_S_300PS_TR_30N6: AirDefence.SAM_SA_10_S_300PS_CP_54K6,
        AirDefence.SAM_SR_P_19: AirDefence.SAM_SA_2_LN_SM_90
    }
}

"""
Units that will always be spawned in the air
"""
TAKEOFF_BAN: List[Type[FlyingType]] = [
]

"""
Units that will be always spawned in the air if launched from the carrier
"""
CARRIER_TAKEOFF_BAN: List[Type[FlyingType]] = [
    Su_33,  # Kuznecow is bugged in a way that only 2 aircraft could be spawned
]

"""
Units separated by country. 
country : DCS Country name
"""
FACTIONS = FactionLoader()

CARRIER_TYPE_BY_PLANE = {
    FA_18C_hornet: CVN_74_John_C__Stennis,
    F_14A_135_GR: CVN_74_John_C__Stennis,
    F_14B: CVN_74_John_C__Stennis,
    Ka_50: LHA_1_Tarawa,
    SA342M: LHA_1_Tarawa,
    UH_1H: LHA_1_Tarawa,
    Mi_8MT: LHA_1_Tarawa,
    AV8BNA: LHA_1_Tarawa,
}

"""
Aircraft payload overrides. Usually default loadout for the task is loaded during the mission generation.
Syntax goes as follows:

    `AircraftIdentifier`: {
        "Category": "PayloadName",
    },

where:
    * `AircraftIdentifier`: identifier of aircraft (the same that is used troughout the file)
    * "Category": (in double quotes) is one of the tasks: CAS, CAP, Intercept, Escort or "*"
    * "PayloadName": payload as found in resources/payloads/UNIT_TYPE.lua file. Sometimes this will match payload names 
                     in the mission editor, sometimes it doesn't
                     
Payload will be used for operation of following type, "*" category will be used always, no matter the operation.
"""

COMMON_OVERRIDE = {
    CAP: "CAP",
    Intercept: "CAP",
    CAS: "CAS",
    PinpointStrike: "STRIKE",
    SEAD: "SEAD",
    AntishipStrike: "ANTISHIP",
    GroundAttack: "STRIKE",
    Escort: "CAP",
    RunwayAttack: "RUNWAY_ATTACK",
    FighterSweep: "CAP",
    AWACS: "AEW&C",
}

"""
This is a list of mappings from the FlightType of a Flight to the type of payload defined in the
resources/payloads/UNIT_TYPE.lua file. A Flight has no concept of a PyDCS task, so COMMON_OVERRIDE cannot be
used here. This is used in the payload editor, for setting the default loadout of an object.
The left element is the FlightType name, and the right element is a tuple containing what is used in the lua file.
Some aircraft differ from the standard loadout names, so those have been included here too.
The priority goes from first to last - the first element in the tuple will be tried first, then the second, etc.
"""

EXPANDED_TASK_PAYLOAD_OVERRIDE = {
    "TARCAP": ("CAP HEAVY", "CAP"),
    "BARCAP": ("CAP HEAVY", "CAP"),
    "CAS": ("CAS MAVERICK F", "CAS"),
    "INTERCEPTION": ("CAP HEAVY", "CAP"),
    "STRIKE": ("STRIKE",),    
    "ANTISHIP": ("ANTISHIP",),
    "SEAD": ("SEAD",),
    "DEAD": ("SEAD",),
    "ESCORT": ("CAP HEAVY", "CAP"),
    "BAI": ( "BAI", "CAS MAVERICK F", "CAS"),
    "SWEEP": ("CAP HEAVY", "CAP"),
    "OCA_RUNWAY": ("RUNWAY_ATTACK","RUNWAY_STRIKE","STRIKE"),
    "OCA_AIRCRAFT": ("OCA","CAS MAVERICK F", "CAS")
}

PLANE_PAYLOAD_OVERRIDES: Dict[Type[PlaneType], Dict[Type[Task], str]] = {

    B_1B: COMMON_OVERRIDE,
    B_52H: COMMON_OVERRIDE,
    F_117A: COMMON_OVERRIDE,
    F_15E: COMMON_OVERRIDE,
    FA_18C_hornet: {
        CAP: "CAP HEAVY",
        Intercept: "CAP HEAVY",
        CAS: "CAS MAVERICK F",
        PinpointStrike: "STRIKE",
        SEAD: "SEAD",
        AntishipStrike: "ANTISHIP",
        GroundAttack: "STRIKE",
        Escort: "CAP HEAVY",
        FighterSweep: "CAP HEAVY",
    },
    F_A_18C: {
        CAP: "CAP HEAVY",
        Intercept: "CAP HEAVY",
        CAS: "CAS MAVERICK F",
        PinpointStrike: "STRIKE",
        SEAD: "SEAD",
        AntishipStrike: "ANTISHIP",
        GroundAttack: "STRIKE",
        Escort: "CAP HEAVY",
        FighterSweep: "CAP HEAVY",
    },
    Tu_160: {
        PinpointStrike: "Kh-65*12",
    },
    Tu_22M3: COMMON_OVERRIDE,
    Tu_95MS: COMMON_OVERRIDE,
    A_10A: COMMON_OVERRIDE,
    A_10C: COMMON_OVERRIDE,
    A_10C_2: COMMON_OVERRIDE,
    AV8BNA: COMMON_OVERRIDE,
    C_101CC: COMMON_OVERRIDE,
    F_5E_3: COMMON_OVERRIDE,
    F_14A_135_GR: COMMON_OVERRIDE,
    F_14B: COMMON_OVERRIDE,
    F_15C: COMMON_OVERRIDE,
    F_111F: COMMON_OVERRIDE,
    F_22A: COMMON_OVERRIDE,
    F_16C_50: COMMON_OVERRIDE,
    JF_17: COMMON_OVERRIDE,
    M_2000C: COMMON_OVERRIDE,
    MiG_15bis: COMMON_OVERRIDE,
    MiG_19P: COMMON_OVERRIDE,
    MiG_21Bis: COMMON_OVERRIDE,
    AJS37: COMMON_OVERRIDE,
    Su_25T: COMMON_OVERRIDE,
    Su_25: COMMON_OVERRIDE,
    Su_27: COMMON_OVERRIDE,
    Su_33: COMMON_OVERRIDE,
    MiG_29A: COMMON_OVERRIDE,
    MiG_29G: COMMON_OVERRIDE,
    MiG_29S: COMMON_OVERRIDE,
    Su_24M: COMMON_OVERRIDE,
    Su_30: COMMON_OVERRIDE,
    Su_34: COMMON_OVERRIDE,
    Su_57: COMMON_OVERRIDE,
    MiG_23MLD: COMMON_OVERRIDE,
    MiG_27K: COMMON_OVERRIDE,
    Tornado_GR4: COMMON_OVERRIDE,
    Tornado_IDS: COMMON_OVERRIDE,
    Mirage_2000_5: COMMON_OVERRIDE,
    MiG_31: COMMON_OVERRIDE,
    S_3B: COMMON_OVERRIDE,
    SA342M: COMMON_OVERRIDE,
    SA342L: COMMON_OVERRIDE,
    SA342Mistral: COMMON_OVERRIDE,
    Mi_8MT: COMMON_OVERRIDE,
    Mi_24V: COMMON_OVERRIDE,
    Mi_28N: COMMON_OVERRIDE,
    Ka_50: COMMON_OVERRIDE,
    L_39ZA: COMMON_OVERRIDE,
    L_39C: COMMON_OVERRIDE,
    Su_17M4: COMMON_OVERRIDE,
    F_4E: COMMON_OVERRIDE,
    P_47D_30: COMMON_OVERRIDE,
    P_47D_30bl1: COMMON_OVERRIDE,
    P_47D_40: COMMON_OVERRIDE,
    B_17G: COMMON_OVERRIDE,
    P_51D: COMMON_OVERRIDE,
    P_51D_30_NA: COMMON_OVERRIDE,
    FW_190D9: COMMON_OVERRIDE,
    FW_190A8: COMMON_OVERRIDE,
    Bf_109K_4: COMMON_OVERRIDE,
    I_16: COMMON_OVERRIDE,
    SpitfireLFMkIXCW: COMMON_OVERRIDE,
    SpitfireLFMkIX: COMMON_OVERRIDE,
    A_20G: COMMON_OVERRIDE,
    A_4E_C: COMMON_OVERRIDE,
    MB_339PAN: COMMON_OVERRIDE,
    Rafale_M: COMMON_OVERRIDE,
    Rafale_A_S: COMMON_OVERRIDE,
    Rafale_B: COMMON_OVERRIDE,
    OH_58D: COMMON_OVERRIDE,
    F_16A: COMMON_OVERRIDE,
    MQ_9_Reaper: COMMON_OVERRIDE,
    RQ_1A_Predator: COMMON_OVERRIDE,
    WingLoong_I: COMMON_OVERRIDE,
    AH_1W: COMMON_OVERRIDE,
    AH_64D: COMMON_OVERRIDE,
    AH_64A: COMMON_OVERRIDE,
    SH_60B: COMMON_OVERRIDE,
    Hercules: COMMON_OVERRIDE,

    Su_25TM: {
        SEAD: "Kh-31P*2_Kh-25ML*4_R-73*2_L-081_MPS410",
    },

}

"""
Aircraft livery overrides. Syntax as follows:

    `Identifier`: "LiveryName",

`Identifier` is aircraft identifier (as used troughout the file) and "LiveryName" (with double quotes) 
is livery name as found in mission editor.
"""
PLANE_LIVERY_OVERRIDES = {
    FA_18C_hornet: "VFA-34",  # default livery for the hornet is blue angels one
}

"""
Possible time periods for new games

    `Name`: daytime(day, month, year),

`Identifier` is the name that will appear in the menu
The object is a python datetime object
"""
TIME_PERIODS = {
    "WW2 - Winter [1944]": datetime(1944, 1, 1),
    "WW2 - Spring [1944]": datetime(1944, 4, 1),
    "WW2 - Summer [1944]": datetime(1944, 6, 1),
    "WW2 - Fall [1944]": datetime(1944, 10, 1),
    "Early Cold War - Winter [1952]": datetime(1952, 1, 1),
    "Early Cold War - Spring [1952]": datetime(1952, 4, 1),
    "Early Cold War - Summer [1952]": datetime(1952, 6, 1),
    "Early Cold War - Fall [1952]": datetime(1952, 10, 1),
    "Cold War - Winter [1970]": datetime(1970, 1, 1),
    "Cold War - Spring [1970]": datetime(1970, 4, 1),
    "Cold War - Summer [1970]": datetime(1970, 6, 1),
    "Cold War - Fall [1970]": datetime(1970, 10, 1),
    "Late Cold War - Winter [1985]": datetime(1985, 1, 1),
    "Late Cold War - Spring [1985]": datetime(1985, 4, 1),
    "Late Cold War - Summer [1985]": datetime(1985, 6, 1),
    "Late Cold War - Fall [1985]": datetime(1985, 10, 1),
    "Gulf War - Winter [1990]": datetime(1990, 1, 1),
    "Gulf War - Spring [1990]": datetime(1990, 4, 1),
    "Gulf War - Summer [1990]": datetime(1990, 6, 1),
    "Gulf War - Fall [1990]": datetime(1990, 10, 1),
    "Modern - Winter [2010]": datetime(2010, 1, 1),
    "Modern - Spring [2010]": datetime(2010, 4, 1),
    "Modern - Summer [2010]": datetime(2010, 6, 1),
    "Modern - Fall [2010]": datetime(2010, 10, 1),
    "Georgian War [2008]": datetime(2008, 8, 7),
    "Syrian War [2011]": datetime(2011, 3, 15),
    "6 days war [1967]": datetime(1967, 6, 5),
    "Yom Kippour War [1973]": datetime(1973, 10, 6),
    "Lebanon War [1982]": datetime(1982, 6, 6),
    "Arab-Israeli War [1948]": datetime(1948, 5, 15),
}

REWARDS = {
    "power": 4, "warehouse": 2, "ware": 2, "fuel": 2, "ammo": 2,
    "farp": 1, "fob": 1, "factory": 10, "comms": 10, "oil": 10,
    "derrick": 8
}

CARRIER_CAPABLE = [
    FA_18C_hornet,
    F_14A_135_GR,
    F_14B,
    AV8BNA,
    Su_33,
    A_4E_C,
    Rafale_M,
    S_3B,
    E_2C,

    UH_1H,
    Mi_8MT,
    Ka_50,
    AH_1W,
    OH_58D,
    UH_60A,
    SH_60B,

    SA342L,
    SA342M,
    SA342Minigun,
    SA342Mistral,
]

LHA_CAPABLE = [
    AV8BNA,

    UH_1H,
    Mi_8MT,
    Ka_50,
    AH_1W,
    OH_58D,
    UH_60A,
    SH_60B,

    SA342L,
    SA342M,
    SA342Minigun,
    SA342Mistral
]

"""
---------- END OF CONFIGURATION SECTION
"""

UnitsDict = Dict[UnitType, int]
PlaneDict = Dict[FlyingType, int]
HeliDict = Dict[HelicopterType, int]
ArmorDict = Dict[VehicleType, int]
ShipDict = Dict[ShipType, int]
AirDefenseDict = Dict[AirDefence, int]

AssignedUnitsDict = Dict[Type[UnitType], Tuple[int, int]]
TaskForceDict = Dict[Type[MainTask], AssignedUnitsDict]

StartingPosition = Union[ShipGroup, StaticGroup, Airport, Point]


def upgrade_to_supercarrier(unit, name: str):
    if unit == CVN_74_John_C__Stennis:
        if name == "CVN-71 Theodore Roosevelt":
            return CVN_71_Theodore_Roosevelt
        elif name == "CVN-72 Abraham Lincoln":
            return CVN_72_Abraham_Lincoln
        elif name == "CVN-73 George Washington":
            return CVN_73_George_Washington
        elif name == "CVN-75 Harry S. Truman":
            return CVN_75_Harry_S__Truman
        else:
            return CVN_71_Theodore_Roosevelt
    elif unit == CV_1143_5_Admiral_Kuznetsov:
        return CV_1143_5_Admiral_Kuznetsov_2017
    else:
        return unit


def unit_task(unit: UnitType) -> Optional[Task]:
    for task, units in UNIT_BY_TASK.items():
        if unit in units:
            return task

    if unit in SAM_CONVERT:
        return unit_task(SAM_CONVERT[unit])

    print(unit.name + " cause issue")
    return None


def find_unittype(for_task: Task, country_name: str) -> List[Type[UnitType]]:
    return [x for x in UNIT_BY_TASK[for_task] if x in FACTIONS[country_name].units]


MANPADS: List[VehicleType] = [
    AirDefence.SAM_SA_18_Igla_MANPADS,
    AirDefence.SAM_SA_18_Igla_S_MANPADS,
    AirDefence.Stinger_MANPADS
]

INFANTRY: List[VehicleType] = [
    Infantry.Paratrooper_AKS, Infantry.Paratrooper_AKS, Infantry.Paratrooper_AKS, Infantry.Paratrooper_AKS,
    Infantry.Paratrooper_AKS,
    Infantry.Soldier_RPG,
    Infantry.Infantry_M4, Infantry.Infantry_M4, Infantry.Infantry_M4, Infantry.Infantry_M4, Infantry.Infantry_M4,
    Infantry.Soldier_M249,
    Artillery._2B11_mortar,
    Infantry.Soldier_AK, Infantry.Soldier_AK, Infantry.Soldier_AK, Infantry.Soldier_AK, Infantry.Soldier_AK,
    Infantry.Paratrooper_RPG_16,
    Infantry.Georgian_soldier_with_M4, Infantry.Georgian_soldier_with_M4, Infantry.Georgian_soldier_with_M4,
    Infantry.Georgian_soldier_with_M4,
    Infantry.Infantry_Soldier_Rus, Infantry.Infantry_Soldier_Rus, Infantry.Infantry_Soldier_Rus,
    Infantry.Infantry_Soldier_Rus,
    Infantry.Infantry_SMLE_No_4_Mk_1, Infantry.Infantry_SMLE_No_4_Mk_1, Infantry.Infantry_SMLE_No_4_Mk_1,
    Infantry.Infantry_Mauser_98, Infantry.Infantry_Mauser_98, Infantry.Infantry_Mauser_98,
    Infantry.Infantry_Mauser_98,
    Infantry.Infantry_M1_Garand, Infantry.Infantry_M1_Garand, Infantry.Infantry_M1_Garand,
    Infantry.Infantry_Soldier_Insurgents, Infantry.Infantry_Soldier_Insurgents, Infantry.Infantry_Soldier_Insurgents
]


def find_manpad(country_name: str) -> List[VehicleType]:
    return [x for x in MANPADS if x in FACTIONS[country_name].infantry_units]


def find_infantry(country_name: str, allow_manpad: bool = False) -> List[VehicleType]:
    if allow_manpad:
        inf = INFANTRY + MANPADS
    else:
        inf = INFANTRY
    return [x for x in inf if x in FACTIONS[country_name].infantry_units]


def unit_type_name(unit_type) -> str:
    return unit_type.id and unit_type.id or unit_type.name


def unit_type_name_2(unit_type) -> str:
    return unit_type.name and unit_type.name or unit_type.id

def unit_get_expanded_info(country_name: str, unit_type, request_type: str) -> str:
    original_name = unit_type.name and unit_type.name or unit_type.id
    default_value = None
    faction_value = None
    with UNITINFOTEXT_PATH.open("r", encoding="utf-8") as fdata:
        data = json.load(fdata, encoding="utf-8")
    type_exists = data.get(original_name)
    if type_exists is not None:
        for faction in type_exists:
            if default_value is None:
                default_exists = faction.get("default")
                if default_exists is not None:
                    default_value = default_exists.get(request_type)
            if faction_value is None:
                faction_exists = faction.get(country_name)
                if faction_exists is not None:
                    faction_value = faction_exists.get(request_type)
    if default_value is None:
        if request_type == "text":
            return "WIP - This unit doesn't have any description text yet."
        if request_type == "name":
            return original_name
        else:
            return "Unknown"
    if faction_value is None:
        return default_value
    return faction_value

def unit_type_from_name(name: str) -> Optional[Type[UnitType]]:
    if name in vehicle_map:
        return vehicle_map[name]
    elif name in plane_map:
        return plane_map[name]
    elif name in ship_map:
        return ship_map[name]
    if name in helicopter_map:
        return helicopter_map[name]
    else:
        return None


def unit_type_of(unit: Unit) -> UnitType:
    if isinstance(unit, Vehicle):
        return vehicle_map[unit.type]
    elif isinstance(unit, Ship):
        return ship_map[unit.type]
    else:
        return unit.type


def task_name(task) -> str:
    if task == AirDefence:
        return "AirDefence"
    elif task == Embarking:
        return "Transportation"
    elif task == PinpointStrike:
        return "Frontline units"
    else:
        return task.name


def choose_units(for_task: Task, factor: float, count: int, country: str) -> List[UnitType]:
    suitable_unittypes = find_unittype(for_task, country)
    suitable_unittypes = [x for x in suitable_unittypes if x not in helicopter_map.values()]
    suitable_unittypes.sort(key=lambda x: PRICES[x])

    idx = int(len(suitable_unittypes) * factor)
    variety = int(count + count * factor / 2)

    index_start = min(idx, len(suitable_unittypes) - variety)
    index_end = min(idx + variety, len(suitable_unittypes))
    return list(set(suitable_unittypes[index_start:index_end]))


def unitdict_append(unit_dict: UnitsDict, unit_type: UnitType, count: int):
    unit_dict[unit_type] = unit_dict.get(unit_type, 0) + 1


def unitdict_merge(a: UnitsDict, b: UnitsDict) -> UnitsDict:
    b = b.copy()
    for k, v in a.items():
        b[k] = b.get(k, 0) + v

    return b


def unitdict_split(unit_dict: UnitsDict, count: int):
    buffer_dict: Dict[UnitType, int] = {}
    for unit_type, unit_count in unit_dict.items():
        for _ in range(unit_count):
            unitdict_append(buffer_dict, unit_type, 1)
            if sum(buffer_dict.values()) >= count:
                yield buffer_dict
                buffer_dict = {}

    if len(buffer_dict):
        yield buffer_dict


def unitdict_restrict_count(unit_dict: UnitsDict, total_count: int) -> UnitsDict:
    if total_count == 0:
        return {}

    groups = list(unitdict_split(unit_dict, total_count))
    if len(groups) > 0:
        return groups[0]
    else:
        return {}


def assigned_units_split(fd: AssignedUnitsDict) -> Tuple[PlaneDict, PlaneDict]:
    return {k: v1 for k, (v1, v2) in fd.items()}, {k: v2 for k, (v1, v2) in fd.items()},


def assigned_units_from(d: PlaneDict) -> AssignedUnitsDict:
    return {k: (v, 0) for k, v in d.items()}


def assignedunits_split_to_count(dict: AssignedUnitsDict, count: int):
    buffer_dict: Dict[Type[UnitType], Tuple[int, int]] = {}
    for unit_type, (unit_count, client_count) in dict.items():
        for _ in range(unit_count):
            new_count, new_client_count = buffer_dict.get(unit_type, (0, 0))

            new_count += 1

            if client_count > 0:
                new_client_count += 1
                client_count -= 1

            buffer_dict[unit_type] = new_count, new_client_count
            if new_count >= count:
                yield buffer_dict
                buffer_dict = {}

    if len(buffer_dict):
        yield buffer_dict


def unitdict_from(fd: AssignedUnitsDict) -> Dict:
    return {k: v1 for k, (v1, v2) in fd.items()}


def country_id_from_name(name):
    for k, v in country_dict.items():
        if v.name == name:
            return k
    return -1


def _validate_db():
    # check unit by task uniquity
    total_set = set()
    for t, unit_collection in UNIT_BY_TASK.items():
        for unit_type in set(unit_collection):
            assert unit_type not in total_set, "{} is duplicate for task {}".format(unit_type, t)
            total_set.add(unit_type)

    # check prices
    for unit_type in total_set:
        assert unit_type in PRICES, "{} not in prices".format(unit_type)


_validate_db()


class DefaultLiveries:
    class Default(Enum):
        af_standard = ""


OH_58D.Liveries = DefaultLiveries
F_16C_50.Liveries = DefaultLiveries
P_51D_30_NA.Liveries = DefaultLiveries
Ju_88A4.Liveries = DefaultLiveries
B_17G.Liveries = DefaultLiveries
