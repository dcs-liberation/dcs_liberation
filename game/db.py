import json
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import List, Optional, Type, Union

from dcs.countries import country_dict
from dcs.helicopters import (
    OH_58D,
    helicopter_map,
)
from dcs.mapping import Point

# mypy can't resolve these if they're wildcard imports for some reason.
from dcs.planes import (
    B_17G,
    FA_18C_hornet,
    F_16C_50,
    Ju_88A4,
    P_51D_30_NA,
    plane_map,
)
from dcs.ships import (
    ship_map,
    Speedboat,
    ELNYA,
    Dry_cargo_ship_2,
    Dry_cargo_ship_1,
    LHA_Tarawa,
    Stennis,
    KUZNECOW,
    CVN_71,
    CVN_75,
    CVN_73,
    CVN_72,
    CV_1143_5,
)
from dcs.terrain.terrain import Airport
from dcs.unit import Ship, Unit, Vehicle
from dcs.unitgroup import ShipGroup, StaticGroup
from dcs.unittype import UnitType, VehicleType
from dcs.vehicles import (
    AirDefence,
    Armor,
    Artillery,
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
from pydcs_extensions.jas39.jas39 import JAS39Gripen, JAS39Gripen_AG
from pydcs_extensions.mb339.mb339 import MB_339PAN
from pydcs_extensions.su57.su57 import Su_57

UNITINFOTEXT_PATH = Path("./resources/units/unit_info_text.json")

plane_map["A-4E-C"] = A_4E_C
plane_map["F-22A"] = F_22A
plane_map["MB-339PAN"] = MB_339PAN
plane_map["Su-57"] = Su_57
plane_map["Hercules"] = Hercules
plane_map["JAS39Gripen"] = JAS39Gripen
plane_map["JAS39Gripen_AG"] = JAS39Gripen_AG

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
    # armor
    Armor.MTLB: 4,
    Artillery.Grad_FDDM: 4,
    Armor.BRDM_2: 6,
    Armor.BTR_D: 6,
    Armor.BTR_80: 8,
    Armor.BTR_82A: 10,
    Armor.T_55: 18,
    Armor.T_72B: 20,
    Armor.T_72B3: 25,
    Armor.T_80UD: 25,
    Armor.T_90: 30,
    Armor.BMD_1: 8,
    Armor.BMP_1: 14,
    Armor.BMP_2: 16,
    Armor.BMP_3: 18,
    Armor.PT_76: 9,
    Armor.ZBD04A: 12,
    Armor.ZTZ96B: 30,
    Armor.Cobra: 4,
    Armor.M_113: 6,
    Armor.M1043_HMMWV_Armament: 2,
    Armor.M1045_HMMWV_TOW: 8,
    Armor.VAB_Mephisto: 12,
    Armor.M_2_Bradley: 12,
    Armor.M1126_Stryker_ICV: 10,
    Armor.M1128_Stryker_MGS: 14,
    Armor.M1134_Stryker_ATGM: 12,
    Armor.M_60: 16,
    Armor.M_1_Abrams: 25,
    Armor.Leclerc: 25,
    Armor.Leopard1A3: 18,
    Armor.Leopard_2A4: 20,
    Armor.Leopard_2A4_trs: 20,
    Armor.Leopard_2A5: 22,
    Armor.Leopard_2: 25,
    Armor.Merkava_Mk4: 25,
    Armor.TPZ: 5,
    Armor.Challenger2: 25,
    Armor.Chieftain_mk3: 20,
    Armor.Marder: 10,
    Armor.MCV_80: 10,
    Armor.LAV_25: 7,
    Armor.AAV7: 10,
    Artillery.MLRS: 55,
    Artillery.M_109: 25,
    Artillery.SAU_2_C9: 12,
    Artillery.SAU_Gvozdika: 18,
    Artillery.SAU_Akatsia: 24,
    Artillery.SAU_Msta: 30,
    Artillery.Grad_URAL: 15,
    Artillery.Uragan_BM_27: 50,
    Artillery.Smerch_HE: 40,
    Artillery._2B11_mortar: 4,
    Artillery.SpGH_Dana: 26,
    Artillery.PLZ05: 25,
    Artillery.T155_Firtina: 28,
    Artillery.Smerch: 60,
    Unarmed.UAZ_469: 3,
    Unarmed.Ural_375: 3,
    Unarmed.GAZ_3307: 2,
    Infantry.Soldier_M4: 1,
    Infantry.Soldier_AK: 1,
    Unarmed.M_818: 3,
    Unarmed.Land_Rover_109_S3: 1,
    Unarmed.GAZ_3308: 1,
    Unarmed.GAZ_66: 1,
    Unarmed.KAMAZ_Truck: 1,
    Unarmed.Land_Rover_101_FC: 1,
    Unarmed.Ural_4320_31: 1,
    Unarmed.Ural_4320T: 1,
    # WW2
    Armor.Pz_V_Panther_G: 24,
    Armor.Pz_IV_H: 16,
    Armor.Tiger_I: 24,
    Armor.Tiger_II_H: 26,
    Armor.Jagdpanther_G1: 18,
    Armor.JagdPz_IV: 11,
    Armor.Elefant_SdKfz_184: 18,
    Armor.Sd_Kfz_251: 4,
    Armor.Sd_Kfz_234_2_Puma: 8,
    Armor.M4_Sherman: 12,
    Armor.M4A4_Sherman_FF: 16,
    Armor.Cromwell_IV: 12,
    Unarmed.M30_CC: 2,
    Armor.M2A1_halftrack: 4,
    Armor.Centaur_IV: 10,
    Armor.Churchill_VII: 16,
    Armor.M8_Greyhound: 8,
    Armor.M10_GMC: 14,
    Armor.Stug_III: 12,
    Armor.Stug_IV: 14,
    Artillery.M12_GMC: 10,
    Armor.SturmPzIV: 10,
    Armor.Daimler_AC: 8,
    Armor.Tetrarch: 8,
    Unarmed.M4_Tractor: 2,
    Unarmed.Sd_Kfz_7: 1,
    Unarmed.Sd_Kfz_2: 1,
    Unarmed.Kubelwagen_82: 1,
    Unarmed.Blitz_36_6700A: 1,
    Unarmed.Bedford_MWD: 1,
    Unarmed.CCKW_353: 1,
    Unarmed.Willys_MB: 1,
    # ship
    KUZNECOW: 100,
    Stennis: 100,
    LHA_Tarawa: 50,
    Dry_cargo_ship_1: 10,
    Speedboat: 10,
    Dry_cargo_ship_2: 10,
    ELNYA: 10,
    # Air Defence units
    AirDefence._2S6_Tunguska: 30,
    AirDefence.Kub_2P25_ln: 20,
    AirDefence._5p73_s_125_ln: 6,
    AirDefence.SA_11_Buk_LN_9A310M1: 30,
    AirDefence.SA_11_Buk_CC_9S470M1: 25,
    AirDefence.SA_11_Buk_SR_9S18M1: 28,
    AirDefence.Osa_9A33_ln: 28,
    AirDefence.Tor_9A331: 40,
    AirDefence.Strela_10M3: 16,
    AirDefence.Strela_1_9P31: 12,
    AirDefence.SA_8_Osa_LD_9T217: 22,
    AirDefence.Patriot_AMG: 35,
    AirDefence.Patriot_ECS: 30,
    AirDefence.Gepard: 24,
    AirDefence.Hawk_pcp: 14,
    AirDefence.Vulcan: 10,
    AirDefence.Hawk_ln: 8,
    AirDefence.M48_Chaparral: 16,
    AirDefence.M6_Linebacker: 18,
    AirDefence.Patriot_ln: 15,
    AirDefence.M1097_Avenger: 20,
    AirDefence.Patriot_EPP: 15,
    AirDefence.Patriot_cp: 18,
    AirDefence.Roland_ADS: 12,
    AirDefence.Soldier_stinger: 6,
    AirDefence.Stinger_comm_dsr: 4,
    AirDefence.Stinger_comm: 4,
    AirDefence.ZSU_23_4_Shilka: 10,
    AirDefence.ZSU_57_2: 12,
    AirDefence.ZU_23_Emplacement_Closed: 6,
    AirDefence.ZU_23_Emplacement: 6,
    AirDefence.Ural_375_ZU_23: 7,
    AirDefence.ZU_23_Closed_Insurgent: 6,
    AirDefence.Ural_375_ZU_23_Insurgent: 7,
    AirDefence.ZU_23_Insurgent: 6,
    AirDefence.SA_18_Igla_manpad: 10,
    AirDefence.SA_18_Igla_comm: 8,
    AirDefence.SA_18_Igla_S_manpad: 12,
    AirDefence.SA_18_Igla_S_comm: 8,
    AirDefence._1L13_EWR: 30,
    AirDefence.Kub_1S91_str: 22,
    AirDefence._55G6_EWR: 30,
    AirDefence.Dog_Ear_radar: 10,
    AirDefence.Hawk_tr: 14,
    AirDefence.Hawk_sr: 18,
    AirDefence.Patriot_str: 22,
    AirDefence.Hawk_cwar: 20,
    AirDefence.P_19_s_125_sr: 14,
    AirDefence.Roland_Radar: 16,
    AirDefence.Snr_s_125_tr: 14,
    AirDefence.S_75M_Volhov: 8,
    AirDefence.SNR_75V: 12,
    AirDefence.Rapier_fsa_launcher: 6,
    AirDefence.Rapier_fsa_optical_tracker_unit: 6,
    AirDefence.Rapier_fsa_blindfire_radar: 8,
    AirDefence.HQ_7_LN_SP: 20,
    AirDefence.HQ_7_STR_SP: 24,
    AirDefence.Flak18: 6,
    AirDefence.Flak30: 6,
    AirDefence.Flak36: 8,
    AirDefence.Flak37: 9,
    AirDefence.Flak38: 5,
    AirDefence.KDO_Mod40: 8,
    AirDefence.Flakscheinwerfer_37: 4,
    AirDefence.Maschinensatz_33: 10,
    AirDefence.Flak41: 10,
    AirDefence.FuMG_401: 25,
    AirDefence.Bofors40: 8,
    AirDefence.S_60_Type59_Artillery: 8,
    AirDefence.M1_37mm: 7,
    AirDefence.M45_Quadmount: 4,
    AirDefence.QF_37_AA: 10,
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
    AirDefence.S_300PS_54K6_cp: 18,
    AirDefence.S_300PS_40B6M_tr: 24,
    AirDefence.S_300PS_40B6MD_sr: 30,
    AirDefence.S_300PS_64H6E_sr: 30,
    AirDefence.S_300PS_5P85C_ln: 22,
    AirDefence.S_300PS_5P85D_ln: 22,
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

"""
---------- END OF CONFIGURATION SECTION
"""

StartingPosition = Union[ShipGroup, StaticGroup, Airport, Point]


def upgrade_to_supercarrier(unit, name: str):
    if unit == Stennis:
        if name == "CVN-71 Theodore Roosevelt":
            return CVN_71
        elif name == "CVN-72 Abraham Lincoln":
            return CVN_72
        elif name == "CVN-73 George Washington":
            return CVN_73
        elif name == "CVN-75 Harry S. Truman":
            return CVN_75
        elif name == "Carrier Strike Group 8":
            return CVN_75
        else:
            return CVN_71
    elif unit == KUZNECOW:
        return CV_1143_5
    else:
        return unit


MANPADS: List[Type[VehicleType]] = [
    AirDefence.SA_18_Igla_manpad,
    AirDefence.SA_18_Igla_S_manpad,
    AirDefence.Soldier_stinger,
]

INFANTRY: List[VehicleType] = [
    Infantry.Paratrooper_AKS_74,
    Infantry.Paratrooper_AKS_74,
    Infantry.Paratrooper_AKS_74,
    Infantry.Paratrooper_AKS_74,
    Infantry.Paratrooper_AKS_74,
    Infantry.Soldier_RPG,
    Infantry.Soldier_M4,
    Infantry.Soldier_M4,
    Infantry.Soldier_M4,
    Infantry.Soldier_M4,
    Infantry.Soldier_M4,
    Infantry.Soldier_M249,
    Artillery._2B11_mortar,
    Infantry.Soldier_AK,
    Infantry.Soldier_AK,
    Infantry.Soldier_AK,
    Infantry.Soldier_AK,
    Infantry.Soldier_AK,
    Infantry.Paratrooper_RPG_16,
    Infantry.Soldier_M4_GRG,
    Infantry.Soldier_M4_GRG,
    Infantry.Soldier_M4_GRG,
    Infantry.Soldier_M4_GRG,
    Infantry.Infantry_AK,
    Infantry.Infantry_AK,
    Infantry.Infantry_AK,
    Infantry.Infantry_AK,
    Infantry.Soldier_wwii_br_01,
    Infantry.Soldier_wwii_br_01,
    Infantry.Soldier_wwii_br_01,
    Infantry.Soldier_mauser98,
    Infantry.Soldier_mauser98,
    Infantry.Soldier_mauser98,
    Infantry.Soldier_mauser98,
    Infantry.Soldier_wwii_us,
    Infantry.Soldier_wwii_us,
    Infantry.Soldier_wwii_us,
    Infantry.Infantry_AK_Ins,
    Infantry.Infantry_AK_Ins,
    Infantry.Infantry_AK_Ins,
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


def unit_get_expanded_info(
    country_name: str, unit_type: Type[UnitType], request_type: str
) -> str:
    original_name = unit_type.name and unit_type.name or unit_type.id
    default_value = None
    faction_value = None
    with UNITINFOTEXT_PATH.open("r", encoding="utf-8") as fdata:
        data = json.load(fdata)
    type_exists = data.get(unit_type.id)
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
