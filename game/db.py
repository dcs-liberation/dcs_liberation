import json
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import List, Optional, Type, Union

from dcs.countries import country_dict
from dcs.helicopters import (
    AH_1W,
    AH_64A,
    AH_64D,
    CH_47D,
    CH_53E,
    Ka_50,
    Mi_24V,
    Mi_26,
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
    C_17A,
    E_3A,
    E_2C,
    FA_18C_hornet,
    FW_190A8,
    FW_190D9,
    F_117A,
    F_14A_135_GR,
    F_14B,
    F_15C,
    F_15E,
    F_16A,
    F_16C_50,
    F_4E,
    F_5E_3,
    F_86F_Sabre,
    IL_76MD,
    IL_78M,
    JF_17,
    J_11A,
    Ju_88A4,
    KC130,
    KC_135,
    KC135MPRS,
    KJ_2000,
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
    I_16,
    Tu_142,
)
from dcs.ships import (
    Boat_Armed_Hi_speed,
    Bulker_Yakushev,
    CVN_71_Theodore_Roosevelt,
    CVN_72_Abraham_Lincoln,
    CVN_73_George_Washington,
    CVN_74_John_C__Stennis,
    CVN_75_Harry_S__Truman,
    CV_1143_5_Admiral_Kuznetsov,
    CV_1143_5_Admiral_Kuznetsov_2017,
    Cargo_Ivanov,
    LHA_1_Tarawa,
    Tanker_Elnya_160,
    ship_map,
)
from dcs.task import (
    AWACS,
    CAP,
    CAS,
    CargoTransportation,
    Embarking,
    MainTask,
    Nothing,
    PinpointStrike,
    Reconnaissance,
    Refueling,
    Transport,
)
from dcs.terrain.terrain import Airport
from dcs.unit import Ship, Unit, Vehicle
from dcs.unitgroup import ShipGroup, StaticGroup
from dcs.unittype import FlyingType, UnitType, VehicleType
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
from pydcs_extensions.su57.su57 import Su_57

UNITINFOTEXT_PATH = Path("./resources/units/unit_info_text.json")

plane_map["A-4E-C"] = A_4E_C
plane_map["F-22A"] = F_22A
plane_map["MB-339PAN"] = MB_339PAN
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
vehicle_map[
    highdigitsams.SAM_SA_10B_S_300PS_54K6_CP.id
] = highdigitsams.SAM_SA_10B_S_300PS_54K6_CP
vehicle_map[
    highdigitsams.SAM_SA_10B_S_300PS_5P85SE_LN.id
] = highdigitsams.SAM_SA_10B_S_300PS_5P85SE_LN
vehicle_map[
    highdigitsams.SAM_SA_10B_S_300PS_5P85SU_LN.id
] = highdigitsams.SAM_SA_10B_S_300PS_5P85SU_LN
vehicle_map[
    highdigitsams.SAM_SA_10__5V55RUD__S_300PS_LN_5P85CE.id
] = highdigitsams.SAM_SA_10__5V55RUD__S_300PS_LN_5P85CE
vehicle_map[
    highdigitsams.SAM_SA_10__5V55RUD__S_300PS_LN_5P85DE.id
] = highdigitsams.SAM_SA_10__5V55RUD__S_300PS_LN_5P85DE
vehicle_map[
    highdigitsams.SAM_SA_10B_S_300PS_30N6_TR.id
] = highdigitsams.SAM_SA_10B_S_300PS_30N6_TR
vehicle_map[
    highdigitsams.SAM_SA_10B_S_300PS_40B6M_TR.id
] = highdigitsams.SAM_SA_10B_S_300PS_40B6M_TR
vehicle_map[
    highdigitsams.SAM_SA_10B_S_300PS_40B6MD_SR.id
] = highdigitsams.SAM_SA_10B_S_300PS_40B6MD_SR
vehicle_map[
    highdigitsams.SAM_SA_10B_S_300PS_64H6E_SR.id
] = highdigitsams.SAM_SA_10B_S_300PS_64H6E_SR
vehicle_map[
    highdigitsams.SAM_SA_20_S_300PMU1_CP_54K6.id
] = highdigitsams.SAM_SA_20_S_300PMU1_CP_54K6
vehicle_map[
    highdigitsams.SAM_SA_20_S_300PMU1_TR_30N6E.id
] = highdigitsams.SAM_SA_20_S_300PMU1_TR_30N6E
vehicle_map[
    highdigitsams.SAM_SA_20_S_300PMU1_TR_30N6E_truck.id
] = highdigitsams.SAM_SA_20_S_300PMU1_TR_30N6E_truck
vehicle_map[
    highdigitsams.SAM_SA_20_S_300PMU1_SR_5N66E.id
] = highdigitsams.SAM_SA_20_S_300PMU1_SR_5N66E
vehicle_map[
    highdigitsams.SAM_SA_20_S_300PMU1_SR_64N6E.id
] = highdigitsams.SAM_SA_20_S_300PMU1_SR_64N6E
vehicle_map[
    highdigitsams.SAM_SA_20_S_300PMU1_LN_5P85CE.id
] = highdigitsams.SAM_SA_20_S_300PMU1_LN_5P85CE
vehicle_map[
    highdigitsams.SAM_SA_20_S_300PMU1_LN_5P85DE.id
] = highdigitsams.SAM_SA_20_S_300PMU1_LN_5P85DE
vehicle_map[
    highdigitsams.SAM_SA_20B_S_300PMU2_CP_54K6E2.id
] = highdigitsams.SAM_SA_20B_S_300PMU2_CP_54K6E2
vehicle_map[
    highdigitsams.SAM_SA_20B_S_300PMU2_TR_92H6E_truck.id
] = highdigitsams.SAM_SA_20B_S_300PMU2_TR_92H6E_truck
vehicle_map[
    highdigitsams.SAM_SA_20B_S_300PMU2_SR_64N6E2.id
] = highdigitsams.SAM_SA_20B_S_300PMU2_SR_64N6E2
vehicle_map[
    highdigitsams.SAM_SA_20B_S_300PMU2_LN_5P85SE2.id
] = highdigitsams.SAM_SA_20B_S_300PMU2_LN_5P85SE2
vehicle_map[
    highdigitsams.SAM_SA_12_S_300V_9S457_CP.id
] = highdigitsams.SAM_SA_12_S_300V_9S457_CP
vehicle_map[
    highdigitsams.SAM_SA_12_S_300V_9A82_LN.id
] = highdigitsams.SAM_SA_12_S_300V_9A82_LN
vehicle_map[
    highdigitsams.SAM_SA_12_S_300V_9A83_LN.id
] = highdigitsams.SAM_SA_12_S_300V_9A83_LN
vehicle_map[
    highdigitsams.SAM_SA_12_S_300V_9S15_SR.id
] = highdigitsams.SAM_SA_12_S_300V_9S15_SR
vehicle_map[
    highdigitsams.SAM_SA_12_S_300V_9S19_SR.id
] = highdigitsams.SAM_SA_12_S_300V_9S19_SR
vehicle_map[
    highdigitsams.SAM_SA_12_S_300V_9S32_TR.id
] = highdigitsams.SAM_SA_12_S_300V_9S32_TR
vehicle_map[
    highdigitsams.SAM_SA_23_S_300VM_9S457ME_CP.id
] = highdigitsams.SAM_SA_23_S_300VM_9S457ME_CP
vehicle_map[
    highdigitsams.SAM_SA_23_S_300VM_9S15M2_SR.id
] = highdigitsams.SAM_SA_23_S_300VM_9S15M2_SR
vehicle_map[
    highdigitsams.SAM_SA_23_S_300VM_9S19M2_SR.id
] = highdigitsams.SAM_SA_23_S_300VM_9S19M2_SR
vehicle_map[
    highdigitsams.SAM_SA_23_S_300VM_9S32ME_TR.id
] = highdigitsams.SAM_SA_23_S_300VM_9S32ME_TR
vehicle_map[
    highdigitsams.SAM_SA_23_S_300VM_9A83ME_LN.id
] = highdigitsams.SAM_SA_23_S_300VM_9A83ME_LN
vehicle_map[
    highdigitsams.SAM_SA_23_S_300VM_9A82ME_LN.id
] = highdigitsams.SAM_SA_23_S_300VM_9A82ME_LN
vehicle_map[
    highdigitsams.SAM_SA_17_Buk_M1_2_LN_9A310M1_2.id
] = highdigitsams.SAM_SA_17_Buk_M1_2_LN_9A310M1_2
vehicle_map[
    highdigitsams.SAM_SA_2__V759__LN_SM_90.id
] = highdigitsams.SAM_SA_2__V759__LN_SM_90
vehicle_map[highdigitsams.SAM_HQ_2_LN_SM_90.id] = highdigitsams.SAM_HQ_2_LN_SM_90
vehicle_map[
    highdigitsams.SAM_SA_3__V_601P__LN_5P73.id
] = highdigitsams.SAM_SA_3__V_601P__LN_5P73
vehicle_map[
    highdigitsams.SAM_SA_24_Igla_S_manpad.id
] = highdigitsams.SAM_SA_24_Igla_S_manpad
vehicle_map[
    highdigitsams.SAM_SA_14_Strela_3_manpad.id
] = highdigitsams.SAM_SA_14_Strela_3_manpad
vehicle_map[highdigitsams.Polyana_D4M1_C2_node.id] = highdigitsams.Polyana_D4M1_C2_node
vehicle_map[
    highdigitsams._34Ya6E_Gazetchik_E_decoy.id
] = highdigitsams._34Ya6E_Gazetchik_E_decoy

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
For example, player accessible Hornet is called `FA_18C_hornet`, and MANPAD Igla is called `AirDefence.MANPADS_SA_18_Igla_S_Grouse`
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
    CH_47D: 4,
    CH_53E: 4,
    UH_60A: 4,
    Mi_26: 4,
    # Bombers
    B_52H: 35,
    B_1B: 50,
    F_117A: 100,
    Tu_160: 50,
    Tu_22M3: 40,
    Tu_95MS: 35,
    Tu_142: 35,
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
    C_17A: 20,
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
    # armor
    Armor.APC_MTLB: 4,
    Artillery.Grad_MRL_FDDM__FC: 4,
    Armor.Scout_BRDM_2: 6,
    Armor.APC_BTR_RD: 6,
    Armor.APC_BTR_80: 8,
    Armor.IFV_BTR_82A: 10,
    Armor.MBT_T_55: 18,
    Armor.MBT_T_72B: 20,
    Armor.MBT_T_72B3: 25,
    Armor.MBT_T_80U: 25,
    Armor.MBT_T_90: 30,
    Armor.IFV_BMD_1: 8,
    Armor.IFV_BMP_1: 14,
    Armor.IFV_BMP_2: 16,
    Armor.IFV_BMP_3: 18,
    Armor.LT_PT_76: 9,
    Armor.ZBD_04A: 12,
    Armor.ZTZ_96B: 30,
    Armor.Scout_Cobra: 4,
    Armor.APC_M113: 6,
    Armor.Scout_HMMWV: 2,
    Armor.ATGM_HMMWV: 8,
    Armor.ATGM_VAB_Mephisto: 12,
    Armor.IFV_M2A2_Bradley: 12,
    Armor.IFV_M1126_Stryker_ICV: 10,
    Armor.SPG_Stryker_MGS: 14,
    Armor.ATGM_Stryker: 12,
    Armor.MBT_M60A3_Patton: 16,
    Armor.MBT_M1A2_Abrams: 25,
    Armor.MBT_Leclerc: 25,
    Armor.MBT_Leopard_1A3: 18,
    Armor.MBT_Leopard_2A4: 20,
    Armor.MBT_Leopard_2A4_Trs: 20,
    Armor.MBT_Leopard_2A5: 22,
    Armor.MBT_Leopard_2A6M: 25,
    Armor.MBT_Merkava_IV: 25,
    Armor.APC_TPz_Fuchs: 5,
    Armor.MBT_Challenger_II: 25,
    Armor.MBT_Chieftain_Mk_3: 20,
    Armor.IFV_Marder: 10,
    Armor.IFV_Warrior: 10,
    Armor.IFV_LAV_25: 7,
    Artillery.MLRS_M270_227mm: 55,
    Artillery.SPH_M109_Paladin_155mm: 25,
    Artillery.SPM_2S9_Nona_120mm_M: 12,
    Artillery.SPH_2S1_Gvozdika_122mm: 18,
    Artillery.SPH_2S3_Akatsia_152mm: 24,
    Artillery.SPH_2S19_Msta_152mm: 30,
    Artillery.MLRS_BM_21_Grad_122mm: 15,
    Artillery.MLRS_9K57_Uragan_BM_27_220mm: 50,
    Artillery.MLRS_9A52_Smerch_HE_300mm: 40,
    Artillery.Mortar_2B11_120mm: 4,
    Artillery.SPH_Dana_vz77_152mm: 26,
    Artillery.PLZ_05: 25,
    Artillery.SPH_T155_Firtina_155mm: 28,
    Unarmed.LUV_UAZ_469_Jeep: 3,
    Unarmed.Truck_Ural_375: 3,
    Infantry.Infantry_M4: 1,
    Infantry.Infantry_AK_74: 1,
    Unarmed.Truck_M818_6x6: 3,
    # WW2
    Armor.MT_Pz_Kpfw_V_Panther_Ausf_G: 24,
    Armor.Tk_PzIV_H: 16,
    Armor.HT_Pz_Kpfw_VI_Tiger_I: 24,
    Armor.HT_Pz_Kpfw_VI_Ausf__B_Tiger_II: 26,
    Armor.SPG_Jagdpanther_G1: 18,
    Armor.SPG_Jagdpanzer_IV: 11,
    Armor.SPG_Sd_Kfz_184_Elefant: 18,
    Armor.APC_Sd_Kfz_251_Halftrack: 4,
    Armor.IFV_Sd_Kfz_234_2_Puma: 8,
    Armor.Tk_M4_Sherman: 12,
    Armor.MT_M4A4_Sherman_Firefly: 16,
    Armor.CT_Cromwell_IV: 12,
    Unarmed.Carrier_M30_Cargo: 2,
    Armor.APC_M2A1_Halftrack: 4,
    Armor.CT_Centaur_IV: 10,
    Armor.HIT_Churchill_VII: 16,
    Armor.Car_M8_Greyhound_Armored: 8,
    Armor.SPG_M10_GMC: 14,
    Armor.SPG_StuG_III_Ausf__G: 12,
    Armor.SPG_StuG_IV: 14,
    Artillery.SPG_M12_GMC_155mm: 10,
    Armor.SPG_Sturmpanzer_IV_Brummbar: 10,
    Armor.Car_Daimler_Armored: 8,
    Armor.LT_Mk_VII_Tetrarch: 8,
    Unarmed.Tractor_M4_Hi_Speed: 2,
    # ship
    CV_1143_5_Admiral_Kuznetsov: 100,
    CVN_74_John_C__Stennis: 100,
    LHA_1_Tarawa: 50,
    Bulker_Yakushev: 10,
    Boat_Armed_Hi_speed: 10,
    Cargo_Ivanov: 10,
    Tanker_Elnya_160: 10,
    # Air Defence units
    AirDefence.SAM_SA_19_Tunguska_Grison: 30,
    AirDefence.SAM_SA_6_Kub_Gainful_TEL: 20,
    AirDefence.SAM_SA_3_S_125_Goa_LN: 6,
    AirDefence.SAM_SA_11_Buk_Gadfly_Fire_Dome_TEL: 30,
    AirDefence.SAM_SA_11_Buk_Gadfly_C2: 25,
    AirDefence.SAM_SA_11_Buk_Gadfly_Snow_Drift_SR: 28,
    AirDefence.SAM_SA_8_Osa_Gecko_TEL: 28,
    AirDefence.SAM_SA_15_Tor_Gauntlet: 40,
    AirDefence.SAM_SA_13_Strela_10M3_Gopher_TEL: 16,
    AirDefence.SAM_SA_9_Strela_1_Gaskin_TEL: 12,
    AirDefence.SAM_SA_8_Osa_LD_9T217: 22,
    AirDefence.SAM_Patriot_CR__AMG_AN_MRC_137: 35,
    AirDefence.SAM_Patriot_ECS: 30,
    AirDefence.SPAAA_Gepard: 24,
    AirDefence.SAM_Hawk_Platoon_Command_Post__PCP: 14,
    AirDefence.SPAAA_Vulcan_M163: 10,
    AirDefence.SAM_Hawk_LN_M192: 8,
    AirDefence.SAM_Chaparral_M48: 16,
    AirDefence.SAM_Linebacker___Bradley_M6: 18,
    AirDefence.SAM_Patriot_LN: 15,
    AirDefence.SAM_Avenger__Stinger: 20,
    AirDefence.SAM_Patriot_EPP_III: 15,
    AirDefence.SAM_Patriot_C2_ICC: 18,
    AirDefence.SAM_Roland_ADS: 12,
    AirDefence.MANPADS_Stinger: 6,
    AirDefence.MANPADS_Stinger_C2_Desert: 4,
    AirDefence.MANPADS_Stinger_C2: 4,
    AirDefence.SPAAA_ZSU_23_4_Shilka_Gun_Dish: 10,
    AirDefence.SPAAA_ZSU_57_2: 12,
    AirDefence.AAA_ZU_23_Closed_Emplacement: 6,
    AirDefence.AAA_ZU_23_Emplacement: 6,
    AirDefence.SPAAA_ZU_23_2_Mounted_Ural_375: 7,
    AirDefence.AAA_ZU_23_Insurgent_Closed_Emplacement: 6,
    AirDefence.SPAAA_ZU_23_2_Insurgent_Mounted_Ural_375: 7,
    AirDefence.AAA_ZU_23_Insurgent_Emplacement: 6,
    AirDefence.MANPADS_SA_18_Igla_Grouse: 10,
    AirDefence.MANPADS_SA_18_Igla_Grouse_C2: 8,
    AirDefence.MANPADS_SA_18_Igla_S_Grouse: 12,
    AirDefence.MANPADS_SA_18_Igla_S_Grouse_C2: 8,
    AirDefence.EWR_1L13: 30,
    AirDefence.SAM_SA_6_Kub_Straight_Flush_STR: 22,
    AirDefence.EWR_55G6: 30,
    AirDefence.MCC_SR_Sborka_Dog_Ear_SR: 10,
    AirDefence.SAM_Hawk_TR__AN_MPQ_46: 14,
    AirDefence.SAM_Hawk_SR__AN_MPQ_50: 18,
    AirDefence.SAM_Patriot_STR: 22,
    AirDefence.SAM_Hawk_CWAR_AN_MPQ_55: 20,
    AirDefence.SAM_P19_Flat_Face_SR__SA_2_3: 14,
    AirDefence.SAM_Roland_EWR: 16,
    AirDefence.SAM_SA_3_S_125_Low_Blow_TR: 14,
    AirDefence.SAM_SA_2_S_75_Guideline_LN: 8,
    AirDefence.SAM_SA_2_S_75_Fan_Song_TR: 12,
    AirDefence.SAM_Rapier_LN: 6,
    AirDefence.SAM_Rapier_Tracker: 6,
    AirDefence.SAM_Rapier_Blindfire_TR: 8,
    AirDefence.HQ_7_Self_Propelled_LN: 20,
    AirDefence.HQ_7_Self_Propelled_STR: 24,
    AirDefence.AAA_8_8cm_Flak_18: 6,
    AirDefence.AAA_Flak_38_20mm: 6,
    AirDefence.AAA_8_8cm_Flak_36: 8,
    AirDefence.AAA_8_8cm_Flak_37: 9,
    AirDefence.AAA_Flak_Vierling_38_Quad_20mm: 5,
    AirDefence.AAA_SP_Kdo_G_40: 8,
    AirDefence.SL_Flakscheinwerfer_37: 4,
    AirDefence.PU_Maschinensatz_33: 10,
    AirDefence.AAA_8_8cm_Flak_41: 10,
    AirDefence.EWR_FuMG_401_Freya_LZ: 25,
    AirDefence.AAA_Bofors_40mm: 8,
    AirDefence.AAA_S_60_57mm: 8,
    AirDefence.AAA_M1_37mm: 7,
    AirDefence.AAA_M45_Quadmount_HB_12_7mm: 4,
    AirDefence.AAA_QF_3_7: 10,
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
    AirDefence.SAM_SA_10_S_300_Grumble_C2: 18,
    AirDefence.SAM_SA_10_S_300_Grumble_Flap_Lid_TR: 24,
    AirDefence.SAM_SA_10_S_300_Grumble_Clam_Shell_SR: 30,
    AirDefence.SAM_SA_10_S_300_Grumble_Big_Bird_SR: 30,
    AirDefence.SAM_SA_10_S_300_Grumble_TEL_C: 22,
    AirDefence.SAM_SA_10_S_300_Grumble_TEL_D: 22,
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
Units separated by country. 
country : DCS Country name
"""
FACTIONS = FactionLoader()

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
    "Mid-90s - Winter [1995]": datetime(1995, 1, 1),
    "Mid-90s - Spring [1995]": datetime(1995, 4, 1),
    "Mid-90s - Summer [1995]": datetime(1995, 6, 1),
    "Mid-90s - Fall [1995]": datetime(1995, 10, 1),
    "Gulf War - Fall [1990]": datetime(1990, 10, 1),
    "Modern - Winter [2010]": datetime(2010, 1, 1),
    "Modern - Spring [2010]": datetime(2010, 4, 1),
    "Modern - Summer [2010]": datetime(2010, 6, 1),
    "Modern - Fall [2010]": datetime(2010, 10, 1),
    "Georgian War [2008]": datetime(2008, 8, 7),
    "Syrian War [2011]": datetime(2011, 3, 15),
    "6 days war [1967]": datetime(1967, 6, 5),
    "Yom Kippour War [1973]": datetime(1973, 10, 6),
    "First Lebanon War [1982]": datetime(1982, 6, 6),
    "Arab-Israeli War [1948]": datetime(1948, 5, 15),
}

REWARDS = {
    "power": 4,
    "warehouse": 2,
    "ware": 2,
    "fuel": 2,
    "ammo": 2,
    "farp": 1,
    # TODO: Should generate no cash once they generate units.
    # https://github.com/dcs-liberation/dcs_liberation/issues/1036
    "factory": 10,
    "comms": 10,
    "oil": 10,
    "derrick": 8,
}

CARRIER_CAPABLE = [
    FA_18C_hornet,
    F_14A_135_GR,
    F_14B,
    AV8BNA,
    Su_33,
    A_4E_C,
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
    SA342Mistral,
]

"""
---------- END OF CONFIGURATION SECTION
"""

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
        elif name == "Carrier Strike Group 8":
            return CVN_75_Harry_S__Truman
        else:
            return CVN_71_Theodore_Roosevelt
    elif unit == CV_1143_5_Admiral_Kuznetsov:
        return CV_1143_5_Admiral_Kuznetsov_2017
    else:
        return unit


MANPADS: List[Type[VehicleType]] = [
    AirDefence.MANPADS_SA_18_Igla_Grouse,
    AirDefence.MANPADS_SA_18_Igla_S_Grouse,
    AirDefence.MANPADS_Stinger,
]

INFANTRY: List[VehicleType] = [
    Infantry.Paratrooper_AKS,
    Infantry.Paratrooper_AKS,
    Infantry.Paratrooper_AKS,
    Infantry.Paratrooper_AKS,
    Infantry.Paratrooper_AKS,
    Infantry.Infantry_RPG,
    Infantry.Infantry_M4,
    Infantry.Infantry_M4,
    Infantry.Infantry_M4,
    Infantry.Infantry_M4,
    Infantry.Infantry_M4,
    Infantry.Infantry_M249,
    Artillery.Mortar_2B11_120mm,
    Infantry.Infantry_AK_74,
    Infantry.Infantry_AK_74,
    Infantry.Infantry_AK_74,
    Infantry.Infantry_AK_74,
    Infantry.Infantry_AK_74,
    Infantry.Paratrooper_RPG_16,
    Infantry.Infantry_M4_Georgia,
    Infantry.Infantry_M4_Georgia,
    Infantry.Infantry_M4_Georgia,
    Infantry.Infantry_M4_Georgia,
    Infantry.Infantry_AK_74_Rus,
    Infantry.Infantry_AK_74_Rus,
    Infantry.Infantry_AK_74_Rus,
    Infantry.Infantry_AK_74_Rus,
    Infantry.Infantry_SMLE_No_4_Mk_1,
    Infantry.Infantry_SMLE_No_4_Mk_1,
    Infantry.Infantry_SMLE_No_4_Mk_1,
    Infantry.Infantry_Mauser_98,
    Infantry.Infantry_Mauser_98,
    Infantry.Infantry_Mauser_98,
    Infantry.Infantry_Mauser_98,
    Infantry.Infantry_M1_Garand,
    Infantry.Infantry_M1_Garand,
    Infantry.Infantry_M1_Garand,
    Infantry.Insurgent_AK_74,
    Infantry.Insurgent_AK_74,
    Infantry.Insurgent_AK_74,
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
        data = json.load(fdata)
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


def flying_type_from_name(name: str) -> Optional[Type[FlyingType]]:
    unit_type = plane_map.get(name)
    if unit_type is not None:
        return unit_type
    return helicopter_map.get(name)


def unit_type_of(unit: Unit) -> UnitType:
    if isinstance(unit, Vehicle):
        return vehicle_map[unit.type]
    elif isinstance(unit, Ship):
        return ship_map[unit.type]
    else:
        return unit.type


def country_id_from_name(name):
    for k, v in country_dict.items():
        if v.name == name:
            return k
    return -1


class DefaultLiveries:
    class Default(Enum):
        af_standard = ""


OH_58D.Liveries = DefaultLiveries
F_16C_50.Liveries = DefaultLiveries
P_51D_30_NA.Liveries = DefaultLiveries
Ju_88A4.Liveries = DefaultLiveries
B_17G.Liveries = DefaultLiveries

# List of airframes that rely on their gun as a primary weapon. We confiscate bullets
# from most AI air-to-ground missions since they aren't smart enough to RTB when they're
# out of everything other than bullets (DCS does not have an all-but-gun winchester
# option) and we don't want to be attacking fully functional Tors with a Vulcan.
#
# These airframes are the exceptions. They probably should be using their gun regardless
# of the mission type.
GUN_RELIANT_AIRFRAMES: List[Type[FlyingType]] = [
    AH_1W,
    AH_64A,
    AH_64D,
    A_10A,
    A_10C,
    A_10C_2,
    A_20G,
    Bf_109K_4,
    FW_190A8,
    FW_190D9,
    F_86F_Sabre,
    Ju_88A4,
    Ka_50,
    MiG_15bis,
    MiG_19P,
    Mi_24V,
    Mi_28N,
    P_47D_30,
    P_47D_30bl1,
    P_47D_40,
    P_51D,
    P_51D_30_NA,
    SpitfireLFMkIX,
    SpitfireLFMkIXCW,
    Su_25,
    Su_25T,
]
